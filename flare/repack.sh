#!/bin/bash

for mod in fantasycore alpha_demo minicore
do
    if [ -e "../../flare-game/mods/${mod}/animations" ] ; then
        for animfile in $(find ../../flare-game/mods/${mod}/animations |grep "\.txt$")
        do
            echo $animfile
            suffixtxt=$(echo "$animfile" |tr '/' ' ' |awk '$1=$2=$3=$4=$5=$6=""; {print $0} '|tr ' ' '/')
            suffixpng=$(echo "$animfile" |tr '/' ' ' |awk '$1=$2=$3=$4=$5=$6=""; {print $0} '|tr ' ' '/'|sed 's,.txt$,.png,')

            ./spritesheetpacker.py --definition ../../flare-game/mods/${mod}/animations/${suffixtxt} --image ../../flare-game/mods/${mod}/images/${suffixpng}
        done
    else
        echo "$mod has no animations folder"
    fi
done

