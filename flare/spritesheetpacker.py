#!/usr/bin/python

from PIL import Image
import argparse
import flareSpriteSheetPacking

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Shrink animations definition file and image.')

    parser.add_argument('--definition', help = 'path to a definition file.', dest = 'definition',
                metavar = 'path', type = type(""), nargs = 1, required = True)

    parser.add_argument('--resize', action = 'store_true', default = False)

    parser.add_argument('--save-always', dest = "save_always", action = 'store_true', default = False)

    args = parser.parse_args()
    if args.image is None or args.definition is None:
        print "One definition and one image must be supplied."
        exit(1)
    else:
        animname = args.definition[0]
        imgname = None
        with f as open(animname):
            for line in f.readlines():
                if line.startswith('image='):
                    imgname=line.split('=')[1]
        if imgname == None:
            print 'No image path found in the spritesheet definition'
            exit(1)
        imgrects, additionalinformation = flareSpriteSheetPacking.parseAnimationFile(animname, imgname)

        imgs = flareSpriteSheetPacking.markDuplicates(imgrects)

        if args.resize:
            imgs = flareSpriteSheetPacking.resizeImages(imgs)

        rects = flareSpriteSheetPacking.extractRects(imgs)
        newrects = flareSpriteSheetPacking.findBestEnclosingRectangle(rects)
        imgrects = flareSpriteSheetPacking.matchRects(newrects, imgrects)

        size = flareSpriteSheetPacking.calculateImageSize(imgrects)
        oldsize = additionalinformation["original_image_size"]

        if args.save_always or (size[0] * size[1] < oldsize[0] * oldsize[1]):
            flareSpriteSheetPacking.writeImageFile(imgname, imgrects, size)
            flareSpriteSheetPacking.writeAnimationfile(animname, imgrects, additionalinformation)
