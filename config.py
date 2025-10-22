import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./mahinsight.db')
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
CORS_ORIGINS: List[str] = os.getenv('CORS_ORIGINS', '*').split(',')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'info')
RATE_LIMIT_PER_MIN = int(os.getenv('RATE_LIMIT_PER_MIN', '60'))

