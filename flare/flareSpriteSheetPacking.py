#!/usr/bin/python

import Image
import ImageChops
import os
import random
import sys
import time
import tempfile
import subprocess

try:
    os.nice(20)
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
                        "height" : newimg.size[1]
                    }
                    images += [f]
        return images


    animation = open(fname, 'r')
    lines = animation.readlines();
    animation.close()

    additionalinformation = {}

    firstsection = True
    newsection = False
    for line in lines:
        if line.startswith("render_size_x"):
            render_size_x=int(line.split("=")[1])

        if line.startswith("render_size_y"):
            render_size_y=int(line.split("=")[1])

        if line.startswith("render_offset_x"):
            render_offset_x=int(line.split("=")[1])

        if line.startswith("render_offset_y"):
            render_offset_y=int(line.split("=")[1])

        if line.startswith("position"):
            position=int(line.split("=")[1])

        if line.startswith("frames"):
            frames=int(line.split("=")[1])

        if line.startswith("duration"):
            duration=int(line.split("=")[1])

        if line.startswith("type"):
            _type=line.split("=")[1].strip()

        if line.startswith("["):
            newsection = True
            if not firstsection:
                images += processNextSection()
            sectionname=line.strip()[1:-1]
            if firstsection:
                additionalinformation['firstsection'] = sectionname
            firstsection=False

    images += processNextSection()
    return images, additionalinformation


def writeImageFile(imgname, images):
    w, h = 0, 0
    for n in images:
        w = max(n["x"]+n["width"], w)
        h = max(n["y"]+n["height"], h)

    # write actual image:
    result = Image.new('RGBA', (w,h), (0, 0, 0, 0))
    for r in images:
        assert (r["x"]+ r["width"] <=w)
        assert (r["y"]+ r["height"] <=h)
        result.paste(r["image"], (r["x"], r["y"]))
    result.save(imgname)

def writeAnimationfile(animname, images, additionalinformation):
    w, h = 0, 0
    for n in images:
        w = max(n["x"]+n["width"], w)
        h = max(n["y"]+n["height"], h)

    def write_section(name):
        framelist = filter(lambda s: s["name"] == name, images)
        f.write("\n")
        f.write("["+name+"]\n")
        f.write("frames="+str(framelist[0]["frames"])+"\n")
        f.write("duration="+str(framelist[0]["duration"])+"\n")
        f.write("type="+str(framelist[0]["type"])+"\n")
        for x in framelist:
            #frame=index,direction,x,y,w,h,offsetx,offsety
            f.write("frame="+str(x["index"])+","+str(x["direction"])+","+str(x["x"])+","+str(x["y"])+","+str(x["width"])+","+str(x["height"])+","+str(x["renderoffset"][0])+","+str(x["renderoffset"][1])+"\n")

    firstsection=additionalinformation["firstsection"]
    sectionnames = {}
    for f in images:
        sectionnames[f["name"]] = True
    del sectionnames[firstsection]

    f = open(animname,'w')
    write_section(firstsection)
    for section in sectionnames:
        write_section(section)
    f.close()

def extractRects(images):
    """returns an array of dicts having ony width, height and index.
    The index describes the position in the passed array"""
    ret=[]
    for xindex, x in enumerate(images):
        r={"width":x["width"], "height":x["height"], "index":xindex}
        ret +=[r]
    return ret

def matchRects(newrects, images):
    for r in newrects:
        index = r["index"]
        images[index]["x"] = r["x"]
        images[index]["y"] = r["y"]
        #assert(images[index]["width"] == r["width"])
        #assert(images[index]["height"] == r["height"])
    return images

def findBestEnclosingRectangle(rects):
    rectPassString="" # passed to rectpacker
    for rect in sorted(rects, key=lambda x: x["index"]):
        rectPassString += " " + str(rect["width"]) + " " + str(rect["height"])

    tf = tempfile.mkstemp()
    string = "rectpacker " + rectPassString
    p = subprocess.call(string, stdout = tf[0], shell = True)

    filehandle = open(tf[1], 'r')
    positions = filehandle.readlines()
    filehandle.close()

    for pos, rect in zip(positions, rects):
        rect["x"]=int(pos.split()[0])
        rect["y"]=int(pos.split()[1])
    return rects

