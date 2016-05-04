#!/bin/bash
# Get intersections from data.csv

while read line; do
    roads=( "$(echo $line | cut -d, -f3)" "$(echo $line | cut -d, -f4)" "$(echo $line | cut -d, -f5)" )
    echo ${roads[0]},${roads[1]} >> intersections.csv
    echo ${roads[0]},${roads[2]} >> intersections.csv
done < data.csv
sort -u intersections.csv -o intersections.csv
