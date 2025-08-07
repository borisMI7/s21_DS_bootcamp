#!/bin/sh

head -n 1 *.csv | grep "," | uniq > hh_positions.csv
data=$(tail -n +2 -q *.csv)
echo "$data" >> hh_positions.csv 


