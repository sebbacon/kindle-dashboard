# bin/python3
# encoding: utf-8

from datetime import datetime, timezone
import os
from os.path import join
from cal import get_events
from dashboard.bin.cache import cache_dir, cache


svg_path = os.path.join(os.environ["PYTHONPATH"], "dashboard", "svg")


def create_svg(svg_data, svg_template, svg_output):

    with open(svg_template, "r") as fin:

        template = fin.read()
        for k, v in svg_data.items():
            template = template.replace(k, v)

        with open(svg_output, "w") as fout:
            fout.write(template)


def fmt_date(date_input):
    d = datetime.strptime(date_input, "%Y-%m-%d").astimezone()
    return d.strftime("%d/%m/%Y")


def is_today(date_input, fmt="%Y-%m-%d"):
    return date_input == datetime.now().strftime(fmt)


@cache(join(cache_dir, "cal_cache.json"), 0)
def get_data():
    # Get Data
    events = get_events()
    max_events = 8  # the number of slots in the template
    utc_dt = datetime.now(timezone.utc)

    svg_data = {
        "LASTUPDATE": "Last Update: "
        + utc_dt.astimezone().strftime("%d/%m/%Y - %H:%M:%S"),
    }

    for i in range(max_events):
        if i < len(events):
            svg_data["EVENT_%d_DATE" % (i + 1)] = events[i][0]
            svg_data["EVENT_%d_TIME" % (i + 1)] = events[i][1]
            svg_data["EVENT_%d_DESCRIPTION" % (i + 1)] = events[i][2]
            if events[i][0] == "Today":
                svg_data["EVENT_%d_BG" % (i + 1)] = "#ffffff"
            elif events[i][0] == "Tomorrow":
                svg_data["EVENT_%d_BG" % (i + 1)] = "#e6e6e6"
            else:
                svg_data["EVENT_%d_BG" % (i + 1)] = "#afafaf"
        else:
            svg_data["EVENT_%d_DATE" % (i + 1)] = ""
            svg_data["EVENT_%d_TIME" % (i + 1)] = ""
            svg_data["EVENT_%d_DESCRIPTION" % (i + 1)] = "No more events found"
            svg_data["EVENT_%d_BG" % (i + 1)] = "#ffffff"
    return svg_data


def render_calendar():
    # Load Data into SVG
    svg_data = get_data()
    create_svg(svg_data, join(svg_path, "template.svg"), join(svg_path, "tmp.svg"))


if __name__ == "__main__":
    render_calendar()
