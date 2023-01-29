from moviepy.editor import *
from PIL import Image, ImageOps
from gtts import gTTS
import sqlite3

# crop image
TIKTOK_WIDTH = 1080
TIKTOK_HEIGHT = 1920

IDEAL_WIDTH = 2250
CUT_FROM_EACH_SIDE = 1875
TOTAL_PICS = 306

#
# def init_db_conn():
#     return sqlite3.connect("cheezit.db")
#
#
# def get_untweeted_file_name(db_cur):
#     photo_names = os.listdir("./photos")
#     db_cur.execute(
#         """
#         SELECT file_name from tik_toks
#         """,
#     )
#     already_tweeted = db_cur.fetchall()
#     for photo_name in photo_names:
#         if photo_name not in already_tweeted:
#             return photo_name
#     raise "Cannot find untweeted photo."


def crop_image_to_ideal_size(file_name):
    im = Image.open(file_name)
    # im = im.crop((1875, 4000, 6000 - 1875, 0))
    border = (1875, 0, 1875, 0)
    ImageOps.crop(im, border).save("cropped.JPG")
    return "cropped.JPG"
    # cropped_file = "cropped.JPG"
    # im.save(cropped_file)
    # return cropped_file


def generate_audio(index):
    tts_string = f"Day {index} of posting a picture of every cheez it in this box."
    tts = gTTS(tts_string)
    tts.save('tts.mp3')
    return "tts.mp3"


# def record_file_as_uploaded(db_cur, db_conn, file_name):
#     db_cur.execute(
#         """
#         INSERT INTO tik_tok_uploads (file_name, tweet_url, occurred_at) VALUES
#         (%s, %s, CURRENT_TIMESTAMP)
#         """, [file_name, tweet_url])
#     db_conn.commit()


# def get_untweeted_file_name(db_cur):
#     photo_names = os.listdir("./photos")
#     db_cur.execute(
#         """
#         SELECT file_name from tweets
#         """,
#     )
#     already_tweeted = db_cur.fetchall()
#     for photo_name in photo_names:
#         if photo_name not in already_tweeted:
#             return photo_name
#     raise "Cannot find untweeted photo."


def main():
    # db_conn = init_db_conn()
    # db_cur = db_conn.cursor()
    file_name = "IMG_1039.JPG"
    audio_file_name = generate_audio(1)
    cropped_image = crop_image_to_ideal_size(file_name)
    image_clip = ImageClip(cropped_image, duration=5)
    image_clip.audio = AudioFileClip(audio_file_name)

    # txt_clip = TextClip(f"Day 1 of posting a picture of every cheez it in this box.", fontsize=175, bg_color="white",
    #                     font='Courier-BoldOblique', color='black', method='caption', size=(1850, None))

    # setting position of text in the center and duration will be 10 seconds
    # txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(3)

    # Overlay the text clip on the first video clip
    # video = CompositeVideoClip([image_clip, txt_clip])
    # image_clip.set_duration('00:00:04.35')
    image_clip.write_videofile('current.mp4', fps=60)
    image_clip.close


if __name__ == "__main__":
    main()
