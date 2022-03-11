from flask import Flask, request
from app.models import User
from http import HTTPStatus
from app.exceptions import EmailAlreadyExist
from app.exceptions import TypeFieldError

app = Flask(__name__)



@app.get("/user")
def retrieve_users():
    response = User.read_database()
    return {"data":response},HTTPStatus.OK


@app.post("/user")
def register_user():
    data = request.get_json()
    try:
        user = User(**data)
    except TypeFieldError as error:
        return {"wrong fields":error.message},error.status_code
    except EmailAlreadyExist as error:
        return {"error": error.message},error.status_code

    dict_user = user.__dict__
    response = user.add_to_database(dict_user)
  
    return {"data":response}