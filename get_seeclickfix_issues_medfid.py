import requests
import json
import pandas as pd
from datetime import datetime
import time
import os

# Whether or not to print the JSON output.
# Default should be False, because Page 24 or so has an emoji in the JSON
# which doesn't print to the Git Bash console properly without erroring out.
DEBUG = True

# Create a "data" directory if it doesn't exist
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

api_url = "https://seeclickfix.com/api/v2/issues"

# status=:status1,:status2 - one of ‘open’, ‘acknowledged’, ‘closed’, ‘archived’. 
# default: open,acknowledged,closed
# For this, we want archived issues too.
status = "open,acknowledged,closed,archived"

# Get the current date and time in the desired format
timestamp = datetime.now().strftime("%Y-%m-%d_%I%M%p")

# Specify the JSON file name in the "data" directory
json_file = os.path.join(data_dir, f"output_data_{timestamp}.json")

# Specify the CSV file name in the "data" directory
csv_file = os.path.join(data_dir, f"output_data_{timestamp}.csv")

# Record the start time
start_time = time.time()

# Set the rate limit and interval
rate_limit = 19  # requests per minute
interval = 60 / rate_limit  # interval in seconds

data_list = []  # Create a list to store data

with open(json_file, "w") as f:
    for page in range(1, 1036):  # Adjust the range as needed
        url = f"{api_url}?place_url=medford_3&per_page=20&page={page}&status={status}"
        print(f"Fetching page {page}...")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Page {page} was succesful!")
            page_data = response.json()
            json.dump(page_data, f)  # Write each page's data to the JSON file
            f.write('\n')            # Add a newline to separate each page's data
            data_list.extend(page_data['issues'])  # Extend the list with the 'issues' data
            if DEBUG:
                try:
                    print(f"page_data was: {json.dumps(page_data, ensure_ascii=False).encode('utf-8').decode()}")
                except:
                    print("Unable to print the JSON string, sorry :(")
                    
            # Calculate the average time per page
            time_per_page = (time.time() - start_time) / (page - 1) if page > 1 else 0

            # Calculate the remaining time in seconds
            remaining_pages = 1035 - page
            remaining_time = time_per_page * remaining_pages

            # Convert remaining_time to minutes and seconds for a more human-readable format
            remaining_minutes = int(remaining_time / 60)
            remaining_seconds = int(remaining_time % 60)

            print(f"Remaining time: {remaining_minutes} minutes {remaining_seconds} seconds")
        else:
            print(f"Page {page} was *NOT* succesful!")
            print(f"Response was: {response}")
            
        # Wait for the defined interval (3 seconds in this case)
        time.sleep(interval)

# Record the end time
end_time = time.time()

print("Data retrieval complete.")

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Script execution time: {elapsed_time:.2f} seconds")

# Load the JSON data into a Pandas DataFrame
df = pd.DataFrame(data_list)

# Save the DataFrame to a CSV file with the timestamp in the "data" directory
df.to_csv(csv_file, index=False)

print(f"JSON data saved to: {json_file}")
print(f"CSV data saved to: {csv_file}")
