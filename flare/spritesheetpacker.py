#!/usr/bin/python

import Image
import argparse
import flareSpriteSheetPacking

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shrink animations definition file and image.')

    parser.add_argument('--image', metavar='path', type=type(""), nargs=1,
               help='path to the image files.', dest='image')

    parser.add_argument('--definition', metavar='path', type=type(""), nargs=1,
               help='path to a definition file.', dest='definition')

    parser.add_argument('--resize', action='store_true', default = False)

    args = parser.parse_args()
    if args.image is None or args.definition is None:
        print "At least one definition and one image must be supplied."
        exit(1)
    else:
        animname = args.definition[0]
        imgname = args.image[0]
        imgrects, additionalinformation = flareSpriteSheetPacking.parseAnimationFile(animname, imgname)

        imgs = flareSpriteSheetPacking.markDuplicates(imgrects)

        if args.resize:
            imgs = flareSpriteSheetPacking.resizeImages(imgs)

        rects = flareSpriteSheetPacking.extractRects(imgs)
        newrects = flareSpriteSheetPacking.findBestEnclosingRectangle(rects)
        imgrects = flareSpriteSheetPacking.matchRects(newrects, imgrects)

        flareSpriteSheetPacking.writeImageFile(imgname, imgrects)
        flareSpriteSheetPacking.writeAnimationfile(animname, imgrects, additionalinformation)
