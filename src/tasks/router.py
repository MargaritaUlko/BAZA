from fastapi import APIRouter, Depends, BackgroundTasks

# from main import current_user
from src.tasks.tasks import send_email_report_dashboard, show_email_report_dashboard

router = APIRouter(prefix = "/report")

# @router.get("/dashboard")
# def get_dashboard_report(background_tasks = BackgroundTasks,user = Depends(current_user)):
#     background_tasks.add_task(send_email_report_dashboard(), user.username)
#     send_email_report_dashboard(user.username)
    # return{
    # "status": 200,
    # "text": "Письмо отправлено"
    # }
@router.get("/dashboard")
# def get_dashboard_report(user = Depends(current_user)):
def get_dashboard_report():
    # show_email_report_dashboard.delay()
    show_email_report_dashboard()
    return {
        "status": 200,
        "text": "Письмо отправлено"
    }
