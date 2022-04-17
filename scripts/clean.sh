#!/bin/bash

set -e

PATH="$PATH:/home/spike/.envs/pomodoro-r2/bin/"
PORT="/dev/ttyACM0"
files=$(ampy --port /dev/ttyACM0 ls)

if [ -z "${files}" ]; then
  echo "Raspberry pico is empty"
  exit 0
fi

files=$(ampy --port /dev/ttyACM0 ls | grep "\.py")
echo ">"
if [ -z "${files}" ]; then
  echo "No files."
else
  echo "Removing files..."
  for f in $files; do
      echo "$f"
      ampy --port /dev/ttyACM0 rm $f
  done
fi

files=$(ampy --port /dev/ttyACM0 ls)
if [ -z "${files}" ]; then
  echo "No directories."
else
  echo "Removing directories..."
  for f in $files; do
      echo "$f"
      ampy --port /dev/ttyACM0 rmdir $f
  done
fi
