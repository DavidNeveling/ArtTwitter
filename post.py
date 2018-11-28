# coding: cp437

import twitter, os, time, random
from twitter import *
from art import draw

def main():
    f = open('credentials.txt')
    ACCESS_TOKEN = f.readline()
    ACCESS_SECRET = f.readline()
    CONSUMER_KEY = f.readline()
    CONSUMER_SECRET = f.readline()

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = Twitter(
        auth=oauth)

    t_upload = Twitter(domain='upload.twitter.com',
        auth=oauth)

    draw()
    while True:
        with open("dickbutt.png", "rb") as imagefile:
            imagedata = imagefile.read()
        id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
        t.statuses.update(status="", media_ids=",".join([id_img1]))
        print "POSTED"
        turn = random.random()
        if turn > .5:
            turn = True
        draw(rotate=turn)
        time.sleep(10)
        # time.sleep(60 * 60 * 24)

if __name__ == "__main__":
    main()
