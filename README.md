# Movi users API

Users API is a service with which we can create and authenticate users 

## Installation

Install the following dependencies

```bash
pip install Flask
pip install pymongo[srv]
pip install uuid
pip install pytest
```

Or download the docker container
```bash
docker push luisdlr11/api_users:1.0.0
```

## Request

signup request
```bash
#POST
http://127.0.0.1:5000/signup
{
        "email":"prueba@correo.com",
        "firstName":"Segio",
        "lastName":"Pérez",
        "age": 32,
        "password":"redbullracing11"
}

#POST
http://127.0.0.1:5000/logon
{
        "email":"prueba@correo.com",
        "password":"redbullracing11"
}
```



## License
[MIT](https://choosealicense.com/licenses/mit/)