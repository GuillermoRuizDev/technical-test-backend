#Server.py

# bottle
from bottle import run, get, post, request, delete, put, template, make_response
from marshmallow import ValidationError

# app
from app.models import User, create_tables
from app.schemas import user_schema

#@get('/logout')


@get('/login')
def login():
    data_input = request.get_json()
    error = ""

    try:
        data = user_schema.load(data_input)
        #user = 
    except ValidationError as err:
        error = err.message

    if user is None or not check_password_hash(user['password'], password):
        error = 'Incorrect user or password'

    if error == "":
        payload = {
            'iat': datetime.utcnow(),                          # Current time
            'exp': datetime.utcnow() + timedelta(minutes=10),  # Expiration time
            'sub': user['name'],
            'rol': user['rol']
        }
        return make_response(jwt.encode(payload, current_app.config['SECRET_KEY'],algorithm='HS256'), 200)

    return make_response(error, 401)


#@app.route("/register", methods=["POST"])
@post("/register")
def register():
    json_input = request.get_json()
    try:
        data = user_schema.load(json_input)
    except ValidationError as err:
        return {"errors": err.messages}, 422
    try:  # Use get to see if user already exists
        User.get(User.email == data["email"])
    except User.DoesNotExist:
        user = User.create(
            email=data["email"], joined_on=dt.datetime.now(), password=data["password"]
        )
        message = "Successfully created user: {}".format(user.email)
    else:
        return {"errors": "That email address is already in the database"}, 400

    data = user_schema.dump(user)
    data["message"] = message
    return data, 201




create_tables()
run(host='localhost', port=8000)