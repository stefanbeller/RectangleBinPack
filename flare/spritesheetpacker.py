#!/usr/bin/python

from PIL import Image
import argparse
import flareSpriteSheetPacking

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Shrink animations definition file and image.')

    parser.add_argument('--mod', help = 'path to mod folder.', dest = 'mod',
                metavar = 'path', type = type(""), nargs = 1, required = True)

    parser.add_argument('--definition', help = 'path to a definition file.', dest = 'definition',
                metavar = 'path', type = type(""), nargs = 1, required = True)

    parser.add_argument('--resize', action = 'store_true', default = False)

    parser.add_argument('--save-always', dest = "save_always", action = 'store_true', default = False)

    args = parser.parse_args()
    if args.mod is None or args.definition is None:
        print "Definition and mod path must be supplied."
        exit(1)
    else:
        mod = args.mod[0]
        animname = args.definition[0]
        imgname = None
        with open(animname) as f:
            for line in f.readlines():
                if line.startswith('image='):
                    imgname=mod + '/' + (line.split('=')[1]).rstrip('\n')
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
