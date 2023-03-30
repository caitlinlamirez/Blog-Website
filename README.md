# How Was Your Day
"How Was Your Day" is a social media app built with Django that allows users to post about their day and give their day a rating. Users can create an account, log in, and start sharing their daily experiences with friends and followers.

## Features
User authentication: Users can create an account and log in to the app.

Account management: Users can edit their account information, such as their name and profile picture.

Posting: Users can create posts and share their daily experiences with others.

Ratings: Users can rate their day on a scale from 1 to 5. 

Feed: Users can see posts from either their followers or other users on the website. 

Search: Users can search for other users and posts.

Follow: Users can follow other users and see their posts in their feed.

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/caitlinlamirez/Blog-Website.git
$ cd Blog-Website
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd blog_project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`

## Usage
Once you've installed the app, you can create an account, log in, and start sharing your daily experiences with others. You can also search for other users, follow them, and see their posts in your feed. Don't forget to rate your day on a scale from 1 to 5!
