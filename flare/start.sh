#!/bin/bash
# minicore first:
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/cursed_grave.txt --images ../../flare-game/mods/minicore/images/enemies/cursed_grave.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/wyvern.txt --images ../../flare-game/mods/minicore/images/enemies/wyvern.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/zombie.txt --images ../../flare-game/mods/minicore/images/enemies/zombie.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/antlion.txt --images ../../flare-game/mods/minicore/images/enemies/antlion.png ../../flare-game/mods/minicore/images/enemies/fire_ant.png ../../flare-game/mods/minicore/images/enemies/ice_ant.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/minotaur.txt --images ../../flare-game/mods/minicore/images/enemies/minotaur.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/wyvern_adult.txt --images ../../flare-game/mods/minicore/images/enemies/wyvern_adult.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/antlion_small.txt --images ../../flare-game/mods/minicore/images/enemies/antlion_hatchling.png

cp ../../flare-game/mods/minicore/animations/skeleton.txt ../../flare-game/mods/minicore/animations/skeleton_weak.txt
cp ../../flare-game/mods/minicore/animations/skeleton.txt ../../flare-game/mods/minicore/animations/skeleton_archer.txt
cp ../../flare-game/mods/minicore/animations/skeleton.txt ../../flare-game/mods/minicore/animations/skeleton_mage_tmp.txt

# delete skeleton mage ranged
sed '30,35d' ../../flare-game/mods/minicore/animations/skeleton_mage_tmp.txt > ../../flare-game/mods/minicore/animations/skeleton_mage.txt
rm ../../flare-game/mods/minicore/animations/skeleton_mage_tmp.txt

./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/skeleton.txt --images  ../../flare-game/mods/minicore/images/enemies/skeleton.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/skeleton_weak.txt --images ../../flare-game/mods/minicore/images/enemies/skeleton_weak.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/skeleton_archer.txt --images ../../flare-game/mods/minicore/images/enemies/skeleton_archer.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/skeleton_mage.txt --images ../../flare-game/mods/minicore/images/enemies/skeleton_mage.png

sed '12,16d' ../../flare-game/mods/minicore/animations/goblin.txt > ../../flare-game/mods/minicore/animations/goblin_tmp.txt
cat << "EOF" >> ../../flare-game/mods/minicore/animations/goblin_tmp.txt
[hop]
position=4
frames=8
duration=60
type=looped

[run]
position=12
frames=8
duration=60
type=looped
EOF
cp ../../flare-game/mods/minicore/animations/goblin_tmp.txt ../../flare-game/mods/minicore/animations/goblin_.txt
cp ../../flare-game/mods/minicore/animations/goblin_tmp.txt ../../flare-game/mods/minicore/animations/goblin_elite_.txt
rm ../../flare-game/mods/minicore/animations/goblin_tmp.txt

# beware, need manual run/hop selection of goblin and goblin_runner.txt!
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/goblin_.txt --images ../../flare-game/mods/minicore/images/enemies/goblin.png
./spritesheetpacker.py --definition ../../flare-game/mods/minicore/animations/goblin_elite_.txt --images ../../flare-game/mods/minicore/images/enemies/goblin_elite.png

cp ../../flare-game/mods/minicore/animations/goblin_.txt ../../flare-game/mods/minicore/animations/goblin_runner_.txt
cp ../../flare-game/mods/minicore/animations/goblin_elite_.txt ../../flare-game/mods/minicore/animations/goblin_elite_runner_.txt

linenumbers=$(cat ../../flare-game/mods/minicore/animations/goblin_.txt |grep -n "\[" |grep -A1 run |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/minicore/animations/goblin_.txt | sed 's,hop,run,' > ../../flare-game/mods/minicore/animations/goblin.txt
rm ../../flare-game/mods/minicore/animations/goblin_.txt

linenumbers=$(cat ../../flare-game/mods/minicore/animations/goblin_elite_.txt |grep -n "\[" |grep -A1 run |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/minicore/animations/goblin_elite_.txt | sed 's,hop,run,' > ../../flare-game/mods/minicore/animations/goblin_elite.txt
rm ../../flare-game/mods/minicore/animations/goblin_elite_.txt

linenumbers=$(cat ../../flare-game/mods/minicore/animations/goblin_runner_.txt |grep -n "\[" |grep -A1 hop |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/minicore/animations/goblin_runner_.txt | sed 's,hop,run,' > ../../flare-game/mods/minicore/animations/goblin_runner.txt
rm ../../flare-game/mods/minicore/animations/goblin_runner_.txt

linenumbers=$(cat ../../flare-game/mods/minicore/animations/goblin_elite_runner_.txt |grep -n "\[" |grep -A1 hop |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/minicore/animations/goblin_elite_runner_.txt | sed 's,hop,run,' > ../../flare-game/mods/minicore/animations/goblin_elite_runner.txt
rm ../../flare-game/mods/minicore/animations/goblin_elite_runner_.txt












# fantasycore:
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/cursed_grave.txt --images ../../flare-game/mods/fantasycore/images/enemies/cursed_grave.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/wyvern.txt --images ../../flare-game/mods/fantasycore/images/enemies/wyvern.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/zombie.txt --images ../../flare-game/mods/fantasycore/images/enemies/zombie.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/antlion.txt --images ../../flare-game/mods/fantasycore/images/enemies/antlion.png ../../flare-game/mods/fantasycore/images/enemies/fire_ant.png ../../flare-game/mods/fantasycore/images/enemies/ice_ant.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/minotaur.txt --images ../../flare-game/mods/fantasycore/images/enemies/minotaur.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/wyvern_adult.txt --images ../../flare-game/mods/fantasycore/images/enemies/wyvern_adult.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/antlion_small.txt --images ../../flare-game/mods/fantasycore/images/enemies/antlion_hatchling.png

cp ../../flare-game/mods/fantasycore/animations/skeleton.txt ../../flare-game/mods/fantasycore/animations/skeleton_weak.txt
cp ../../flare-game/mods/fantasycore/animations/skeleton.txt ../../flare-game/mods/fantasycore/animations/skeleton_archer.txt
cp ../../flare-game/mods/fantasycore/animations/skeleton.txt ../../flare-game/mods/fantasycore/animations/skeleton_mage_tmp.txt
# delete skeleton mage ranged
sed '30,35d' ../../flare-game/mods/fantasycore/animations/skeleton_mage_tmp.txt > ../../flare-game/mods/fantasycore/animations/skeleton_mage.txt
rm ../../flare-game/mods/fantasycore/animations/skeleton_mage_tmp.txt

./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/skeleton_weak.txt --images ../../flare-game/mods/fantasycore/images/enemies/skeleton_weak.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/skeleton_archer.txt --images ../../flare-game/mods/fantasycore/images/enemies/skeleton_archer.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/skeleton.txt --images ../../flare-game/mods/fantasycore/images/enemies/skeleton.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/skeleton_mage.txt --images ../../flare-game/mods/fantasycore/images/enemies/skeleton_mage.png

sed '12,16d' ../../flare-game/mods/fantasycore/animations/goblin.txt > ../../flare-game/mods/fantasycore/animations/goblin_tmp.txt
cat << "EOF" >> ../../flare-game/mods/fantasycore/animations/goblin_tmp.txt
[hop]
position=4
frames=8
duration=60
type=looped

[run]
position=12
frames=8
duration=60
type=looped
EOF

cp ../../flare-game/mods/fantasycore/animations/goblin_tmp.txt ../../flare-game/mods/fantasycore/animations/goblin_.txt
cp ../../flare-game/mods/fantasycore/animations/goblin_tmp.txt ../../flare-game/mods/fantasycore/animations/goblin_elite_.txt
rm ../../flare-game/mods/fantasycore/animations/goblin_tmp.txt

# beware, need manual run/hop selection of goblin and goblin_runner.txt!
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/goblin_.txt --images ../../flare-game/mods/fantasycore/images/enemies/goblin.png
./spritesheetpacker.py --definition ../../flare-game/mods/fantasycore/animations/goblin_elite_.txt --images ../../flare-game/mods/fantasycore/images/enemies/goblin_elite.png

cp ../../flare-game/mods/fantasycore/animations/goblin_.txt ../../flare-game/mods/fantasycore/animations/goblin_runner_.txt
cp ../../flare-game/mods/fantasycore/animations/goblin_elite_.txt ../../flare-game/mods/fantasycore/animations/goblin_elite_runner_.txt

linenumbers=$(cat ../../flare-game/mods/fantasycore/animations/goblin_.txt |grep -n "\[" |grep -A1 run |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/fantasycore/animations/goblin_.txt | sed 's,hop,run,' > ../../flare-game/mods/fantasycore/animations/goblin.txt
rm ../../flare-game/mods/fantasycore/animations/goblin_.txt

linenumbers=$(cat ../../flare-game/mods/fantasycore/animations/goblin_elite_.txt |grep -n "\[" |grep -A1 run |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/fantasycore/animations/goblin_elite_.txt | sed 's,hop,run,' > ../../flare-game/mods/fantasycore/animations/goblin_elite.txt
rm ../../flare-game/mods/fantasycore/animations/goblin_elite_.txt

linenumbers=$(cat ../../flare-game/mods/fantasycore/animations/goblin_runner_.txt |grep -n "\[" |grep -A1 hop |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/fantasycore/animations/goblin_runner_.txt | sed 's,hop,run,' > ../../flare-game/mods/fantasycore/animations/goblin_runner.txt
rm ../../flare-game/mods/fantasycore/animations/goblin_runner_.txt

linenumbers=$(cat ../../flare-game/mods/fantasycore/animations/goblin_elite_runner_.txt |grep -n "\[" |grep -A1 hop |tr ":" " "|awk '{print $1}'|xargs |tr " " ",")
sed "${linenumbers}d" ../../flare-game/mods/fantasycore/animations/goblin_elite_runner_.txt | sed 's,hop,run,' > ../../flare-game/mods/fantasycore/animations/goblin_elite_runner.txt
rm ../../flare-game/mods/fantasycore/animations/goblin_elite_runner_.txt


# TODO:
#../../flare-game/mods/fantasycore/animations/hero.txt

# TODO: search repo for "animations=" and act upon


