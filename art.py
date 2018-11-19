# coding: cp437

from PIL import Image, ImageColor, ImageDraw
# from post import t, t_upload # left unincluded because I don't want to give out my personal info

def lerpColor(color1, color2, percent):
    return (int(color1[0] + (color2[0]-color1[0]) * percent), int(color1[1] + (color2[1]-color1[1]) * percent), int(color1[2] + (color2[2]-color1[2]) * percent))

def main():
    img = Image.new('RGBA', (400, 400))
    draw = ImageDraw.Draw(img)

    color1 = (255, 128, 255)
    color2 = (0, 128, 255)

    """ # THIS WORKS (and it doesn't require the ImageDraw module)
    for r in range(400):
        color = lerpColor(color1, color2, (1.0/400)*r)
        for c in range(400):
            img.putpixel((c, r), color)
    """

    """ # GLITCHY
    for i in range(401):
        color = lerpColor(color1, color2, (1.0/400)*i)
        print color
        print 10*i
        draw.rectangle((0, i, 400, 1), color)
    """

    """ # GLITCHY
    color = lerpColor(color1, color2, 0)
    print color
    draw.rectangle((0, 0, 400, 100), fill=color)
    color = lerpColor(color1, color2, .33)
    print color
    draw.rectangle((0, 100, 400, 100), fill=color)
    color = lerpColor(color1, color2, .67)
    print color
    draw.rectangle((0, 200, 400, 100), fill=color)
    color = lerpColor(color1, color2, 1)
    print color
    draw.rectangle((0, 300, 400, 100), fill=(100, 128, 255))
    del draw
    """
    img.save('dickbutt.png')

if __name__ == "__main__":
    main()
