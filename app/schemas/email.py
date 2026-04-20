from pydantic import BaseModel, EmailStr, field_validator
import re

ALLOWED_DOMAINS: set[str] = set()  # fill with your whitelist, or leave empty for all

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    html_content: str
    consent_given: bool   # GDPR/CAN-SPAM: must be True

    @field_validator("consent_given")
    @classmethod
    def must_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("Recipient consent is required")
        return v

    @field_validator("subject")
    @classmethod
    def no_spam_phrases(cls, v: str) -> str:
        blocked = ["FREE MONEY", "CLICK NOW", "ACT FAST", "LIMITED TIME"]
        for phrase in blocked:
            if phrase in v.upper():
                raise ValueError(f"Subject contains blocked phrase: {phrase}")
        return v