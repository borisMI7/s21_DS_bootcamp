#!/bin/sh
{ head -n 1 ../ex02/hh_sorted.csv; tail -n 20 ../ex02/hh_sorted.csv | awk -F ',' '
BEGIN{FS=OFS=","}
{
w = ""
line = $3
while (match(line, /(Junior|Middle|Senior)/)) {
    found = substr(line, RSTART, RLENGTH)
    w = w ? w"/"found : found
    line = substr(line, RSTART + RLENGTH)
}
buff = w ? w : "-"
buff = "\"" buff
$3 = buff "\"" 
print 
}
'; } | cat > hh_positions.csv

