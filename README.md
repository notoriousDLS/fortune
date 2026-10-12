# Fortune Teller (Zodi-app) Version 1. 

A digital fortune teller, built for a friend who loves the Zodiac. Enter your date of birth and Michael the Magnificent shares your horoscope for the day.

It's a small Flask app with a SQLite DB, lives on Railway.

## Stack

- Python 3.13 + Flask
- SQLite for storage
- Hosted on Railway (moved over from PythonAnywhere)

## Project layout

The app borrows from the Flaskr Quickstart.

```
fortune/
├── main.py           # Flask app entry point
├── auth.py           # Very login and registration
├── blog.py           # Very simple blog, untouched.
├── db.py             # Database connection and helpers
├── schema.sql        # SQLite schema
├── __init__.py
├── requirements.txt
├── templates/
└── static/
```

## Running it locally

```
git clone https://github.com/notoriousDLS/fortune.git
cd fortune
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set up the database (first run only):

```
flask --app main init-db
```

Then start the dev server:

```
flask --app main run --debug
```

A few things that bit me getting this live:

- Deployment, which is normally fine was a bit of  a disaster, hence 12 deployments. `gunicorn` has to be in `requirements.txt`, or Railway won't pick it as the server.
- Leave Custom Build Command empty in Railway or it conflicts with the Railway Starter Package Default. If gunicorn ends up in the build step, the build fails with exit code 3.
- Railway sets `PORT` itself and gunicorn reads it, so no `--bind` needed.
- Railway's filesystem resets on every deploy. The SQLite file needs to sit on a mounted drive volume, or every user account disappears. Not such a bad thing. I do not intend to keep the data. 

## Errors

- The app has instructions to mention a lucky number. I noticed when using it frequently it tends to default to 47. Investigate. 

## What's next 

#### General Application

- Finish the login feature so fortunes can be saved per user
- Add authentication features to detect emails and stricter password rules. 
- remove unused paths and features
- Improve the design, perhaps with Claude once I strong concept is established. I put all the design effort in to mrdls.fyi 
- Add account controls, limit to 1 horoscope per day.


#### Add new features 

- Perhaps a tarot card reading game using messages API 

