# Winkle Social Network

## Overview
#### Django3, PostgreSQL

Basic models:<br />
- User (sign in / signup)<br />
    - Registration by using **django-registration**
    - Login, Logout by using **django.contrib.auth**
    - Change, Reset password by using **django.contrib.auth**
    - Used **hunter.io** for verifying email existence on signup
    - Used **clearbit.com** for getting additional data for the user on signup (user's first and last name)
- Profile (storing additional user information)<br />
    - Used **django signals** for creation profile instance while user registered
    - Used **Pillow** library for saving profile image
 