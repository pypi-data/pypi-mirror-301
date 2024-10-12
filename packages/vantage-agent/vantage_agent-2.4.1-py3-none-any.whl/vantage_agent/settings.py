"""Core module for defining global settings of the Vantage Agent."""

import sys
from pathlib import Path
from typing import Annotated, Optional

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from vantage_agent.logging import logger


def _define_dotenv_file_location() -> Path:
    """Define the location of the .env file based on the env var `DOTENV_FILE_LOCATION`.

    In case it is not set, the default location is defined as `.env`.
    """
    default_dotenv_file_location = Path("/var/snap/vantage-agent/common/.env")
    if default_dotenv_file_location.exists():
        return default_dotenv_file_location
    return Path(".env")


class Settings(BaseSettings):
    """Settings for the Vantage Agent."""

    SCONTROL_PATH: Path = Path("/usr/bin/scontrol")

    # Vantage API info
    BASE_API_URL: Annotated[str, AnyHttpUrl] = "https://apis.vantagehpc.io"

    # Sentry
    SENTRY_DSN: Optional[AnyHttpUrl] = None
    SENTRY_ENV: str = "local"

    # OIDC config for machine-to-machine security
    OIDC_DOMAIN: str
    OIDC_CLIENT_ID: str
    OIDC_CLIENT_SECRET: str
    OIDC_USE_HTTPS: bool = True

    CACHE_DIR: Path = Path.home() / ".cache/vantage-agent"

    # Task settings
    TASK_JOBS_INTERVAL_SECONDS: int = Field(30, ge=10, le=3600)  # seconds
    TASK_SELF_UPDATE_INTERVAL_SECONDS: Optional[int] = Field(30, ge=10)  # seconds

    @field_validator("SCONTROL_PATH", mode="after")
    @classmethod
    def validate_scontrol_path(cls, v: Path) -> Path:
        """Ensure that the SCONTROL_PATH is an absolute path."""
        if not v.is_absolute():
            raise ValueError("SCONTROL_PATH must be an absolute path")
        return v

    model_config = SettingsConfigDict(
        env_prefix="VANTAGE_AGENT_", env_file=_define_dotenv_file_location(), extra="ignore"
    )


def _init_settings() -> Settings:
    try:
        return Settings()  # type: ignore[call-arg]
    except ValueError as e:
        logger.error(e)
        sys.exit(1)


SETTINGS = _init_settings()
