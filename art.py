# coding: cp437

from PIL import Image
import re, random, math, requests, json, os
from operator import add, itemgetter
from search import search
def main():
    functions = [draw, imageSearchArt]
    for i in range(len(functions)):
        print str(i) + ": " + functions[i].__name__
    goodResponse = False
    response = -1
    while not goodResponse:
        try:
            response = int(raw_input('Which option would you like? '))
            if response >= 0 and response < len(functions):
                goodResponse = True
        except:
            print 'please enter a number corresponding to one of the options'
    functions[response]().show()

def imageSearchArt():
    path = search()
    img = Image.open(path)
    img = medianFilter(img, loops=60)
    img = smooth(img)
    img.save('uncomfortablyLongFart.png')
    os.remove(path)
    return img

def makeEquation(x, equation):
    y = 0
    check = False
    index = 0
    while index < len(equation) and not check:
        check = equation[index].isalpha()
        index += 1
    index -= 1
    equation = equation[index:]
    segs = re.split(r'[+-]', equation)
    ops = re.split(r'[^+-]+', equation)
    try:
        while(segs.remove("")):
            pass
    except:
        pass
    op = "+"
    i = 0
    while i < len(segs):
        temp = x
        j = len(segs[i])-1
        while j >= 0:
            # print temp
            segPart = segs[i][j]
            if segPart == 'X':
                temp *= x
            elif segPart == 'S':
                # print 'sin'
                try:
                    temp = math.sin(temp)
                except:
                    temp = float('inf')
            elif segPart == 'C':
                try:
                    temp = math.cos(temp)
                except:
                    temp = float('inf')
            elif segPart == 'T':
                try:
                    temp = math.tan(temp)
                except:
                    temp = float('inf')
            elif segPart == 'K':
                try:
                    temp = 1 / math.sin(temp)
                except:
                    temp = float('inf')
            elif segPart == 'E':
                try:
                    temp = 1 / math.cos(temp)
                except:
                    temp = float('inf')
            elif segPart == 'O':
                try:
                    temp = 1 / math.tan(temp)
                except:
                    temp = float('inf')
            j -= 1
        if op == "+":
            y += temp
        elif op == "-":
            y -= temp
        if len(ops) > 0:
            op = ops.pop(0)
        if len(op) > 1:
            op = "" + op[0]
        i += 1
    return y

def genEquation():
    length = int(random.gauss(6, 3))
    possible = "SCTXKEO+-"
    result = ""
    for i in range(length):
        index = int(random.randrange(0, len(possible)))
        result += possible[index]
    check = False
    i = 0
    while i < len(result) and not check:
        check = result[i].isalpha()
        i += 1
    if not check:
        result += possible[int(random.randrange(0, 6))]
    return result

def getColors():
    data = '{"model":"default"}'
    r = requests.post('http://colormind.io/api/', data=data)
    data = r.json()['result']
    extraData = [(v, reduce(add, data[data.index(v)])) for v in data]
    extraData.sort(key=itemgetter(1), reverse = True)
    return (tuple(extraData[3][0]), tuple(extraData[1][0]))

def draw(scale=4, size=4000, left=None, right=None, rotate=False):
    colorTuple = getColors()
    scale = 4
    size = 4000
    width, height = size, size
    distance = int(size * .6375)
    if left == None:
        left = -scale
    if right == None:
        right = scale
    img = Image.new('RGBA', (width, height))

    color1 = colorTuple[1]
    color2 = colorTuple[0]
    equation = genEquation()
    print equation
    for i in range(width):
        mappedI = mapValue(i, 0, width, left, right)
        y = makeEquation(mappedI, equation)
        for j in range(height):
            match = mapValue(y, left, right, height, 0)
            try:
                match = int(match)
            except:
                match = 1000000
            point = distance - abs(j - int(match))
            if match >= 0 and match < height:
                percent = mapValue(point, 0, distance, 0, 1)
                img.putpixel((i, j), lerpColor(color1, color2, percent))
            else:
                img.putpixel((i, j), color1)
    if rotate:
        img.rotate(90)
    img.save('uncomfortablyLongFart.png')
    return img

def processImage(path='images/NorthernLights.png'):
    img = Image.open(path)
    img = medianFilter(loops=60)
    img = smooth(img, loops=1)
    img.save('uncomfortablyLongFart.png')

def medianFilter(img, loops=1):
    width, height = img.size
    pixels = list(img.getdata())
    imgNext = Image.new('RGBA', (width, height))
    print "Median Filtering"
    for i in range(loops):
        print "Pass %d" % (i+1)
        for r in range(height):
            for c in range(width):
                pixel = getMedianNeighbors(pixels, r, c, img.size)
                imgNext.putpixel((c, r), pixel)
        pixels = list(imgNext.getdata())
    return imgNext

def smooth(img, loops=1):
    width, height = img.size
    pixels = list(img.getdata())
    imgNext = Image.new('RGBA', (width, height))
    print "Smoothing"
    for i in range(loops):
        print "Pass %d" % (i+1)
        for r in range(height):
            for c in range(width):
                pixel = getAvgNeighbors(pixels, r, c, img.size)
                imgNext.putpixel((c, r), pixel)
        pixels = list(imgNext.getdata())
    return imgNext

def getAvgNeighbors(pixels, r, c, size):
    neighbors = []
    for rOff in range(-1, 2):
        for cOff in range(-1, 2):
            if inBounds(r + rOff, c + cOff, size):
                neighbors.append(pixels[(r + rOff) * size[0] + (c + cOff)])
    neighbors.sort(key=tupleSum)
    avgRGBA = [0 for i in neighbors[0]] # get num values in tuple
    for tIndex in range(len(neighbors[0])):
        avgRGBA[tIndex] = reduce(add, [x[tIndex] for x in neighbors]) / len(neighbors)
    return tuple(avgRGBA)

def getMedianNeighbors(pixels, r, c, size):
    neighbors = []
    for rOff in range(-1, 2):
        for cOff in range(-1, 2):
            if inBounds(r + rOff, c + cOff, size):
                neighbors.append(pixels[(r + rOff) * size[0] + (c + cOff)])
    neighbors.sort(key=tupleSum)
    if len(neighbors) % 2 == 0:
        return lerpColor(neighbors[len(neighbors) / 2], neighbors[(len(neighbors) / 2) + 1], .5)
    else:
        return neighbors[(len(neighbors) / 2) + 1]

def inBounds(r, c, size):
    return r >= 0 and c >= 0 and r < size[1] and c < size[0]

def tupleSum(tuple):
    return reduce(add, tuple[:-1])

def mapValue(value, left1, right1, left2, right2):
    return left2 + (right2 - left2) * ((value - left1) / (float(right1) - left1))

# I'm assuming that and RGBA isn't being lerped with and RGB
def lerpColor(color1, color2, percent):
    return tuple(int(color1[i] + (color2[i]-color1[i]) * percent) for i in range(len(color1)))

if __name__ == "__main__":
    main()
