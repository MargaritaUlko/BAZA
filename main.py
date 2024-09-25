import logging
import time

from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, BaseModel
from typing_extensions import Optional
from fastapi_users.authentication import JWTStrategy
from fastapi import Form
from src.auth import schemas
from src.auth.manager import UserManager
from fastapi.middleware.cors import CORSMiddleware
from anyio import Path
from fastapi import FastAPI, Depends, Request, BackgroundTasks, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import asyncio as aioredis
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.operations.models import operation
from src.tasks.tasks import send_email_report_dashboard, show_email_report_dashboard
from src.operations.router import router as router_operation
from src.auth.auth import auth_backend
from database import User, get_async_session, async_session_maker
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
import os
from src.tasks.tasks import show_email_report_dashboard
from src.tasks.router import router as bebrarouter
from utils import hash_password
import jwt
# from jose.exceptions import JWTError

# Отправляем задачу в очередь
# result = show_email_report_dashboard.delay()
result = show_email_report_dashboard()
# Проверяем результат
print(f"Task Status: {result}")

# Получаем абсолютный путь к текущей рабочей директории
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "src", "static")

# Настройка базовой конфигурации логирования
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s')

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trading App",
    docs_url="/docs",  # Убедитесь, что этот параметр не равен None
    redoc_url="/redoc"  # Проверьте также этот параметр
)
app.include_router(bebrarouter)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="krmfk")
@app.get("/")
async def read_root():
    return {"Hello": "World"}


app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=static_dir)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# origins = [
#     "https://localhost:8000",
#     "http://127.0.0.1:8000/docs"
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins ,
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"]
# )

@app.post("/send-email/")
async def send_email( request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [JWTStrategy(secret="SECRET", lifetime_seconds=3600)]
)

logger = logging.getLogger(__name__)


class LoginForm(BaseModel):
    email: str
    password: str



@app.post("/log-in/")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    user_manager: UserManager = Depends(get_user_manager)
):
    user = await user_manager.authenticate(email=email, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token_type": "bearer"}








@app.post("/create-user/")
async def create_user(
    # user_manager: schemas.UserCreate,
    user_manager: UserManager = Depends(get_user_manager),
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),

):

    user_create = UserCreate(
        username=name,
        email=email,
        password=password,
        role_id=1,  # Обновите это на role_id
        is_active = True,
        is_superuser= False,
        is_verified = False
    )
    # bebra = UserManager()
    created_user = await user_manager.create(user_create)
    return {"message": "User created successfully", "user": created_user}



@app.post("/send-email/")
async def send_email():
    # Placeholder implementation
    return {"message": "Email sending functionality not implemented yet"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.url.path.startswith("/docs"):
        return await call_next(request)
    async with async_session_maker() as session:
        result1 = await session.execute(select(operation))
        operations = result1.fetchall()  # Извлечение данных как списка кортежей
        operations_dict = [{"figi": op.figi, "type": op.type} for op in operations]
        response = templates.TemplateResponse("bebra.html", {"request": request, "operations": operations_dict})
        response = await call_next(request)
        return response




    # start_time = time.time()
    # response = await call_next(request)
    # process_time = time.time() - start_time
    # response.headers["X-Process-Time"] = str(process_time)
    #
     # logger.info("This is an info message")
    # result1 = await session.execute(select(operation))
    # operations = result1.scalars().all()
    # if request.url.path == "/report/dashboard":
    #     return templates.TemplateResponse("bebra.html", {"request": request, "process_time": process_time, "operations": operations})

    # return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# async def create_user(
#     name: str = Form(...),
#     email: str = Form(...),
#     password: str = Form(...),
#     user_manager: UserManager = Depends(get_user_manager)  # Исправлено здесь
# ):
#     user_create = UserCreate(
#         username=name,
#         email=email,
#         password=password,
#         role_id=1,  # Установите нужное значение role_id
#         is_active=True,
#         is_superuser=False,
#         is_verified=False
#     )
#
#     created_user = await user_manager.create(user_create)  # Обратите внимание на await
#     return {"message": "User created successfully", "user": created_user}




# async def create_user(
#     name: str = Form(...),
#     email: str = Form(...),
#     password: str = Form(...),
#     user_manager: UserManager = Depends(get_user_manager)
# ):
#     user_create = schemas.UserCreate(
#         username=name,
#         email=email,
#         password=password,
#         role_id=1  # Обновите это на role_id
#     )
#     created_user = await user_manager.create(user_create)
#     return {"message": "User created successfully", "user": created_user}

# Define the endpoint to send an email (for now it just returns a message)