# Flare SpriteSheet Packing

## 1. Inside of bestEnclosingRect folder run

### make

This should produce rectpacker executable (under WIndows/MinGW it will have *.exe extension)

## 2. Make sure you have installed:

### Python 2.7 (https://www.python.org/downloads/)
### Pillow (https://pypi.python.org/pypi/Pillow) for Python 2.7
### NumPy (http://www.scipy.org/scipylib/download.html) for Python 2.7

## 3. Be sure there is no uncommitted work in your flare game repo, as step 4 will commit all changes without asking you.

## 4. From inside the flare directory you can run the repack shell script, which is just a wrapper around the python script

### mods=<the mod you want> game_dir=<relative path such as ../../flare-noname> ./repack.sh

Example:

### mods=noname game_dir=../../flare-noname ./repack.sh

Script searches corresponding spritesheets/animation definitions in next locations:

### ${game_dir}/mods/${mod}/images/${suffixpng}

and the txt in

### ${game_dir}/mods/${mod}/animations/${suffixtxt}

## 4. Wait until it finishes. It will take a very long time because it is doing it with different heuristics and lots of trial.
