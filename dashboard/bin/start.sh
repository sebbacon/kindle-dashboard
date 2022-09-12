#!/bin/sh

set -eo pipefail

echo "Starting at $(date)"
# Make sure there is enough time to reconnect to the wifi
sleep 30

source "$(dirname $0)/common.sh"

# Make sure the screen is fully refreshed before going to sleep
sleep 5

echo "" > /sys/class/rtc/rtc1/wakealarm
# Following line contains sleep time in seconds
echo "+3600" > /sys/class/rtc/rtc1/wakealarm
# Following line will put device into deep sleep until the alarm above is triggered
echo mem > /sys/power/state

# Kill self and spawn a new instance
/bin/sh ./bin/start.sh && exit