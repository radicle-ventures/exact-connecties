import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["EXACT_CLIENT_ID"]
CLIENT_SECRET = os.environ["EXACT_CLIENT_SECRET"]
REDIRECT_URI = "https://www.exact.com/login"
BASE_URL = "https://start.exactonline.nl"
TOKEN_URL = f"{BASE_URL}/api/oauth2/token"
AUTH_URL = f"{BASE_URL}/api/oauth2/auth"
API_URL = f"{BASE_URL}/api/v1"
