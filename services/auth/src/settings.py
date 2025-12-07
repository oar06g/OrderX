import os
from dotenv import load_dotenv

load_dotenv()

# --- Database config ---
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB_USERS = os.getenv("MYSQL_DB_USERS")
DB_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_USERS}"

# --- JWT config ---
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT", "123456yuikdmgfsjdlk09w")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 2

