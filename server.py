""" Server.py """

# modules
import bottle
from bottle import run, get, post, request
from marshmallow import ValidationError
import datetime as dt
import jwt

# app
from app.models import User, create_tables, Nota
from app.schemas import user_schema, nota_schema, notas_schema
from app.security import security_validated, token_generated, token_required
from app.utils import EnableCors

app = bottle.app()

@app.post('/api/v1/login')
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



@app.post("/api/v1/register")
def register():
    """ Function register new user """
    json_input = request.json

    #Validate fields
    try:
        data = user_schema.load(json_input).data
    except ValidationError as err:
        return {'status':"error", "message": err.messages}

    # Email is exist in data base
    try:
        rpta = User.get(User.email == data['email'])
    except User.DoesNotExist:
        user = User.create(
            email = data["email"],
            password = security_validated.hashed_password(data["password"]),
            first_name = data["first_name"],
            last_name = data["last_name"],
            created_at = dt.datetime.now(),
            updated_at = dt.datetime.now(),
        )
        response_data = user_schema.dump(user).data

        del response_data['user']['password']

        return {'status':"Successful", 'data': response_data, 'message': "Successfully created user: {}".format(user.email)}
    else:
        return {'status':"Error", "message": "That email address is already in the database"}


@app.get("/api/v1/notas")
@token_required
def get_notas(user):
    notas = Nota.select().order_by(Nota.posted_on.asc())  # Get all notas
    return notas_schema.dump(list(notas)).data


@app.get("/api/v1/notas/<pk>")
@token_required
def get_nota(pk, user):
    nota = Nota.get(Nota.id == pk)
    if not nota:
        return {"errors": "nota could not be find"}
    return nota_schema.dump(nota).data


@app.post("/api/v1/notas")
@token_required
def new_nota(user):

    json_input = request.json
    try:
        nota = nota_schema.load(json_input).data
    except ValidationError as err:
        return {"errors": err.messages}
    nota.user = user
    nota.save()
    return nota_schema.dump(nota).data


if __name__ == "__main__":
    create_tables()
    app.install(EnableCors())
    app.run(host='localhost', port=8000, reloader=True, debug=True)