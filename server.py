""" Server.py """

# modules
from bottle import run, get, post, request, error
from marshmallow import ValidationError
import datetime as dt
import jwt

# app
from app.models import User, create_tables
from app.schemas import user_schema
from app.security import security_validated, token_generated, token_required


@post('/login')
def login():
    """ Function to login user """
    json_input = request.json
    response_data = {}

    # Validate fields from form
    try:
        data = user_schema.load(json_input).data
    except ValidationError as err:
        return {'status':"error", "message": err.messages}#, 422

    # User and password validate
    try:
        user = User.select().where(
                (User.email == data["email"])
           ).get()
        user = user_schema.dump(user).data['user']

        # Password validate
        if not (user is None) and (security_validated.compare_password(str(user["password"]), data["password"]) == True):

            token = token_generated.generate_token(user)

            del user['password']

            response_data['user'] = user
            response_data['token'] = token

            return {'status': "Successful", "data": response_data, "message": "Usuario logueado correctamente"}#, 200

    except ValidationError as err:
        return {'status':"error", "message": err.messages}

    return {'status':"error", "message": "That email or password are incorrect"}#, 400




if __name__ == "__main__":
    create_tables()
    run(host='localhost', port=8000, reloader=True, debug=True)