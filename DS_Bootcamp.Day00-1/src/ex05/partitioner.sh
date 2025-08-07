#!/bin/sh
path="../ex03/hh_positions.csv"
u_values=$(tail -n 20 $path | awk -F ',' '{print substr($2, 2, 10)}' | sort | uniq)

for line in $u_values; do
	head -n 1 $path > $line.csv
	grep $line $path >> $line.csv
done
