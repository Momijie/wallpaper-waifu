#!/bin/bash
imageviewer="nsxiv"
clear

echo "Creating ./test/"
mkdir ./.test

python wallpaper-gen.py -h
python wallpaper-gen.py ./.test/default.png --debug --ornament_num 500 --ornament_minimum_distance 100 --ornament_samples 10

"$imageviewer" ./.test/

echo "Deleting ./test/"
rm ./.test/ -rf
