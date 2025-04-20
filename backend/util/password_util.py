from passlib.context import CryptContext
from beanie import PydanticObjectId


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "d594dd02eff8db4186b2ee6c45182c4cee8e6db0aa6844036db3e6f7d1c05df8"
ALGORITHM = "HS256"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(user_password: str, entered_password: str):
    if not verify_password(entered_password, user_password):
        return False
    return True