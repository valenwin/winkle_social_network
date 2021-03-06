# Winkle Social Network

## Overview
#### Django3, PostgreSQL

Basic models:<br />

- `CustomUser` (sign in / signup)<br />
    - Registration by using **django-registration**
    - Registration by using **social-auth-app-django** 
        - Sign in with Facebook
        - Sign in with Google
    - Login, Logout by using **django.contrib.auth**
    - Change, Reset password (sent confirmation email) by using **django.contrib.auth**
    - Used **hunter.io** for verifying email existence on signup
    - Used **clearbit.com** for getting additional data for the user on signup (user's first and last name)
    
- `Profile` (storing additional user information)<br />
    - Used **django signals** for creation profile instance while user registered
    - Used **Pillow** library for saving profile image

- `Image` (create, view list (user's dashboard) and details of each image)
    - `CRUD` operations
    - `Like vs Unlike` for image using **AJAX requests plus jQuery**
- `Comment` (image comments for registered users)
- `Contact` (base for user subscription system (following/followers) by using **AJAX handler**) 
- `Action`:
    - user added the picture to bookmarks;
    - user liked the image;
    - user created an account;
    - user subscribed to updates.

Other functionality:<br />
- jQuery `Bookmark image` button (move button to your browser Bookmarks Bar and tap on it every time you want to bookmark some photo or image)

- `Redis`
    - for image view counter 
    - for image ranking (rating of 10 most viewed images)

## Deploy project on your local machine

1 - To deploy project on your local machine create new virtual environment and execute this command:

`pip install -r requirements.txt`

2 - Insert your own db configuration settings (see example.env):
and change file name to .env:

`SECRET_KEY`,

`DB_PASSWORD`,
`DB_NAME`,
`DB_USER`

`EMAIL_HOST_USER`,
`EMAIL_HOST_PASSWORD`

3 - Migrate db models to PostgreSQL:

`python3 manage.py migrate`

4 - **Ngrok** for hostname creation:

`https://ngrok.com/download` and run `./ngrok http 8000` <br />
or `brew cask install ngrok` and run `ngrok http 8000` <br />
copy `Forwarding address` instead data in next files: <br />
1. settings.py => ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1', '`Forwarding address`'] <br />
2. static/js/bookmarklet.js => const site_url = '\'https://`Forwarding address`\''; <br />
3. templates/images/bookmarklet_launcher.js => 'https://`Forwarding address`/static/js/bookmarklet.js?r='

5 - Run Redis server: `redis-server`
    
6 - Load data from JSON files:

7 - Run app:

`python3 manage.py runserver`
