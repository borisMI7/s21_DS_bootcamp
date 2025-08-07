#!/bin/sh

path="../ex03/hh_positions.csv"
values=$(tail -n +2 $path | awk -F ',' '{print $3}' | sort | uniq)
   
for line in $values; do
	number=$(awk -F ',' '{print $3}' $path | grep "$line" | wc -w | tr -d ' ')
	echo "$line,$number" >> temp
done

echo \"name\",\"count\" > hh_uniq_positions.csv
sort -t ',' -k2 -n -r temp >> hh_uniq_positions.csv
rm temp



: '
j_number=$(awk -F ',' '{print $3}' ../ex03/hh_positions.csv | grep "Junior" | wc -w)
m_number=$(awk -F ',' '{print $3}' ../ex03/hh_positions.csv | grep "Middle" | wc -w)
s_number=$(awk -F ',' '{print $3}' ../ex03/hh_positions.csv | grep "Senior" | wc -w)
echo \"name\",\"count\" > hh_uniq_positions.csv
echo \"Middle\",$m_number >> hh_uniq_positions.csv
echo \"Senior\",$s_number >> hh_uniq_positions.csv
echo \"Junior\",$j_number >> hh_uniq_positions.csv
sort -r -t ',' -k2 -o hh_uniq_positions.csv hh_uniq_positions.csv  
'
