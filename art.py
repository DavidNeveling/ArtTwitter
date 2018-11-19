# coding: cp437

from PIL import Image
import re, random, math

def main():
    draw()

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

def draw():
    scale = 4
    width, height = 400, 400
    left, right = -scale, scale
    img = Image.new('RGBA', (width, height))

    color1 = (255, 150, 255)
    color2 = (0, 100, 200)
    equation = genEquation()
    # equation = ''
    print equation
    for i in range(width):
        mappedI = mapValue(i, 0, width, left, right)
        # print 'mappedI = ' + str(mappedI)
        y = makeEquation(mappedI, equation)
        # print 'f(%f) = ' % i,
        # print y
        for j in range(height):
            match = mapValue(y, left, right, height, 0)
            if match == float('inf') or match == -float('inf'): # not sure what else to do in this case
                match = 1000000
            # print match
            point = 255 - abs(j - int(match))
            if match >= 0 and match < height:
                percent = mapValue(point, 0, 255, 0, 1)
                # print 'percent = ' + str(percent)
                img.putpixel((i, j), lerpColor(color1, color2, percent))
            else:
                img.putpixel((i, j), color2)
    img.save('dickbutt.png')

def mapValue(value, left1, right1, left2, right2):
    return left2 + (right2 - left2) * ((value - left1) / (float(right1) - left1))

def lerpColor(color1, color2, percent):
    return tuple(int(color1[i] + (color2[i]-color1[i]) * percent) for i in range(3))

if __name__ == "__main__":
    main()
