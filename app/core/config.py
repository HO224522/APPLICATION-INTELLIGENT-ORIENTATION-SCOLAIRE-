import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "Burkina Faso Educational Guidance AI Engine"
    ENV: str = os.getenv("ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Weight settings for scoring components (Configurable and testable)
    WEIGHT_ACADEMIC: float = 0.30
    WEIGHT_INTEREST: float = 0.25
    WEIGHT_APTITUDE: float = 0.15
    WEIGHT_PREFERENCE: float = 0.10
    WEIGHT_GOAL: float = 0.10
    WEIGHT_FEASIBILITY: float = 0.10

    # Data privacy settings
    ENFORCE_DATA_MINIMIZATION: bool = True
    ANONYMIZE_MINORS_DATA: bool = True

settings = Settings()
