import tweepy
import os
from hackernews import HackerNews
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
	# Using Selenium and Chrome Headless browser to screenshot Hacker News posts
	chrome_options = Options()
	chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_SHIM', None)
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--window-size=1400, 900')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-extensions')
	driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
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
	lower = size['height'] - 800  # Format for Twitter's autocrop
	img = img.crop((left, upper, right, lower))  # Crop at defined points
	img.save('screenshot.png')  # Saves cropped image
	api.update_profile_banner('screenshot.png')  # Uploads cropped banner

# Tweets top 10 stories on Hacker News with no duplicates on Twitter feed
def refresh_posts():
	hn = HackerNews()
	for story in hn.top_stories(limit=10):  # Only viewing top 10 posts on HN
		story_id = hn.get_item(story)

		#  Tweets title, story URL, and comments
		if len(story_id.title) > 76:  # Adjusting for max tweet length
			story_title = (story_id.title.rsplit(' ', 1)[0] + '\n')
		else:
			story_title = (story_id.title + '\n')

		story_comments = ('Cmts: https://news.ycombinator.com/item?id=%s' %
						  str(story_id.item_id))

		#  Check to see if post has an external link
		if story_id.url is None:
			try: # If tweet is a duplicate, ignores the post and doesn't tweet
				api.update_status(story_title + story_comments)
			except tweepy.error.TweepError:
				continue
		else:
			story_url = ('Link: ' + story_id.url + '\n')
			# If tweet is a duplicate, ignores the post and doesn't tweet
			try:
				api.update_status(story_title + story_url + story_comments)
			except tweepy.error.TweepError:
				continue


def main():
	refresh_banner()  # Refresh banner on Twitter page
	refresh_posts()  # Tweet new posts on Twitter page


if __name__ == '__main__':
	main()
