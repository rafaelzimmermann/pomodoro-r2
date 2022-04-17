#!/bin/bash

set -e

PATH="$PATH:/home/spike/.envs/pomodoro-r2/bin/"
PORT="/dev/ttyACM0"
dir_path=$1

if [ -z $dir_path ]; then
  dir_path="."
fi

directories=$(find "${dir_path}" -type d | grep -v "\/\.")
echo "Creating directories..."

for dir in $directories; do
    echo "$dir"
    ampy --port /dev/ttyACM0 mkdir --exists-okay "$dir"
done


files=$(find "${dir_path}" -type f | grep "\.py")
echo "Copying files..."
for f in $files; do
    echo "$f"
    ampy --port /dev/ttyACM0 put $f $f
done
