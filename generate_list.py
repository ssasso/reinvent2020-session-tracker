#!/usr/bin/python3

# Read file input/xxx.json, generate file output/xxx.md
FILE_VERSION="20201120"

# Real code for real men starts here.
import json
from datetime import datetime
import re
import sys

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
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

i = 0
for sessions in sess_split:
    # Start generating MD output
    fn = "./output/%s_%s.md" % (FILE_VERSION, str(i))
    with open(fn, 'w') as o:
        o.write("# re:Invent 2020 - Session List\n\n")
        for name in sorted(sessions.keys()):
            s=sessions[name]
            o.write("## {}\n".format(name))
            o.write("**TAGS**: {}\n".format(s[0]['tags']))
            o.write("\n{}\n".format(cleanhtml(s[0]['description'])))
            o.write("\n")
            o.write("| Start (UTC) | End (UTC) | Location | G Calendar |\n")
            o.write("|-------------|-----------|----------|------------|\n")
            for det in s:
                tstart = datetime.fromtimestamp(det['schedulingData']['start']['timestamp'])
                tend = datetime.fromtimestamp(det['schedulingData']['end']['timestamp'])
                tzstart = tstart.strftime("%Y%m%dT%H%M%SZ")
                tzend = tend.strftime("%Y%m%dT%H%M%SZ")
                calname = "re:Invent 2020 - {}".format(name).replace(" ", "+")
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


"""
    {
      "id": "1_3hvbfhan",
      "name": "Come architettare una soluzione di rendering 3D a basso costo con istanze spot (caso d'uso: Ferrari)",
      "description": "<div><div><div>In questa sessione parleremo dei benefici tecnologici ed economici legati all’utilizzo di servizi AWS per la gestione di applicazioni di rendering 3D. Ferrari racconterà come ha costruito un servizio efficiente di rendering, utilizzando le istanze GPU di ultima generazione e creando una modalità dinamica di assegnazione delle risorse basato su istanze di tipo Spot.</div></div></div>",
      "type": "7",
      "updatedAt": 1605769250,
      "thumbnailUrl": "https://cfvod.kaltura.com/p/3047232/sp/304723200/thumbnail/entry_id/1_3hvbfhan/version/100001/width/379/height/213/type/3",
      "tags": "Italian,Manufacturing,Architecture,Enterprise/Migration,Automotive,Compute,Session",
      "mediaType": 201,
      "duration": 0,
      "recordedEntryId": null,
      "schedulingData": {
        "start": {
          "timestamp": 1606798800,
          "timeZoneName": "US/Pacific",
          "timeZoneOffset": -28800
        },
        "end": {
          "timestamp": 1606800600,
          "timeZoneName": "US/Pacific",
          "timeZoneOffset": -28800
        }
      },
      "presenters": [],
      "stats": [],
      "hiddenTags": "__italian,amazon elastic compute cloud (amazon ec2),amazon cloudfront,amazon simple storage service (amazon s3)",
      "callToActionLink": ""
    },
"""
## G Calendar: https://www.google.com/calendar/render?action=TEMPLATE&text=a&details=aa&location=bb&dates=20201026T133300Z%2F20201111T133300Z