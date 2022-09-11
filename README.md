Show the next few events from a Google Calendar on a Kindle Paperwhite


# Install

## Jailbreak your Kindle
The correct way of doing this depends on the Kindle firmware (and hardware) you are using.

All the methods depend on exploits that are fixed in newer versions of the firmware.

All the documentation is in early 2000s-style phpbb-type forums. The user community is very helpful but it's rather hard to navigate around.

I started [here](https://www.mobileread.com/forums/showthread.php?t=320564) but later worked out that this method didn't support my _precise_ firmware and had to look around the forums for an older method.  

## Install required software

Once your Kindle is jailbroken, you can install new software. As the jailbreak threads like the one I linked to above describe, the general installation method is via software called `MRPI`; you drop binary files in a folder that you can see mounted as a filesystem when you connect your Kindle via a data USB cable to your laptop.

You need to use `MRPI` to install at least three things: python, KUAL, and USBNetwork. The most up-to-date packages are [in this thread](https://www.mobileread.com/forums/showthread.php?t=225030) at the time of writing. Python is for the scripts in this repo; KUAL is a kind of simple UI toolkit that makes it easy to interact with scripts, via menus; USBNetwork provides an SSHD service on your Kindle so you can get a shell, to debug things.


Once you have a shell (hint: open USBNetwork via KUAL; toggle "allow USBNetwork"; start out by connecting over USB, but for ease of use, then configure for public key auth so you can access over wifi safely).

Now you have a shell, you can install the python libraries required for interacting with Google Calendar API:

```sh
python3 -m ensurepip --upgrade
python3 -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib requests
```

I also deleted the Amazon-supplied binaries that provide for remote firmware update, as I don't want to remove access again. These are `u/usr/bin/otav3` and `/usr/bin/otaupd`.

Next, to be sure times are correct, I installed my local timezone info in the right place; that is, I copied `/usr/share/zoneinfo/Europe/London` from my laptop to the Kindle.  Note that I've currently hardcoded my timezone into the script. If you live elsewhere, you'll want to change that.

Finally, to install _this_ software, copy the folder `dashboard` from the repository to the `/extensions` folder on the kindle (if that folder is not there
KUAL isn't installed properly).

### Generate oauth credentials

Set up a local dev environment on your computer, by installing python3 and pip installing the dependencies listed above.

Create a file at `bin/calendar.txt` whose contents are the calendar id you wish to query.  Something like `family04215672838001015700@group.calendar.google.com` (get it from your calendar's "Sharing" settings).

Run the script at `bin/cal.py`, something like `cd bin/; PYTHONPATH=../../ python cal.py`. This should run the oauth flow to create `token.json` and `credentials.json`, that authorise your script's access. If it succeeds, you'll see some JSON of your upcoming events.

Now copy all three files (`calendar.txt`, `token.json`, and `credentials.json` to the `dashboard/bin/` directory on your Kindle). Test by running the same `cal.py` script from the command line on your Kindle.

## Run

Test locally on your computer by running `bin/start_once_laptop.sh`. This should generate and display the next 8 calendar entries as an SVG.

If that works, test on your Kindle with the "Calendar (debug)" button in KUAL. This should run the script once: it fills the screen with your calendar.

If _that_ works, first type `~ds` in the searchbar and hit enter. This will disable the Kindle's own deep sleep and screensaver, this is
required as this will put the device in deep sleep without the wake-up timer enabled eventually. Which in turn will 
stop the dashboard from refreshing. To disable this you will need to restart the Kindle by holding the power button for
15-20 seconds and pushing restart in the menu.

Now you can press the "Calendar" button. This does the same, but the script also puts the kindle into deep sleep, with a timer to wake it in an hour; and when it wakes it spawns a new copy of the same script. (Note this hack can make it rather hard to use your kindle normally; you have to wake it up, quickly SSH in and hope you are in the 30 second sleep window such that you have time to locate and `kill` the `start.sh` process!)


# Developing and deploying

The pragmatic solution I've used is deploy over an `sshfs` mount.

Toggle `USBNetwork` so it's running, ensure SSHD is available over wifi, then mount it locally, something like:

    sshfs root@192.168.1.82:/ /mnt/kindle

Usually I develop it locally, so pushing to the kindle is suitable. However, sometimes, for debugging you need to work directly on the device. So I've been using `unison` like this:

    unison -prefer dashboard/ -fat /mnt/kindle/mnt/base-us/extensions/dashboard/ dashboard/


## Starting the Dashboard

First type `~ds` in the searchbar and hit enter. This will disable the Kindle's own deep sleep and screensaver, this is
required as this will put the device in deep sleep without the wake-up timer enabled eventually. Which in turn will 
stop the dashboard from refreshing. To disable this you will need to restart the Kindle by holding the power button for
15-20 seconds and pushing restart in the menu.

Next, open KUAL and start "Dashboard 4DCu.be", wait 30 seconds for the dashboard to appear and done!

## Acknowledgements

Forked from https://github.com/4dcu-be/kual-dashboard with huge thanks.
