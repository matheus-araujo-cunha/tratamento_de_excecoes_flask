from http import HTTPStatus
from os import getenv
from app.exceptions import TypeFieldError
from app.exceptions import EmailAlreadyExist
import ujson as json


DATABASE_FILEPATH = getenv("DATABASE_FILEPATH")


types = {
    "<class 'int'>": "integer",
    "<class 'float'>": "float",
    "<class 'dict'>": "dictionary",
    "<class 'NoneType'>": "none",
    "<class 'list'>" : "list",
    "<class 'bool'>":"boolean"
}


def validate_fields(name,email):
    fields_error = []
    
    field_name = validate_name(name,fields_error)
    field_email = validate_email(email,fields_error)

    if fields_error:
        raise TypeFieldError(fields_error,HTTPStatus.BAD_REQUEST)

    return {"name" : field_name, "email" : field_email}

def validate_email(email:str,fields_error:list):

    assert_field = check_field(email)
  
    if not assert_field:
        type_field = types[str(type(email))]
        type(email).__name__
        fields_error.append({"email":type_field})
        return fields_error
    check_email_exist(email)
    return format_email(email)


def validate_name(name:str,fields_error:list):
    
    assert_field = check_field(name)
    if not assert_field:
        type_field = types[str(type(name))]
        fields_error.append({"name":type_field})
        return fields_error
    return format_name(name)

def format_name(name:str):
    return name.title()
    
def format_email(email:str):
    return email.casefold()


def check_field(data):
    return type(data) is str
    

def check_database():
    try:
        with open(DATABASE_FILEPATH,"r") as database_reader:
            data = json.load(database_reader)
            return data
    except (FileNotFoundError,ValueError):
        with open(DATABASE_FILEPATH,"w") as database_writer:   
            json.dump([],database_writer,indent=2)
            return []               

def check_email_exist(email):    
    database = check_database()
    response = [data for data in database if data["email"] == email ]

    if response:
        raise EmailAlreadyExist(HTTPStatus.CONFLICT)
    return email


def create_user_id():
    database = check_database()

    if not database:
        return 1     

    last_user_id = database[-1]["id"]       
    return last_user_id + 1