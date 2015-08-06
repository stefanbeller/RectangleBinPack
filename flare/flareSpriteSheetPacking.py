#!/usr/bin/python
# This is just a library file for the spritesheetpacker.py executable

from PIL import Image
from PIL import ImageChops
import os
import random
import sys
import time
import tempfile
import subprocess
import sha

import numpy as np

try:
    os.nice(15)
except:
    print "not able to be nice!"

def parseAnimationFile(fname, imgname):
    images = []
    img = Image.open(imgname)

    def processNextSection():
        images = []
        for index in range(0, frames):
            for direction in range(0,8):
                x = (position + index) * render_size_x
                y = direction * render_size_y
                w = x + render_size_x
                h = y + render_size_y
                imgrect = (x, y, w, h)
                partimg = img.copy().crop(imgrect)
                bbox = partimg.split()[partimg.getbands().index('A')].getbbox()
                newimg = partimg.crop(bbox)

                if bbox is None:
                    print imgname
                    print "skipping empty image at ",(x, y, w, h)
                    print "position / direction is ",position, direction
                else:
                    f = {
                        "name" : sectionname,
                        "type" : _type,
                        "direction" : direction,
                        "index" : index,
                        "duration" : duration,
                        "frames" : frames,
                        "renderoffset" : (render_offset_x-bbox[0], render_offset_y-bbox[1]),
                        "image" : newimg,
                        "width" : newimg.size[0],
                        "height" : newimg.size[1],
                        "active_frame" : active_frame
                    }
                    images += [f]
        return images


    animation = open(fname, 'r')
    lines = animation.readlines();
    animation.close()

    additionalinformation = {}
    additionalinformation["original_image_size"] = img.size

    firstsection = True
    newsection = False
    compressedloading = False
    active_frame = None
    for line in lines:
        if line.startswith("image="):
            imgname = line.split("=")[1] # keep this information to write out again!
            additionalinformation["imagename"] = imgname

        if line.startswith("render_size"):
            value = line.split("=")[1]
            render_size_x = int(value.split(",")[0])
            render_size_y = int(value.split(",")[1])

        if line.startswith("render_offset"):
            value = line.split("=")[1]
            render_offset_x = int(value.split(",")[0])
            render_offset_y = int(value.split(",")[1])

        if line.startswith("position"):
            position = int(line.split("=")[1])

        if line.startswith("frames"):
            frames = int(line.split("=")[1])

        if line.startswith("duration"):
            duration = line.split("=")[1].strip()

        if line.startswith("type"):
            _type = line.split("=")[1].strip()

        if line.startswith("active_frame"):
            active_frame = line.split("=")[1].strip()

        if line.startswith("frame="):
            compressedloading = True;
            vals = line.split("=")[1].split(",")
            index = int(vals[0])
            direction = int(vals[1])
            x = int(vals[2])
            y = int(vals[3])
            w = x + int(vals[4])
            h = y + int(vals[5])
            render_offset_x = int(vals[6])
            render_offset_y = int(vals[7])
            imgrect = (x, y, w, h)
            partimg = img.copy().crop(imgrect)
            bbox = partimg.split()[partimg.getbands().index('A')].getbbox()
            newimg = partimg.crop(bbox)

            if bbox is None:
                print imgname
                print "skipping empty image at ",(x, y, w, h)
                print "direction is ", direction
            else:
                f = {
                    "name" : sectionname,
                    "type" : _type,
                    "direction" : direction,
                    "index" : index,
                    "duration" : duration,
                    "frames" : frames,
                    "renderoffset" : (render_offset_x-bbox[0], render_offset_y-bbox[1]),
                    "image" : newimg,
                    "active_frame" : active_frame
                }
                images += [f]

        if line.startswith("["):
            newsection = True
            if not firstsection and not compressedloading:
                images += processNextSection()
            compressedloading = False
            sectionname=line.strip()[1:-1]
            if firstsection:
                additionalinformation['firstsection'] = sectionname
            firstsection=False

    if not compressedloading:
        images += processNextSection()
    return images, additionalinformation

def markDuplicates(images):
    # assign global unique ids to each image:
    gid=0
    for im in images:
        im["gid"] = gid
        im["imagehash"] = sha.sha(im["image"].tostring()).hexdigest()
        gid += 1

    for im1 in images:
        for im2 in images:
            if im1["imagehash"] == im2["imagehash"]:
                smallergid = min(im1["gid"], im2["gid"])
                if "isequalto" in im1:
                    im1["isequalto"] = min(smallergid, im1["isequalto"])
                else:
                    im1["isequalto"] = smallergid

                if "isequalto" in im2:
                    im2["isequalto"] = min(smallergid, im2["isequalto"])
                else:
                    im2["isequalto"] = smallergid


    for im in images:
        if "isequalto" in im:
            if im["isequalto"] == im["gid"]:
                del im["isequalto"]

    return images

def resizeImages(imgs):
    for index, img in enumerate(imgs):
        imag = img["image"].load()
        for y in xrange(img["image"].size[1]):
            for x in xrange(img["image"].size[0]):
                if imag[x, y] == (255, 0, 255, 0):
                    imag[x, y] = (0, 0, 0, 0)

        newsize = (img["image"].size[0]/2, img["image"].size[1]/2)
        imgs[index]["image"] = img["image"].resize(newsize, Image.BICUBIC)
        imgs[index]["renderoffset"] = (imgs[index]["renderoffset"][0]/2, imgs[index]["renderoffset"][1]/2)
    return imgs

def extractRects(images):
    """returns an array of dicts having only width, height and index.
    The index describes the position in the passed array"""
    ret = []
    for xindex, x in enumerate(images):
        if not "isequalto" in x:
            r = {"width" : x["image"].size[0], "height" : x["image"].size[1], "index" : xindex, "gid" : x["gid"]}
            ret += [r]
    return ret

def findBestEnclosingRectangle(rects):
    rectPassString = ""
    for rect in sorted(rects, key = lambda x: x["index"]):
        rectPassString += " " + str(rect["width"]) + " " + str(rect["height"])

    tf = tempfile.mkstemp()
    if 'win' in sys.platform:
        string = "..\\bestEnclosingRect\\rectpacker.exe " + rectPassString
    elif sys.platform.startswith('linux'):
        string = "../bestEnclosingRect/rectpacker " + rectPassString
    p = subprocess.call(string, stdout = tf[0], shell = True)

    filehandle = open(tf[1], 'r')
    positions = filehandle.readlines()
    filehandle.close()

    for pos, rect in zip(positions, rects):
        rect["x"] = int(pos.split()[0])
        rect["y"] = int(pos.split()[1])
    return rects

def matchRects(newrects, images):
    for r in newrects:
        index = r["index"]
        images[index]["x"] = r["x"]
        images[index]["y"] = r["y"]
        #assert(images[index]["width"] == r["width"])
        #assert(images[index]["height"] == r["height"])
    for im in images:
        if "isequalto" in im:
            im["x"] = images[im["isequalto"]]["x"]
            im["y"] = images[im["isequalto"]]["y"]

    return images

def calculateImageSize(images):
    w, h = 0, 0
    for n in images:
        w = max(n["x"] + n["image"].size[0], w)
        h = max(n["y"] + n["image"].size[1], h)
    return (w, h)

def writeImageFile(imgname, images, size):
    result = Image.new('RGBA', size, (0, 0, 0, 0))
    for r in images:
        assert (r["x"] + r["image"].size[0] <= size[0])
        assert (r["y"] + r["image"].size[1] <= size[1])
        result.paste(r["image"], (r["x"], r["y"]))
    result.save(imgname, option = 'optimize')

def writeAnimationfile(animname, images, additionalinformation):
    w, h = 0, 0
    for n in images:
        w = max(n["x"]+n["image"].size[0], w)
        h = max(n["y"]+n["image"].size[1], h)

    def write_section(name):
        framelist = filter(lambda s: s["name"] == name, images)
        f.write("\n")
        f.write("["+name+"]\n")
        if len(framelist)>0:
            f.write("frames="+str(framelist[0]["frames"])+"\n")
            f.write("duration="+str(framelist[0]["duration"])+"\n")
            f.write("type="+str(framelist[0]["type"])+"\n")
            if framelist[0]["active_frame"]:
                f.write("active_frame="+str(framelist[0]["active_frame"])+"\n")
            for x in framelist:
                #frame=index,direction,x,y,w,h,offsetx,offsety
                f.write("frame=" + str(x["index"]) + "," + str(x["direction"]) + "," + str(x["x"]) + "," + str(x["y"]) + "," + str(x["image"].size[0]) + "," + str(x["image"].size[1]) + "," + str(x["renderoffset"][0]) + "," + str(x["renderoffset"][1]) + "\n")
        else:
            f.write("frames=1\n")
            f.write("duration=1s\n")
            f.write("type=back_forth\n")

    firstsection = additionalinformation["firstsection"]
    sectionnames = {}
    for f in images:
        sectionnames[f["name"]] = True
    if firstsection in sectionnames:
        del sectionnames[firstsection]

    f = open(animname,'w')

    if "imagename" in additionalinformation:
        f.write("\n")
        f.write("image="+additionalinformation["imagename"])
        #f.write("\n")

    write_section(firstsection)
    for section in sectionnames:
        write_section(section)
    f.close()


if __name__ == "__main__":
    print "This is just a library file containing lots of functions."
    print "Run spritesheetpacker.py instead"





