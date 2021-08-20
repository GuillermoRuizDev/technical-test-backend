from werkzeug.security import check_password_hash, generate_password_hash
import datetime as dt
from functools import wraps
from bottle import request
import jwt

from config import Config
class SecurityValidation:
    def hashed_password(self, value):
        return generate_password_hash(value).decode('utf-8')

    def compare_password(self, password_login, password_user):
        return check_password_hash(password_login, password_user)

class Tokenization:
    def generate_token(user):
        time = dt.datetime.utcnow() + dt.timedelta(hours=24)
        payload = {
            "user": {
                "email": f"{user['email']}",
                "id": f"{user['id']}",
            },
            "exp": time
        }
        new_token = jwt.encode(payload, Config.SECRET_KEY,'HS256')
        return new_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.headers)
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(token, Config.SECRET_KEY,'HS256')
            except:
                return {"status": "fail", "message": "unauthorized 1"}, 401
            return f(*args, **kwargs)
        else:
            return {"status": "fail", "message": "unauthorized 2"}, 401
    return decorated