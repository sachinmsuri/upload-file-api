Upload File API
===

## Overview

Flask REST API developed using Flask Rest-X to allow users to upload files and retrive infromation about files stored on the webserver. All files uploaded by users are stored within the uploads directory. Swagger documentation can be found on local host.


## Installation

Install requriments for project
```bash
pip install -r requirements.txt
```

Create SECRET_KEY and add to .env file
```bash
import secrets

secrets.token_hex()
```

Run flask shell and create database
```bash
flask shell

db.create_all()
```

Run flask shell and create database
```bash
flask shell

db.create_all()
```

Run Flask Application
```bash
python app.py
```








