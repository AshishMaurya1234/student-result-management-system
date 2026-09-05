import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "ignou-bcsp064-dev-secret-key-default-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Centralized grade point mapping (Standard Academic Scale)
    GRADE_POINT_MAP = {
        "A+": 10,
        "A": 9,
        "B+": 8,
        "B": 7,
        "C": 6,
        "D": 5,
        "F": 0
    }

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR / 'instance' / 'student_results.db'}"
    )

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

class TestingConfig(Config):
    """Test environment configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
