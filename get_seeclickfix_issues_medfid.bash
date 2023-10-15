#!/bin/bash

# Format the date and time as "YYYY-MM-DD_HHMMam/pm"
current_datetime=$(date +"%Y-%m-%d_%I%M%P")
output_file="seeclickfix_medfid_$current_datetime.json"

api_url="https://seeclickfix.com/api/v2/issues"
# Adjust this value as needed; note that SeeClickFix rate limits 
# at 20 requests per minute as of 10/14/2023
# The default is conservative on purpose to avoid rate limits cloberring
# the output file...
request_interval=10

echo "Note: saving output to $output_file"

for page in {1..100}; do
  url="$api_url?place_url=medford_3&page=$page"
  echo "Fetching page $page..."
  curl -ksS "$url" >> "$output_file"
  sleep "$request_interval"
done

echo "Data retrieval complete. Output saved to $output_file"
