from flask import Blueprint, make_response, jsonify, request
from connections import ConnectionMongo
import hashlib, uuid, re, os
from datetime import datetime

mongo_connection = ConnectionMongo().mongo_connect()
data_base = mongo_connection["users"]
user_collection = data_base["data_user"]

signup = Blueprint('signup',__name__)
@signup.route("/signup", methods=['POST'])
def singup():
    params = request.json
    return validator(params)

def validator(request_params):
    no_params_copy = "Parámetros incorrectos"
    invalid_mail_copy = "Formato de correo no válido"
    require_params = ["email","firstName","lastName","age","password"]
    if bool(request_params):
        if all(key in request_params for key in (require_params)):
            for item in request_params.values():
                if not item:
                    print("no value", item)
                    return error_handler(404,no_params_copy)

            request_params = clean_params(request_params)
            if not valid_email(request_params["email"]):
                return error_handler(404, invalid_mail_copy)
            return create_user(request_params)
        else:
            return error_handler(404,no_params_copy)
    else:
        return error_handler(404,no_params_copy)

def create_user(request_params):
    used_mail_copy = "El correo ya se encuentra en uso"
    db_error_copy = "Error en base de datos"
    success_copy = "El usuario fue creado con éxito"
    try:
        token = str(uuid.uuid4())
        email =  request_params['email']
        filter_dict = {"email":email}
        if user_collection.count_documents(filter_dict):
            return error_handler(404,used_mail_copy) 
        user_data = {
            "email" : request_params["email"],
            "password": hashlib.sha512((request_params["password"] + os.getenv("SALT")).encode('utf-8')).hexdigest(),
            "first_name": request_params['firstName'],
            "last_name": request_params['lastName'],
            "token": token,
            "created": datetime.today().replace(microsecond=0),
            "last_update":datetime.today().replace(microsecond=0)
        }
        insert = user_collection.insert_one(user_data)
        print(insert.inserted_id)
        response = {
            'status':201,
            'code': 'success',
            "data": success_copy
        }
        return make_response(jsonify(response),201) 
    except Exception as exception:
        print(exception)
        return error_handler(404, db_error_copy)

def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not (re.fullmatch(regex, email)):
        return False
    return True

def clean_params(request_params):
    regex = '[^a-zA-Z0-9 \n\.]'
    request_params["email"] = re.sub('[^a-zA-Z0-9 \n\.\@]', '', request_params["email"].strip()).lower()
    request_params["firstName"] = re.sub(regex, '', request_params["firstName"].strip())
    request_params["lastName"] = re.sub(regex, '', request_params["lastName"].strip())
    request_params["password"] = re.sub('[^a-zA-Z0-9 \n\.\@]', '', request_params["password"].strip()).lower()
    request_params["age"] = int(request_params["age"])
    return request_params

def error_handler(status_code,description):
    response_error = {
        'status':status_code,
        'code': 'error',
        "message": description
    }
    return make_response(jsonify(response_error),status_code)

