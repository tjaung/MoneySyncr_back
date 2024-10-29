# MoneySyncr Backend

Django app that handle authentication for the platform

## Get Started
To clone this repo copy and paste this in the terminal:
https://github.com/tjaung/MoneySyncr_back.git

Go to the directory and enter:
python3 manage.py runserver

Follow the directions and you are good to go!

There isn't much to do after that since this serves as a REST api for the [client side](https://github.com/tjaung/MoneySyncr_client).

## About

This project has to be secure since it deals with financial data. I was inspired by some youtube tutorials, but ultimately, I ended up recreating the backend on my own with Django. I wanted something that I could build quickly, yet something that was secure. The django framework has lots of out of the box security as well as other libraries to create more layers. It is also relatively beginner friendly, so this fit the criteria perfectly.

## Functions

The backend only deals with user authentication due to the timeline. I would like to come back to implement Plaid and Dwolla here, but that is a future ticket to do.
