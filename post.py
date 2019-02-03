# coding: cp437

import twitter, os, time, random
from twitter import *
from art import draw, imageSearchArt

def main():
    f = open('credentials.txt')
    ACCESS_TOKEN = f.readline()[:-1]
    ACCESS_SECRET = f.readline()[:-1]
    CONSUMER_KEY = f.readline()[:-1]
    CONSUMER_SECRET = f.readline()[:-1]

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = Twitter(
        auth=oauth)

    t_upload = Twitter(domain='upload.twitter.com',
        auth=oauth)

    whichArt = random.random()
    if whichArt > .5:
        draw()
    else:
        imageSearchArt()
    while True:
        with open("uncomfortablyLongFart.png", "rb") as imagefile:
            imagedata = imagefile.read()
        id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
        t.statuses.update(status="", media_ids=",".join([id_img1]))
        print "POSTED"
        whichArt = random.random()
        if whichArt > .5:
            turn = random.random()
            if turn > .5:
                turn = True
            draw(rotate=turn)
        else:
            imageSearchArt()

        time.sleep(time.time() % (60 * 60 * 24))

if __name__ == "__main__":
    main()
