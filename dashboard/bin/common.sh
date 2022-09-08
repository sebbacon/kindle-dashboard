#!/bin/bash


export PYTHONPATH=$(realpath $(dirname $0)../../..)
#cd "/mnt/base-us/extensions/dashboard/"
cd $PYTHONPATH/dashboard


# Remove files
if [ -f ./svg/tmp.svg ]; then
    rm ./svg/tmp.svg
fi

if [ -f ./svg/tmp.png ]; then
    rm ./svg/tmp.png
fi


# Copy rsvg-convert to a share where it can be started
# The shared folder that can be accessed via USB is mounted with the noexec flag,
# copying file to /var/tmpt gets around this restriction.
if [ ! -f /var/tmp/rsvg-convert ]; then
    cp -rf ./external/* /var/tmp
fi

python3 ./bin/run.py


# Check if svg exists and convert it
if [ -e ./svg/tmp.svg ]; then
  export LD_LIBRARY_PATH=/var/tmp/rsvg-convert-lib:/usr/lib:/lib
  /var/tmp/rsvg-convert-lib/rsvg-convert --background-color=white -o ./svg/tmp.png ./svg/tmp.svg > /dev/null 2>&1
  fbink -c -g file=./svg/tmp.png,w=758,halign=center,valign=center > /dev/null 2>&1
fi