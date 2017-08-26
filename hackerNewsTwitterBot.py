import datetime
import tweepy
import os
from hackernews import HackerNews
from selenium import webdriver
from PIL import Image
from io import BytesIO

# Personalized Twitter API keys generated for Tweepy use; insert your own
# Using .env file access through Heroku environment variables
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# Instantiate Tweepy client with keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Screenshots Hacker News posts and uploads to Twitter as banner
def refresh_banner():
	# Using Selenium and PhantomJS browser to screenshot Hacker News posts
	# phantomJS_path = 'C:\\Python\\selenium\\webdriver\\phantomjs\\phantomjs.exe' LOCAL USE ONLY
	driver = webdriver.PhantomJS()
	driver.set_window_size(1600, 900)
	driver.get('https://news.ycombinator.com')
	img = driver.get_screenshot_as_png()  # Save screenshot as binary data

	# Find element on page with posts and get element pixel location on page
	element = driver.find_element_by_tag_name('tbody')
	location = element.location
	size = element.size
	driver.quit()

	# Load screenshotted image from memory and crop for upload
	img = Image.open(BytesIO(img))
	left = location['x']
	upper = location['y']
	right = location['x'] + size['width']
	lower = size['height'] - 772  # Format for Twitter's autocrop
	img = img.crop((left, upper, right, lower))  # Crop at defined points
	img.save('screenshot.png')  # Saves cropped image
	api.update_profile_banner('screenshot.png')  # Uploads cropped banner

# Tweets top 10 stories on Hacker News with no duplicates
def refresh_posts():
	hn = HackerNews()
	for story in hn.top_stories(limit=10):  # Only viewing top 10 posts on HN
		story_id = hn.get_item(story)

		# Ignores post if posted over 4 hour ago (to avoid duplicate tweets)
		current_time = datetime.datetime.now()
		story_time = story_id.submission_time
		delta = current_time - story_time
		# Chng. if bot runs per x hours
		if delta > datetime.timedelta(hours=4):
			continue
		else:  # If younger than 4 hour: Tweets title, story URL, and comments
			story_title = (story_id.title + '\n')
			story_url = ('Link: ' + story_id.url + '\n')
			story_comments = ('Comments: https://news.ycombinator.com/item?id=%s' %
							  str(story_id.item_id))
			api.update_status(story_title + story_url + story_comments)

def main():
	refresh_banner()  # Refresh banner on Twitter page
	refresh_posts()  # Tweet new posts on Twitter page

if __name__ == '__main__':
	main()

