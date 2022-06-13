import os, json
import requests

host = os.getenv("FLASK_HOST")
port = os.getenv("FLASK_PORT")

signin_url = "%s:%s/logon" % (host,str(port))

def test_login_users():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"luis.delossantos@pruebas.com",
        "password":"testing01"
    }
    resp = session.post(signin_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 200
    assert "token" in resp.json()["data"]
    assert len(resp.json()["data"]["token"]) > 0
    session.close()

def test_nonexistent_user():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"antonio@outlook.com",
        "password":"contraseña"
    }
    resp = session.post(signin_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 401
    assert resp.json()["message"] == "Correo electrónico o contraseña inválidos"
    session.close()

def test_wrong_password():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"antonio.cota@outlook.com",
        "password":"pass"
    }
    resp = session.post(signin_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 401
    assert resp.json()["message"] == "Correo electrónico o contraseña inválidos"
    session.close()

def test_empty_password():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"antonio.cota@outlook.com",
        "password":""
    }
    resp = session.post(signin_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 404
    assert resp.json()["message"] == "Parámetros incorrectos"
    session.close()