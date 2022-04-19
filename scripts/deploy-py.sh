#!/bin/bash


SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
source $SCRIPTPATH/config.sh

dir_path=$1

if [ -z $dir_path ]; then
  dir_path="."
fi

files=$(find "${dir_path}" -type f | grep "\.py" | grep -v lcd | grep -v init)
echo "Copying files..."
for f in $files; do
    echo "$f"
    ampy --port $PORT put $f $f
done
