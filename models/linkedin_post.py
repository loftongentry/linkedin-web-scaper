from peewee import *
from db.db_config import db
import datetime

class LinkedInPost(Model):
  class Meta:
    database = db
    table_name = 'linkedin_posts'

  post_id = IntegerField(
    primary_key = True
  )
  post_content_text = TextField(
    null = False
  )
  post_social_interaction_count = IntegerField(
    null = True
  )
  post_social_interaction_comment = IntegerField(
    null = True
  )
  post_social_interaction_repost = IntegerField(
    null = True
  )
  createdAt = DateTimeField(
    default = datetime.datetime.now,
    null = False
  )
  updatedAt = DateTimeField(
    default = datetime.datetime.now,
    null = False
  )

# NOTE: Just a reminder on how to make and drop tables using peewee
def create_table():
  try:
    db.connect()
    print('Connected')
    db.drop_tables([LinkedInPost])
    db.create_tables([LinkedInPost])
  except Exception as e:
    print('Error occurred making table:', e)
  finally:
    db.close()
    print('Disconnected')

create_table()