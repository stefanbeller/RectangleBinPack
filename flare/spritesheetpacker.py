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
    args=parser.parse_args()
    if args.images is None or args.definitions is None:
        print "At least one definition and one image must be supplied."
        exit(1)

    if len(args.definitions) == 1:
        animname = args.definitions[0]
        imgrects=[]
        for imgname in args.images:
            imgrect, additionalinformation = flareSpriteSheetPacking.parseAnimationFile(animname, imgname)
            imgrects+=[imgrect]
        for c in range(len(imgrects)):
            assert(len(imgrects[0]) == len(imgrects[c]))
            for n in range(len(imgrects[c])):
                if imgrects[c][n]["height"] != imgrects[0][n]["height"]:
                    w = max(imgrects[c][n]["height"], imgrects[0][n]["height"])
                    print "adjusting height to ", w, "at"
                    print imgrects[c][n]
                    print imgrects[0][n]
                    imgrects[c][n]["renderoffset"]=(imgrects[c][n]["renderoffset"][0], imgrects[c][n]["renderoffset"][1] + w-imgrects[c][n]["height"])
                    imgrects[0][n]["renderoffset"]=(imgrects[0][n]["renderoffset"][0], imgrects[0][n]["renderoffset"][1] + w-imgrects[0][n]["height"])
                    imgrects[c][n]["height"]=w
                    imgrects[0][n]["height"]=w

                if imgrects[c][n]["width"] != imgrects[0][n]["width"]:
                    w = max(imgrects[c][n]["width"], imgrects[0][n]["width"])
                    print "adjusting width to ", w, "at"
                    print imgrects[c][n]
                    print imgrects[0][n]
                    imgrects[c][n]["renderoffset"]=(imgrects[c][n]["renderoffset"][0] + w-imgrects[c][n]["width"], imgrects[c][n]["renderoffset"][1])
                    imgrects[0][n]["renderoffset"]=(imgrects[0][n]["renderoffset"][0] + w-imgrects[0][n]["width"], imgrects[c][n]["renderoffset"][1])
                    imgrects[c][n]["width"]=w
                    imgrects[0][n]["width"]=w


            # now in [0] all the maxima are set.
            for n in range(len(imgrects[c])):
                if imgrects[c][n]["height"] != imgrects[0][n]["height"]:
                    w = max(imgrects[c][n]["height"], imgrects[0][n]["height"])
                    print "adjusting height to ", w, "at"
                    print imgrects[c][n]
                    print imgrects[0][n]
                    imgrects[c][n]["renderoffset"]=(imgrects[c][n]["renderoffset"][0], imgrects[c][n]["renderoffset"][1] + w-imgrects[c][n]["height"])
                    imgrects[0][n]["renderoffset"]=(imgrects[0][n]["renderoffset"][0], imgrects[0][n]["renderoffset"][1] + w-imgrects[0][n]["height"])
                    imgrects[c][n]["height"]=w
                    imgrects[0][n]["height"]=w

                if imgrects[c][n]["width"] != imgrects[0][n]["width"]:
                    w = max(imgrects[c][n]["width"], imgrects[0][n]["width"])
                    print "adjusting width to ", w, "at"
                    print imgrects[c][n]
                    print imgrects[0][n]
                    imgrects[c][n]["renderoffset"]=(imgrects[c][n]["renderoffset"][0] + w-imgrects[c][n]["width"], imgrects[c][n]["renderoffset"][1])
                    imgrects[0][n]["renderoffset"]=(imgrects[0][n]["renderoffset"][0] + w-imgrects[0][n]["width"], imgrects[c][n]["renderoffset"][1])
                    imgrects[c][n]["width"]=w
                    imgrects[0][n]["width"]=w

            # now all must be the same:
            for n in range(len(imgrects[c])):
                assert (imgrects[c][n]["width"] == imgrects[0][n]["width"])
                assert (imgrects[c][n]["height"] == imgrects[0][n]["height"])

        # ok now lets pack it.
        rects = flareSpriteSheetPacking.extractRects(imgrects[0])
        newrects = flareSpriteSheetPacking.findBestEnclosingRectangle(rects)

        for c in range(len(imgrects)):
            imgrects[c] = flareSpriteSheetPacking.matchRects(newrects, imgrects[c])
            flareSpriteSheetPacking.writeImageFile(args.images[c], imgrects[c])

        flareSpriteSheetPacking.writeAnimationfile(animname, imgrects[0], additionalinformation)
