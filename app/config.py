import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DB_URL")
CORS_ORIGINS = [
    "http://localhost:3000",
]

IP_ADDRESS = "http://127.0.0.1:8000/"
IMAGE_DIR = "app/media/uploads/user/"
IMAGE_URL = "media/uploads/user/"

ACCESS_TOKEN_EXPIRE_TIME = 60 # in minutes
REFRESH_TOKEN_EXPIRE_TIME = 7

### Hashing
SECRET_KEY = os.environ.get("SECRET_KEY") # if you don't have one, you can generate one using `openssl rand -hex 32` in cmd
ENCRYPTION_ALGORITHM = "HS256"

CHECK_IF_ACTIVE = False