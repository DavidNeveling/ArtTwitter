# coding: cp437

import twitter, os, time
from twitter import *
from art import draw

def main():

    t = Twitter(
        auth=OAuth('1015751543180660736-jtRIfHGZdbIh9HhBFAB9llWMAwxfb2', 'Twb6mXIuHzC0G2uqP5gp7Xtu2WGl6AnsR4cYlYFcM2VFj', '5oTNOTG0OqTqhfsFoiDbcSEER', 'hr3IFGcH6OerA6iVftFqoYSFUA703kMa9mJTOcI2XAUdxClnv2'))

    t_upload = Twitter(domain='upload.twitter.com',
        auth=OAuth('1015751543180660736-jtRIfHGZdbIh9HhBFAB9llWMAwxfb2', 'Twb6mXIuHzC0G2uqP5gp7Xtu2WGl6AnsR4cYlYFcM2VFj', '5oTNOTG0OqTqhfsFoiDbcSEER', 'hr3IFGcH6OerA6iVftFqoYSFUA703kMa9mJTOcI2XAUdxClnv2'))

    while True:
        draw()
        with open("dickbutt.png", "rb") as imagefile:
            imagedata = imagefile.read()
        id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]
        t.statuses.update(status="", media_ids=",".join([id_img1]))
        # time.sleep(60 * 60 * 24)
        time.sleep(10)

if __name__ == "__main__":
    main()
