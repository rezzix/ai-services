# Introduction 
Set of general utility services, mainly REST APIs

# Getting Started
The services are python scripts using OpenAPI specification

1.	Installation process

works with python 3.11 +

2.	Software dependencies

Flask numpy pandas openai gunicorn apiflask python-dotenv pyodbc

3.	Latest releases

4.	Create a .env file with folowing content
OPENAI_API_KEY=XXXXXXXXX
SMTP_SERVER=XXXXX
SMTP_USER=XXXXX
SMTP_PASSWORD=XXXXX


# Build and Test

can be run using gunicorn :
gunicorn -t 60 -w 4 -b 0.0.0.0:8000 main:app
