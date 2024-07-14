"""
Currently: Extracting post text, number of likes, number comments, number of reposts
TODO: Check to make sure content is available to be extracted (within the post of posts for loop)
TODO: Create a CRON job to do this automatically
"""
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
from db.db_config import db
from models.linkedin_post import LinkedInPost

# Load .env variables
load_dotenv()

driver = webdriver.Chrome()

linkedin_username = os.getenv('LINKEDIN_USERNAME')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')
linkedin_login_url = 'https://www.linkedin.com/login'

# Logging into LinkedIn
def login_to_linkedin(driver, username, password):
  try:
    driver.get(linkedin_login_url)
    time.sleep(2)
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    time.sleep(3)
  except Exception as e:
    print('Error logging into LinkedIn:', e)

def scrape_linkedin_posts(driver):
  time.sleep(2)

  # REGEX expression to extract the UUID of the post
  pattern = re.compile(r'urn:li:activity:\d+')

  try:
    db.connect()
    print('Connected to database')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    posts = soup.find_all('div', {'data-id': pattern})
    
    # Parse through all of the posts found on the page that have loaded
    for post in posts:
      post_social_interaction_count = None
      comment_count = None
      repost_count = None
      
      # NOTE: Extracting post id as characters because Integer format was too large to be stored
      post_id = post.get('data-id')

      # Finding the actual post content we want
      post_container = post.find('div', {'id': 'fie-impression-container'})
      if post_container:
        post_content = post_container.find('div', {'class': 'update-components-text relative update-components-update-v2__commentary'})
        
        # Extract the text from the post
        post_content_text = post_content.find('span', {'dir': 'ltr'}).text
        
        # Extract social interactions in total if they exist
        post_social_interaction = post.find('span', {'class': 'social-details-social-counts__reactions-count'})
        if post_social_interaction:
          post_social_interaction_count = post_social_interaction.text

        # Extract number of comments
        post_social_interaction_comment = str(post.select_one('button[aria-label*=comment]'))
        if post_social_interaction_comment:
          comment_count_group = re.search(r'\d+', post_social_interaction_comment)
          if comment_count_group:
            comment_count = comment_count_group.group(0)
        
        # Extract number of reposts
        post_social_interaction_repost = str(post.select_one('button[aria-label*=repost]'))
        if post_social_interaction_repost:
          repost_count_group = re.search(r'\d+', post_social_interaction_repost)
          if repost_count_group:
            repost_count = repost_count_group.group(0)
        
        create_new_entry(
          post_id, 
          post_content_text, 
          post_social_interaction_count,
          comment_count,
          repost_count
        )
      else:
        print('No scraped data available to store in database')

  except Exception as e:
    print('Error gathering data from LinkedIn:', e)
  finally:
    db.close()
    print('Diconnected from database')

def create_new_entry(id, text, social_count, comment_count, repost_count):
  print('Attempting to create new entry in database')
  try:
    query = LinkedInPost.select().where(LinkedInPost.post_id == id)

    if query:
      print('Entry already exists')
      return
    else:
      # Convert counts to integers if they are valid
      try:
          social_count = int(social_count) if social_count else None
      except ValueError:
          social_count = None
      
      try:
          comment_count = int(comment_count) if comment_count else None
      except ValueError:
          comment_count = None
      
      try:
          repost_count = int(repost_count) if repost_count else None
      except ValueError:
          repost_count = None

      LinkedInPost.create(
        post_id = id,
        post_content_text = text,
        post_social_interaction_count = social_count,
        post_social_interaction_comment = comment_count,
        post_social_interaction_repost = repost_count
      )

      print('Created new entry in database')
  except Exception as e:
    print('Error occurred while creating an entry into database:', e)

login_to_linkedin(driver, linkedin_username, linkedin_password)
scrape_linkedin_posts(driver)

driver.quit()