from fastapi import FastAPI, Depends, Request, HTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limiter import limiter
from app.dependencies.auth import get_current_user
from app.schemas.email import EmailRequest
from app.tasks.email_tasks import send_email_task
from app.core.security import create_access_token
import structlog

log = structlog.get_logger()

app = FastAPI(title="Secure Email Platform", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/auth/token")
def get_token(username: str, password: str):
    # Replace with real DB lookup
    if username == "admin" and password == "secret":
        return {"access_token": create_access_token(username), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/v1/send-email")
@limiter.limit("30/minute")
async def send_email(
    request: Request,
    payload: EmailRequest,
    current_user: str = Depends(get_current_user),
):
    # TODO Day 4: check suppression list before queuing
    task = send_email_task.delay(
        to_email=str(payload.to_email),
        subject=payload.subject,
        html_content=payload.html_content,
        user_id=current_user,
    )
    log.info("email_queued", task_id=task.id, to=str(payload.to_email), user=current_user)
    return {"task_id": task.id, "status": "queued"}

@app.get("/health")
def health():
    return {"status": "ok"}