import hashlib
import hmac
import json

from fastapi import HTTPException
from app.core.settings import settings