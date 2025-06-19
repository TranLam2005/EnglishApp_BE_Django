import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = os.getenv("DJANGO_ENV", "development")

if env == "production":
    from .production import *
else:
    from .development import *