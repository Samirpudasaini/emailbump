import structlog
from celery import shared_task
from celery.utils.log import get_task_logger
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

logger = get_task_logger(__name__)
log = structlog.get_logger()

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,         # 1 min, then exponential
    rate_limit=settings.CELERY_TASK_RATE_LIMIT,
    name="app.tasks.email_tasks.send_email_task",
)
def send_email_task(self, to_email: str, subject: str, html_content: str, user_id: str):
    """
    Sends a single email via SendGrid.
    Retries up to 3x with exponential backoff on transient failures.
    """
    try:
        message = Mail(
            from_email=(settings.FROM_EMAIL, settings.FROM_NAME),
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        log.info(
            "email_sent",
            to=to_email,
            status=response.status_code,
            user_id=user_id,
        )
        return {"status": response.status_code, "to": to_email}

    except Exception as exc:
        log.error("email_send_failed", to=to_email, error=str(exc))
        # Exponential backoff: 60s, 120s, 240s
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))