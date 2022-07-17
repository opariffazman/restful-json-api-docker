# Pre-Requisites

[Docker Desktop](https://docs.docker.com/desktop/)
- To deploy the containers used for this api

[Postman](https://www.postman.com/downloads/)
- To utilize the json collection for calls to the api endpoints

# Getting Started

Clone this [repo](https://github.com/opariffazman/restful-json-api-docker.git) if you have git installed or `Code` > `Download Zip`

![download-zip](docs/download-zip.png)

And extract its content

# Deployment

For ease of deployment, we will make use of the `Dockerfile` and `docker-compose.yml`

For reference only (already included when build):
## Dockerfile

- [Python 3.10-Slim](https://hub.docker.com/_/python)

- [Postgres 14](https://hub.docker.com/_/postgres)

## Pip requirements

- [flask](https://flask.palletsprojects.com/en/2.1.x/) - Application Framework

- [flask sql alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Simplify SQL Usage

- [psycopg](https://www.psycopg.org/docs/install.html) - PostgreSQL adapter

- [Werkzeug](https://werkzeug.palletsprojects.com/en/2.1.x/installation/) - Password Hashing

- [pyjwt](https://pyjwt.readthedocs.io/en/stable/) - JWT Implementation

## Docker Commands

Open a PowerShell session inside the root folder of this repository.

Run this command to start deploying the API container
```powershell
docker compose up --build api
```

Once the shell is reporting that the api is running like below
```powershell
api  |  * Running on http://127.0.0.1:5000
api  |  * Running on http://172.24.0.3:5000 (Press CTRL+C to quit)
```

Or you could verify on the `Docker Desktop` application > `Containers` as below

![docker-desktop](docs/docker-desktop.png)

# API Usage

Open `Postman` and import the json by navigating to `Import` > `Link` > `Enter a URL` > `https://www.getpostman.com/collections/37c6351577b1f3e9d8d2`

![postman-import](docs/postman-import.png)
___
## create-admin

| INFO   |  |
| -------- | -------- |
| METHOD   | POST |
| ENDPOINT | http://localhost:5000/api/v1/admins |
| TOKEN    | none |

Provide a name & password > `Send`

![create-admin](docs/create-admin.png)
___
## admin-auth

| INFO   |  |
| -------- | -------- |
| METHOD   | GET |
| ENDPOINT | http://localhost:5000/api/v1/admins/auth |
| TOKEN    | none |

Use the same name & password you've created earlier > `Send`

![admin-auth](docs/admin-auth.png)

You will get a token in response in such format, copy the token as below (valid for 2 minutes)

![admin-token](docs/admin-token.png)

Endpoint with Token: `required` will need to be supplied with this token as key for `x-access-token` on the `Headers` for example

![create-customer-1](docs/create-customer-1.png)
___
## create-customer

| INFO   |  |
| -------- | -------- |
| METHOD   | POST |
| ENDPOINT | http://localhost:5000/api/v1/customers |
| TOKEN    | required |

This endpoint will add new customer with values of `name` & `dob` (date of birth)

![create-customer-2](docs/create-customer-2.png)
___
## get-customers

| INFO   |  |
| -------- | -------- |
| METHOD   | GET |
| ENDPOINT | http://localhost:5000/api/v1/customers/all |
| TOKEN    | required |

This endpoint will list all the customers in the table

![get-customers](docs/get-customers.png)
___
## get-customers-size

| INFO   |  |
| -------- | -------- |
| METHOD   | GET |
| ENDPOINT | http://localhost:5000/api/v1/customers?size={{customer_size}} |
| TOKEN    | required |

This endpoint will get the list of customer according to given size ordered by youngest age

![get-customers-size](docs/get-customers-size.png)
___
## get-customer

| INFO   |  |
| -------- | -------- |
| METHOD   | GET |
| ENDPOINT | http://localhost:5000/api/v1/customer?id={{customer_id}} |
| TOKEN    | required |

This endpoint will get a specific customer with id given

![get-customer](docs/get-customer.png)
___
## update-customer

| INFO   |  |
| -------- | -------- |
| METHOD   | PUT |
| ENDPOINT | http://localhost:5000/api/v1/customer?id={{customer_id}} |
| TOKEN    | required |

This endpoint will update the record of a specific customer with id given

![get-customer](docs/get-customer.png)
___
## delete-customer

| INFO   |  |
| -------- | -------- |
| METHOD   | DELETE |
| ENDPOINT | http://localhost:5000/api/v1/customer?id={{customer_id}} |
| TOKEN    | required |


This endpoint will update the record of a specific customer with id given

![delete-customer](docs/delete-customer.png)
