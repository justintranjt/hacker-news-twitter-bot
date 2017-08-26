# HackerNewsTwitterBot
This Python script aims to compile the Top 10 posts from news.ycombinator.com (Hacker News) and posts the title, link to the story, and  link to the comments section for each post every 4 hours (as managed by the [APScheduler library](https://apscheduler.readthedocs.io/en/latest/)). In addition, the Twitter page features a banner with a screenshot of the news.ycombinator.com frontpage that updates every 4 hours as well.

The project is hosted on a Heroku server and utilizes [Tweepy](https://github.com/tweepy/tweepy) to make the tweets and update the banner. [Haxor](https://github.com/avinassh/haxor) was used to access the Hacker News API without having to deal with pesky JSON files. [Selenium](http://www.seleniumhq.org/) and [Pillow](https://github.com/python-pillow/Pillow) allowed for screenshotting and image manipulation while [PhantomJS](http://phantomjs.org/) was used as the headless browser accessing the Hacker News front page.

The Twitter page is @HackerPostsBot or https://twitter.com/HackerPostsBot
