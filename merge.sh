#!/bin/bash

folder="/home/pi/cg3002/data"
output="in.csv"
cmd="find $folder -maxdepth 1 -iname '*.csv' | grep -vE '($output|out.csv)'" # | xargs cat > 'in.csv'

echo "Your data folder is: $folder"
echo "Your output csv is: $output"
echo "Running command: $cmd | xargs cat > '$output'"
read -e -p "Continue? y/n (leave blank for y): " $CONTINUE
[ "$CONTINUE" != "y" -o "$CONTINUE" != "" ] && exit 0
eval "$cmd"
filecount="$($cmd | wc -l)"
old="$($cmd | xargs cat | wc -l)"
new="$(cat $folder | wc -l)"

echo "Concatenating $filecount csv files produced $old lines of data."
echo "Number of lines in in.csv: $new"
