#!/usr/bin/python3

# Read file input/xxx.json, generate file output/xxx.md
FILE_VERSION="20201202"

## TODO: Output by_name, by_tag

# Real code for real men starts here.
import json
from datetime import datetime
import pytz
import re
import sys

languages = ['Spanish', 'French', 'Chinese', 'Japanese', 'Korean', 'Italian', 'Portuguese']

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html.encode('utf-8'))
    return cleantext

data = {}

with open("./input/%s.json" % FILE_VERSION) as json_file:
    data = json.load(json_file)

sessions = {}

for s in data.get('sessions', []):
    # Take name
    name = s['name']
    if name in sessions.keys():
        # append
        sessions[name].append(s)
    else:
        #create
        sessions[name] = [ s ]

# Now we have sessions aggregated by name.
# Split in multiple pages (500 items per page).
# it seems we need to split the output in parts, otherwise github is not able to render it as preview ;)
divide_by = 500

session_names = sorted(sessions.keys())

# Initialize array
topics_len = len(session_names)
page_range = (topics_len // divide_by) + 1
sess_split = []
for i in range(page_range):
    sess_split.append({})

i = 0
for name in session_names:
    pg_idx = i // 500
    sess_split[pg_idx][name] = sessions[name]
    i = i + 1

localtz = pytz.timezone("Europe/Rome")

i = 0
for sessions in sess_split:
    # Start generating MD output
    fn = "./output/%s_%s.md" % (FILE_VERSION, str(i))
    with open(fn, 'w') as o:
        o.write("# re:Invent 2020 - Session List\n\n")
        for name in sorted(sessions.keys()):
            s=sessions[name]
            if s[0]['tags'].split(",")[0] in languages:
                continue
            o.write("## {}\n".format(name.encode('utf-8')))
            o.write("**TAGS**: {}\n".format(s[0]['tags']))
            o.write("\n{}\n".format(cleanhtml(s[0]['description'])))
            o.write("\n")
            o.write("| Start (UTC) | End (UTC) | Location | G Calendar |\n")
            o.write("|-------------|-----------|----------|------------|\n")
            for det in s:
                tstart = localtz.localize(datetime.fromtimestamp(det['schedulingData']['start']['timestamp']), is_dst=None).astimezone(pytz.utc)
                tend = localtz.localize(datetime.fromtimestamp(det['schedulingData']['end']['timestamp']), is_dst=None).astimezone(pytz.utc)
                tzstart = tstart.strftime("%Y%m%dT%H%M%SZ")
                tzend = tend.strftime("%Y%m%dT%H%M%SZ")
                calname = "re:Invent 2020 - {}".format(name.encode('utf-8')).replace(" ", "+")
                location = "https://virtual.awsevents.com/media/{}".format(det['id'])
                location_link = "[{}]({})".format(det['id'], location)
                url = "https://www.google.com/calendar/render?action=TEMPLATE&text={}&location={}&dates={}%2F{}".format(calname, location, tzstart, tzend)
                link = "[G_CAL]({})".format(url)
                o.write("| {} | {} | {} | {} |\n".format(
                    tstart,
                    tend,
                    location_link,
                    link)
                )
    i = i + 1

