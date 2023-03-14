#!/bin/sh

set -eo pipefail

# Redirect all output to a logfile

# Saves file descriptors so they can be restored to whatever 
# they were before redirection or used themselves to output 
# to whatever they were before the following redirect.
exec 3>&1 4>&2
# Restore file descriptors for particular signals. Not
#  generally necessary since they should be restored
# when the sub-shell exits.
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>/tmp/calendar.log 2>&1

while true; do
    # Make sure there is enough time to reconnect to the wifi
    sleep 30
    if [[ -f "/var/run/calendar_flag" ]]; then

        echo "$(date): Refreshing calendar"
        source "$(dirname $0)/common.sh"

        # Make sure the screen is fully refreshed before going to sleep
        sleep 5
        echo "" > /sys/class/rtc/rtc1/wakealarm
        # Following line contains sleep time in seconds
        echo "+3600" > /sys/class/rtc/rtc1/wakealarm
        # Following line will put device into deep sleep until the alarm above is triggered
        echo mem > /sys/power/state
        # Give the user time to override calendar_flag
        sleep 30
        if [[ -f "/var/run/calendar_flag" ]]; then
            # Reboot! Because wifi does not reliably restart on awakening
            # /sbin/reboot
            restart wifid
        fi
    else
        echo "$(date): Calendar is off"
    fi
done
