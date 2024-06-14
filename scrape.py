"""
Scraping order of operations:

1. Could go to this url: https://www.linkedin.com/in/<user's profile-name>/recent-activity/all/ or main feed
2. Extracting post text, number of likes, number comments, number of reposts
3. POSSIBLE: up to separate likes modal to separate them further to adjust scoring
4. POSSIBLE: open up posts and extract comments to gather post sentiment (might be redundant because no one has the guts to talk trash on a LinkedIn post)
"""
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re

# Load .env variables
load_dotenv()

driver = webdriver.Chrome()

linkedin_username = os.getenv('LINKEDIN_USERNAME')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')

linkedin_login_url = 'https://www.linkedin.com/login'

posts_url = os.getenv('POSTS_URL')

def login_to_linkedin(driver, username, password):
  driver.get(linkedin_login_url)
  time.sleep(2)
  driver.find_element(By.ID, 'username').send_keys(username)
  driver.find_element(By.ID, 'password').send_keys(password)
  driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
  time.sleep(3)

def scrape_linkedin_posts(driver, url):
  driver.get(url)
  time.sleep(2)

  page_source = driver.page_source
  soup = BeautifulSoup(page_source, 'html.parser')
  posts = soup.find_all('div', {'id': 'fie-impression-container'})

  # Parse through all of the posts found on the page that have loaded
  for post in posts:
    post_content = post.find('div', {'class': 'update-components-text relative update-components-update-v2__commentary'})
    
    # Extract the text from the post
    post_content_text = post_content.find('span', {'dir': 'ltr'}).text
    
    # Extract social interactions in total
    post_social_interaction_count = post.find('span', {'class': 'social-details-social-counts__reactions-count'}).text
    
    # Extract number of comments
    post_social_interaction_comments = str(post.select_one('button[aria-label*=comment]'))
    if post_social_interaction_comments:
      comment_count_group = re.search(r'\d+', post_social_interaction_comments)
      if(comment_count_group):
        comment_count = comment_count_group.group(0)
        print(comment_count)
      else: 
        print('No comments')
    
    # Extract number of reposts
    post_social_interaction_reposts = str(post.select_one('button[aria-label*=repost]'))
    if(post_social_interaction_reposts):
      repost_count_group = re.search(r'\d+', post_social_interaction_reposts)
      if(repost_count_group):
        repost_count = repost_count_group.group(0)
        print(repost_count)
      else:
        print('No reposts')
    
    print('---------------------')

login_to_linkedin(driver, linkedin_username, linkedin_password)
scrape_linkedin_posts(driver, posts_url)

driver.quit()