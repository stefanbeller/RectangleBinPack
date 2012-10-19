#!/usr/bin/python

import Image
import argparse
import flareSpriteSheetPacking

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shrink animations definition files and images.')
    parser.add_argument('--images', metavar='path', type=type(""), nargs='+',
               help='pathes to the image files.', dest='images')

    parser.add_argument('--definitions', metavar='path', type=type(""), nargs='+',
               help='path to a definition file.', dest='definitions')
    parser.add_argument('--resize', action='store_true', default=False)
    args=parser.parse_args()
    if args.images is None or args.definitions is None:
        print "At least one definition and one image must be supplied."
        exit(1)

    if len(args.definitions) == 1 and len(args.images) == 1:
        animname = args.definitions[0]
        imgname = args.images[0]
        imgrects, additionalinformation = flareSpriteSheetPacking.parseAnimationFile(animname, imgname)

        imgs = flareSpriteSheetPacking.removeDuplicates(imgrects)

        if args.resize:
            for index, img in enumerate(imgs):
                newsize = (img["image"].size[0]/2, img["image"].size[1]/2)
                imgs[index]["image"] = img["image"].resize(newsize, Image.BICUBIC)

        rects = flareSpriteSheetPacking.extractRects(imgs)
        newrects = flareSpriteSheetPacking.findBestEnclosingRectangle(rects)
        imgrects = flareSpriteSheetPacking.matchRects(newrects, imgrects)

        flareSpriteSheetPacking.writeImageFile(imgname, imgrects)
        flareSpriteSheetPacking.writeAnimationfile(animname, imgrects, additionalinformation)
