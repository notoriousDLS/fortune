from datetime import date
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from flask import Blueprint, Response, request, stream_with_context

load_dotenv(Path(__file__).resolve().parent / ".env")

bp = Blueprint("fortune", __name__, url_prefix="/fortune")

# uses ANTHROPIC_API_KEY (loaded from .env above) or credentials from `ant auth login`
client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a wizard with the power of sight and clairvoyance.
You speak in a mysterious and direct tone of voice. 
You do not use stage direction, closed captions or descriptive inputs. You speak through this website. For example you would never say something like *A distant, knowing voice emerges from the mists of time* and begin speaking. 
You create horoscopes that follow a structured pattern. You tell your horoscopes with a short introduction and  then a paragraph each for 4 categories. Love, Family, Career and Self.
You will seperate each category with a title <h2> tag followed by a paragraph on a new line.  You will add breaks between each paragraph. You are very particular when it comes to 
When you finish a horoscope you will tell the requester that your powers grow weary and to return on the morrow. You can alter this message but the sentiment is always the same.
You must respond and be completely gender neutral.
You will generate a random number and use it in the story, you may also simply state that a person lucky number is something between 1 and 100."""

# Reference-year (2000, a leap year) MM-DD ranges for each sign. Capricorn
# wraps across the year boundary, so it gets two ranges.
ZODIAC_DATE_RANGES = {
    "Capricorn": [("2000-01-01", "2000-01-19"), ("2000-12-22", "2000-12-31")],
    "Aquarius": [("2000-01-20", "2000-02-18")],
    "Pisces": [("2000-02-19", "2000-03-20")],
    "Aries": [("2000-03-21", "2000-04-19")],
    "Taurus": [("2000-04-20", "2000-05-20")],
    "Gemini": [("2000-05-21", "2000-06-20")],
    "Cancer": [("2000-06-21", "2000-07-22")],
    "Leo": [("2000-07-23", "2000-08-22")],
    "Virgo": [("2000-08-23", "2000-09-22")],
    "Libra": [("2000-09-23", "2000-10-22")],
    "Scorpio": [("2000-10-23", "2000-11-21")],
    "Sagittarius": [("2000-11-22", "2000-12-21")],
}


def get_zodiac_sign(dob):
    """Look up the zodiac sign for a date.fromisoformat-parsed date of birth."""
    month_day = (dob.month, dob.day)
    for sign, ranges in ZODIAC_DATE_RANGES.items():
        for start_str, end_str in ranges:
            start = date.fromisoformat(start_str)
            end = date.fromisoformat(end_str)
            if (start.month, start.day) <= month_day <= (end.month, end.day):
                return sign
    raise ValueError(f"no zodiac sign matches {dob.isoformat()}")


def build_user_message(dob, sign):
    return f"My date of birth is {dob.isoformat()}. I am a {sign}. Tell me my horoscope for today."


@bp.route("/see", methods=["POST"])
def see_future():
    payload = request.get_json(silent=True) or request.form
    dob_str = (payload or {}).get("dob", "")

    try:
        dob = date.fromisoformat(dob_str)
    except (TypeError, ValueError):
        return {"error": "Please provide a valid date of birth (YYYY-MM-DD)."}, 400

    sign = get_zodiac_sign(dob)
    message = build_user_message(dob, sign)

    def generate():
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    return Response(stream_with_context(generate()), mimetype="text/html")
