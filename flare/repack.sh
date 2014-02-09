#!/bin/bash

if [[ ! -z $mods || ! -z game_dir ]] ; then
	echo "Please define the variables mods and game_dir before running this script"
	exit 1
fi

for mod in ${mods}
do
	if [ -e "${game_dir}/mods/${mod}/animations" ] ; then
		for animfile in $(find ${game_dir}/mods/${mod}/animations |grep "\.txt$")
		do
			echo $animfile
			suffixtxt=$(echo "$animfile" |tr '/' ' ' |awk '$1=$2=$3=$4=$5=$6=""; {print $0} '|tr ' ' '/')
			suffixpng=$(echo "$animfile" |tr '/' ' ' |awk '$1=$2=$3=$4=$5=$6=""; {print $0} '|tr ' ' '/' | tr -s "/"|cut --characters=2-|sed 's,.txt$,.png,')

			./spritesheetpacker.py --definition ${game_dir}/mods/${mod}/animations/${suffixtxt} --image ${game_dir}/mods/${mod}/images/${suffixpng}

			{
				cd ${game_dir}
				git commit -a -m "repack $suffixpng"
				cd -
			}
		done
	else
		echo "$mod has no animations folder"
	fi
done
