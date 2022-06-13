import os, json
import requests

host = "http://127.0.0.1"
port = 5000

signup_url = "%s:%s/signup" % (host,str(port))

"""
host = os.getenv("FLASK_HOST")
port = os.getenv("FLASK_PORT")
"""

def test_create_users():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"antonio.cota@outlook.com",
        "firstName":"Antonio   ",
        "lastName":"Cota",
        "age": 29,
        "password":"contra@1"
    }
    resp = session.post(signup_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 201
    assert resp.json()["data"] == "El usuario fue creado con éxito"
    session.close()

def test_empty_users():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {}
    resp = session.post(signup_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 404
    assert resp.json()["message"] == "Parámetros incorrectos"
    session.close()

def test_incomplete_users():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "firstName":"Antonio   ",
        "lastName":"Cota",
        "age": 29,
        "password":"contra@1"
    }
    resp = session.post(signup_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 404
    assert resp.json()["message"] == "Parámetros incorrectos"
    session.close()

def test_capital_letter():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"MARCOANTONIO@outlook.com",
        "firstName":"SOLIS",
        "lastName":"Cota",
        "age": 60,
        "password":"PASSPORT09"
    }
    resp = session.post(signup_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 201
    assert resp.json()["data"] == "El usuario fue creado con éxito"
    session.close()

def test_duplicate_users():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"antonio.cota@outlook.com",
        "firstName":"Antonio   ",
        "lastName":"Cota",
        "age": 29,
        "password":"contra@1"
    }
    resp = session.post(signup_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 404
    assert resp.json()["message"] == "El correo ya se encuentra en uso"
    session.close()

def test_wrong_users():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"antonio.cotaoutlookcom",
        "firstName":"Antonio   ",
        "lastName":"Cota",
        "age": 29,
        "password":"contra@1"
    }
    resp = session.post(signup_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 404
    assert resp.json()["message"] == "Formato de correo no válido"

    session.close()

def test_decimal_age():
    session = requests.Session()
    header = {
        "Content-Type" : "application/json"
    }
    data = {
        "email":"luis.delossantos@pruebas.com",
        "firstName":"Luis",
        "lastName":"de los Santos",
        "age": 27.7,
        "password":"testing01"
    }
    resp = session.post(signup_url,headers=header,data=json.dumps(data))
    assert resp.status_code == 201
    assert resp.json()["data"] == "El usuario fue creado con éxito"
    session.close()