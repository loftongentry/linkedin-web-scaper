"""
TODO: Export database
TODO: Create model for linkedIn post entries and export that as well
"""
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

class BaseModel(Model):
  class Meta:
    database = db

class TempModel(BaseModel):
  name = CharField()

def test_db_connection():
  try:
    db.connect()
    print('Connected to database')

    if db.is_closed():
      print('Connection to database is closed')
    else:
      print('Connection to database is open')

    db.create_tables([TempModel])
    print('Temp table created succesfully')

    TempModel.create(name='Test Name')
    print('Record inserted into temp table succesfully')

    query = TempModel.select().where(TempModel.name == 'Test Name')

    if query.exists():
      print('Record found in table')
      for record in query:
        print('Record:', record.name)
    else:
      print('Record not found in table')

  except Exception as e:
    print('Failed to connect to database to perform operation')
    print('Error:', e)
  
  finally:
    db.drop_tables([TempModel])
    print('Temp table dropped')
    if not db.is_closed():
      db.close()
      print('Closed connection to database')

test_db_connection()