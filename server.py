#Server.py

# bottle
from bottle import run, get, post, request
from marshmallow import ValidationError
import datetime as dt
import jwt

# app
from app.models import User, create_tables
from app.schemas import user_schema
from app.security import SecurityValidation, Tokenization

@get('/')
def say_hello():
    return "Hello World with Bottle"


@post('/login')
def login():
    data_input = request.json.get()
    res_data = {}

    try:
        data = user_schema.load(data_input)
    except ValidationError as err:
        return {'status':"error", "message": err.messages}, 422

    #try:  # Use get to see if user already exists
    user = User.select().where(
                (User.email == data["email"]) &
                (SecurityValidation.compare_password(User.username, data["password"]) == True)
           ).get()

    if not user is None:
        token = Tokenization.generate_token(user)
        del data['password']

        res_data['token'] = token
        res_data['user'] = user

        return {'status': "Successful", "data": res_data, "message": "Usuario logueado correctamente"}, 200

    return {'status':"error", "message": "That email or password are incorrect"}, 400



#@app.route("/register", methods=["POST"])
@post("/register")
def register():
    json_input = request.json
    try:
        data = user_schema.load(json_input)
    except ValidationError as err:
        return {'status':"error", "message": err.messages}, 422

    try:  # Use get to see if user already exists
        print(data)
        print(data[1])
        User.get(User.email == data["email"])
    except User.DoesNotExist:
        user = User.create(
            email = data["email"],
            password = data["password"],
            first_name = data["first_name"],
            last_name = data["last_name"],
            created_at = dt.datetime.now(),
            updated_at = dt.datetime.now(),
        )
        del user["password"]
        del user["updated_at"]
        return {'status':"Successful", 'data': data, 'message': "Successfully created user: {}".format(user.email)}, 201
    else:
        return {'status':"Error", "message": "That email address is already in the database"}, 400

    # data = user_schema.dump(user)
    # data["message"] = message
    # return {'status':"error", 'data': data, 'message': "Error "}, 201

if __name__ == "__main__":
    create_tables()
    run(host='localhost', port=8000, reloader=True, debug=True)