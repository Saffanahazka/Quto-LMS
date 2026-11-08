import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    model: str
    grounding_threshold: float
    max_retries: int
    max_tokens: int = 4000
    base_url: str = "https://api.groq.com/openai/v1"
    disable_password_reset: bool = False
    admin_api_key: str | None = None
    enable_demo_lecturer_registration: bool = False
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None

    @property
    def smtp_configured(self) -> bool:
        return bool(self.smtp_host and self.smtp_from) and (
            bool(self.smtp_username) == bool(self.smtp_password)
        )


def get_settings() -> Settings:
    load_dotenv(dotenv_path=ENV_FILE, override=False)
    api_key = os.getenv("LLM_API_KEY", "").strip()
    if not api_key or api_key.casefold() == "your_groq_api_key_here":
        api_key = (dotenv_values(ENV_FILE).get("LLM_API_KEY") or "").strip()
    if api_key.casefold() == "your_groq_api_key_here":
        api_key = ""
    return Settings(
        api_key=api_key or None,
        model=os.getenv("QUTO_MODEL", "openai/gpt-oss-120b"),
        grounding_threshold=float(os.getenv("QUTO_GROUNDING_THRESHOLD", "0.6")),
        base_url=os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1"),
        max_retries=int(os.getenv("QUTO_MAX_RETRIES", "2")),
        disable_password_reset=os.getenv("QUTO_DISABLE_PASSWORD_RESET", "false").strip().lower()
        in {"1", "true", "yes", "on"},
        admin_api_key=os.getenv("QUTO_ADMIN_API_KEY") or None,
        enable_demo_lecturer_registration=os.getenv(
            "QUTO_ENABLE_DEMO_LECTURER_REGISTRATION", "false"
        ).strip().lower()
        in {"1", "true", "yes", "on"},
        smtp_host=os.getenv("QUTO_SMTP_HOST") or None,
        smtp_port=int(os.getenv("QUTO_SMTP_PORT", "587")),
        smtp_username=os.getenv("QUTO_SMTP_USERNAME") or None,
        smtp_password=os.getenv("QUTO_SMTP_PASSWORD") or None,
        smtp_from=os.getenv("QUTO_SMTP_FROM") or None,
    )
