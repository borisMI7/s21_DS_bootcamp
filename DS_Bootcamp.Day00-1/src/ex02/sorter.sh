#!/bin/sh
{ head -n 1 ../ex01/hh.csv; tail -n 20 ../ex01/hh.csv | sort -t ',' -k2 -k1; }|cat > hh_sorted.csv
