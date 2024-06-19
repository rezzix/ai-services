# Introduction 
Set of general utility services, mainly REST APIs

# Getting Started
The services are python scripts using OpenAPI specification

1.	Installation process

works with python 3.11 +

2.	Software dependencies

Flask numpy pandas openai gunicorn apiflask python-dotenv pyodbc

3.	Latest releases

# Build and Test

can be run using gunicorn :
gunicorn -t 60 -w 4 -b 0.0.0.0:8000 main:app
