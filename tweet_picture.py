import tweepy
import os
from dotenv import load_dotenv
import sqlite3
from PIL import Image

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


def compress_file(file_name):
    img = Image.open(f"photos/{file_name}")
    img.save("photos/current.JPG", optimize=True, quality=91)
    return "current.JPG"


def tweet_new_photo(db_cur, db_conn, compressed_file_name, file_name):
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
    media = api.media_upload(f"photos/{compressed_file_name}")

    # Post tweet with image
    post_result = api.update_status(status=file_name, media_ids=[media.media_id])

    return post_result.id


def save_file_as_tweeted(db_cur, db_conn, file_name, tweet_url):
    db_cur.execute(
        """
        INSERT INTO tweets (file_name, tweet_url, occurred_at) VALUES
        (%s, %s, CURRENT_TIMESTAMP)
        """, [file_name, tweet_url])
    db_conn.commit()


def init_db_conn():
    return sqlite3.connect("cheezit.db")


def main():
    db_conn = init_db_conn()
    db_cur = db_conn.cursor()
    file_name = get_untweeted_file_name(db_cur)
    compressed_file_name = compress_file(file_name)
    tweet_url = tweet_new_photo(db_cur, db_conn, compressed_file_name, file_name)
    save_file_as_tweeted(db_cur, db_conn, file_name, tweet_url)



if __name__ == "__main__":
    main()
