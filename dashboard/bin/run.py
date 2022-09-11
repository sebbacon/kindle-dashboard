# bin/python3
# encoding: utf-8

from datetime import datetime, timezone
import os
from os.path import join
from extract import get_google_scholar, get_gwent_data, get_tvmaze_data
from cal import get_events


scholar_url = "http://scholar.google.com/citations?user=4niBmJUAAAAJ&hl=en"
gwent_url = "http://www.playgwent.com/en/profile/sepro"
tvmaze_ids = [
    6,  # The 100
    79,  # The Goldbergs
    38963,  # The Mandalorian
    17128,  # This Is Us
]

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


def do_original_think():
    # Get Data
    gs_data = get_google_scholar(scholar_url)
    gwent_data = get_gwent_data(gwent_url)
    tvmaze_data = get_tvmaze_data(tvmaze_ids)

    # Combine into dict
    svg_data = {
        "GS_HINDEX": gs_data.get("h_index"),
        "GS_CITATIONS": gs_data.get("citations"),
        "GWENT_LADDER_RANK": gwent_data.get("ladder")
        + (
            " (Rank " + gwent_data.get("rank") + ")"
            if "Pro" not in gwent_data.get("ladder")
            else ""
        ),
        "GWENT_MMR": gwent_data.get("mmr"),
        "GWENT_POSITION": gwent_data.get("position"),
        "LASTUPDATE": "Last Update: " + datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
    }

    for i in range(3):
        if i < len(tvmaze_data):
            svg_data["TV_SHOW_%d" % (i + 1)] = tvmaze_data[i]["name"]
            svg_data["TV_EPISODE_%d" % (i + 1)] = tvmaze_data[i]["episode_name"]
            svg_data["TV_AIRDATE_%d" % (i + 1)] = (
                "TODAY"
                if is_today(tvmaze_data[i]["airdate"])
                else fmt_date(tvmaze_data[i]["airdate"])
            )
        else:
            svg_data["TV_SHOW_%d" % (i + 1)] = "No upcoming episodes found"
            svg_data["TV_EPISODE_%d" % (i + 1)] = ""
            svg_data["TV_AIRDATE_%d" % (i + 1)] = ""

    # Load Data into SVG
    create_svg(svg_data, join(svg_path, "template2.svg"), join(svg_path, "tmp.svg"))


def render_calendar():
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

    # Load Data into SVG
    create_svg(svg_data, join(svg_path, "template.svg"), join(svg_path, "tmp.svg"))


if __name__ == "__main__":
    render_calendar()
