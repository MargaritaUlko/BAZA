import logging

from anyio import Path
from fastapi import FastAPI, Depends, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers

from src.tasks.tasks import send_email_report_dashboard, show_email_report_dashboard
from src.operations.router import router as router_operation
from src.auth.auth import auth_backend
from database import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
import os
from src.tasks.tasks import show_email_report_dashboard

# Отправляем задачу в очередь
result = show_email_report_dashboard.delay()

# Проверяем результат
print(f"Task ID: {result.id}")
print(f"Task Status: {result.status}")

# Получаем абсолютный путь к текущей рабочей директории
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "src", "static")

# Настройка базовой конфигурации логирования
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s')

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trading App"
)

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
    FastAPICache.init(RedisBackend(redis), prefix="krmfk")



app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=static_dir)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send-email/")
async def send_email( request: Request):
    # Добавляем задачу в фоновые задачи Celery

    return templates.TemplateResponse("success.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
