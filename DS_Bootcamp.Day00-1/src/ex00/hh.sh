#!/bin/sh

if [ $# -eq 0 ]; then
	v_name="data scientist"
else
	v_name=$1	
fi

curl -G "https://api.hh.ru/vacancies" --data-urlencode "text=$v_name" -d "per_page=20" | jq > hh.json
