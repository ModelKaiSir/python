# 图片转字符图片
from PIL import Image
from urllib.request import urlopen
from io import BytesIO

# 用于替换图片rgb值的字符
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.>")
url_path = "http://labfile.oss.aliyuncs.com/courses/370/test.png"

img_path = "D:\desktopWork\image\huaji.jpg"

def getRgbChar(r, g, b, alpha=256):
    if alpha == 0:
        return '  '
    l = len(ascii_char)

    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (alpha + 1) /l

    index = int(gray/unit)
    if index >= len(ascii_char):
        index = len(ascii_char) - 1
    return ascii_char[int(index)]


file = urlopen(url_path)
temp = BytesIO(file.read())
img = Image.open(temp)

# img = Image.open(img_path)

img = img.resize((int(img.size[0]/10),int(img.size[1]/10)), Image.NEAREST)

if img is not None:
    w, h = img.size[0], img.size[1]
    print("{} : {}".format(w, h))
    text = ""
    for i in range(h):
        for j in range(w):
            text += getRgbChar(*img.getpixel((j, i)))
        text += "\n"

    print(text)


