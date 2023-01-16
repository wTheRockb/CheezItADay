import tweepy
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

## Constants
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET")
FILE_SIZE_LIMIT = 5242880
DEBUG_MODE = False


def get_untweeted_file_name(db_cur):
    photo_names = os.listdir("./photos")
    db_cur.execute(
        """
        SELECT file_name from tweets 
        """,
    )
    already_tweeted = db_cur.fetchall()
    for photo_name in photo_names:
        if photo_name not in already_tweeted:
            return photo_name
    raise "Cannot find untweeted photo."


def save_file_as_tweeted(db_cur, db_conn, file_name, tweet_url):
    db_cur.execute(
        """
        INSERT INTO tweets (file_name, tweet_url, occurred_at) VALUES
        (%s, %s, CURRENT_TIMESTAMP)
        """, [file_name, tweet_url])
    db_conn.commit()


def tweet_new_photo(db_cur, db_conn, file_name):
    auth = tweepy.OAuthHandler(
        os.environ['API_KEY'],
        os.environ['API_SECRET']
    )
    auth.set_access_token(
        os.environ['ACCESS_TOKEN'],
        os.environ['ACCESS_SECRET']
    )
    api = tweepy.API(auth)

    # Upload image
    media = api.media_upload(file_name)

    # Post tweet with image
    post_result = api.update_status(status=file_name, media_ids=[media.media_id])
    tweet_url = post_result.id
    save_file_as_tweeted(db_cur, db_conn, file_name, tweet_url)


def init_db_conn():
    return sqlite3.connect("cheezit.db")


def main():
    db_conn = init_db_conn()
    db_cur = db_conn.cursor()
    file_name = get_untweeted_file_name(db_cur)
    tweet_new_photo(db_cur, db_conn, file_name)


if __name__ == "__main__":
    main()
