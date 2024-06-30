import os
from dotenv import load_dotenv
from peewee import *

load_dotenv()

db_name = os.getenv('DB_NAME')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

db = PostgresqlDatabase(
  db_name,
  user = db_username,
  password = db_password,
  host = db_host,
  port = db_port 
)