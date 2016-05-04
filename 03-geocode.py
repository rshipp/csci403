#!/usr/bin/env python
"""Convert intersections to coordinates"""
import json

import requests

def geocode(road1, road2):
    """Return adress from coords"""
    # read API keys
    with open('google_secret.json') as cred:
        key = json.load(cred)

    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={road1} and {road2}, new york city&key={key}'.format(road1=road1, road2=road2, key=key))
    r.raise_for_status()

    try:
        location = r.json()['results'][0]['geometry']['location']
        coordinates = [location['lat'], location['lng']]
    except (KeyError, IndexError):
        coordinates = []
    return coordinates

def main():
    with open('intersections.csv', 'r+') as f:
        csv = f.read().strip().split('\n')
        for line in csv:
            road, crossroad = line.split(',')
            print "'" + line + "': " + str(geocode(road, crossroad))

if __name__ == "__main__":
    main()
