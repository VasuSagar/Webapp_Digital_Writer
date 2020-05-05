from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
# Create your views here.


def get_concat_h_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=True):           #concat and resize images acoordingly
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif (((im1.height > im2.height) and resize_big_image) or
          ((im1.height < im2.height) and not resize_big_image)):
        _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
    dst = Image.new('RGB', (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))
    return dst

def join(imlist):
    img = imlist.pop(0)

    for img2 in imlist:
        img =get_concat_h_resize(img, img2)
    return img


def makeimgarray(arr):
    list = []
    for i in arr:
        if (i == ' '):
            image = Image.open('cropimg/space.jpg')

        elif(i=='\n'):
            continue
        else:
            image = Image.open('cropimg/' + i + '.jpg')
        list.append(image)
    return list

def convert_to_transparent(img):
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        #if (item != (255, 255, 255, 255)):
            #print(item)
        if item[0] < 200 and item[1] < 200 and item[2] < 200:
            newData.append((0, 0, 69, 255))
        else:
            if item[0] > 150:
                newData.append((0, 0, 0, 0))
            else:
                newData.append(item)

    img.putdata(newData)
    return img


def mainfun(line):
    k = len(line) #total number of lines in file
    i = 0
    x = 1 #x axis for pasting image on specific location
    y = 0 # y axis for pasting image on specific location
    background = Image.open('cropimg/background.jpg')


    while (i != k):  #loop will run for n=total no of line
        imglist = makeimgarray(line[i])  # return array consisting of images of each letter in line
        i = i + 1
        final = join(imglist)  #will concate those image and return a concatenated image
        final=convert_to_transparent(final)
        final.thumbnail((600, 150))  #to resize image
        #final.save('indimg/Final' + str(i) + '.png') #to save every line img

        background.paste(final, (x, y),final.convert('RGBA')) #paste those images on white plain background
        y = y + 100 ##change y axis to new line

    return background

def home(req):
    return render(req,'home.html')


def process(req):
    val1=req.GET["text"]
    k=len(val1)
    handle = open('file.txt', 'w')
    handle.write(val1)
    handle.close()
    handle = open('file.txt', 'r')

    ##starting app.py logic
    line = handle.readlines()

    img = mainfun(line)

    img.save('img.jpg')  #save final result image in /media
    return render(req,'result.html',{'text':val1})    