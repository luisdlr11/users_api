from flask import Blueprint, make_response, jsonify, request
from connections import ConnectionMongo
import hashlib, os, re

mongo_connection = ConnectionMongo().mongo_connect()
data_base = mongo_connection["users"]
user_collection = data_base["data_user"]

logon = Blueprint('logon',__name__)
@logon.route("/logon", methods=['POST'])
def log_on():
    params = request.json
    return validator(params)

def validator(request_params):
    no_params_copy = "Parámetros incorrectos"
    invalid_mail_copy = "Formato de correo no válido"
    require_params = ["email","password"]
    if bool(request_params):
        if all(key in request_params for key in (require_params)):
            for item in request_params.values():
                if not item:
                    print("no value", item)
                    return error_handler(404,no_params_copy)

            request_params = clean_params(request_params)
            if not valid_email(request_params["email"]):
                return error_handler(404, invalid_mail_copy)
            return login_users(request_params)
        else:
            return error_handler(404,no_params_copy)
    else:
        return error_handler(404,no_params_copy)

def login_users(request_params):
    unauthorized_copy = "Correo electrónico o contraseña inválidos"
    db_error_copy = "Error en base de datos"
    try:
        password = hashlib.sha512((request_params["password"] + os.getenv("SALT")).encode('utf-8')).hexdigest()
        find_user = user_collection.find_one({"email":request_params["email"]})
        if not find_user:
            return error_handler(401,unauthorized_copy)
        if find_user["password"] == password:
            response = {
                'status':200,
                'code': 'success',
                "data": {
                    "token": find_user["token"]
                }
            }
            return make_response(jsonify(response),200) 
        else:
            return error_handler(401,unauthorized_copy)
    except Exception as exception:
        print(exception)
        return error_handler(404, db_error_copy)

    

def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not (re.fullmatch(regex, email)):
        return False
    return True

def clean_params(request_params):
    request_params["email"] = re.sub('[^a-zA-Z0-9 \n\.\@]', '', request_params["email"].strip()).lower()
    request_params["password"] = re.sub('[^a-zA-Z0-9 \n\.\@]', '', request_params["password"].strip()).lower()
    return request_params

def error_handler(status_code,description):
    response_error = {
        'status':status_code,
        'code': 'error',
        "message": description
    }
    return make_response(jsonify(response_error),status_code)
