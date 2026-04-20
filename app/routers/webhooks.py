from fastapi import APIRouter, Request, HTTPException, Header
import hmac, hashlib
from app.core.config import settings

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

SENDGRID_WEBHOOK_SECRET = "your-webhook-signing-secret"

def verify_sendgrid_signature(payload: bytes, signature: str, timestamp: str) -> bool:
    expected = hmac.new(
        SENDGRID_WEBHOOK_SECRET.encode(),
        timestamp.encode() + payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@router.post("/sendgrid")
async def sendgrid_events(
    request: Request,
    x_twilio_email_event_webhook_signature: str = Header(None),
    x_twilio_email_event_webhook_timestamp: str = Header(None),
):
    body = await request.body()

    # Verify signature (skip in dev, NEVER skip in prod)
    # if not verify_sendgrid_signature(body, sig, ts):
    #     raise HTTPException(status_code=403, detail="Invalid signature")

    events = await request.json()
    for event in events:
        email = event.get("email")
        event_type = event.get("event")  # bounce, spamreport, unsubscribe

        if event_type in ("bounce", "spamreport", "unsubscribe"):
            # TODO: insert into suppression_list table
            print(f"SUPPRESSING {email} — reason: {event_type}")

    return {"received": len(events)}