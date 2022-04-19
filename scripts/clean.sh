#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
source $SCRIPTPATH/config.sh


files=$(ampy --port $PORT ls)

if [ -z "${files}" ]; then
  echo "Raspberry pico is empty"
  exit 0
fi

files=$(ampy --port $PORT ls | grep "\.py")
echo ">"
if [ -z "${files}" ]; then
  echo "No files."
else
  echo "Removing files..."
  for f in $files; do
      echo "$f"
      ampy --port $PORT rm $f
  done
fi

files=$(ampy --port $PORT ls)
if [ -z "${files}" ]; then
  echo "No directories."
else
  echo "Removing directories..."
  for f in $files; do
      echo "$f"
      ampy --port $PORT rmdir $f
  done
fi
