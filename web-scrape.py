import requests
import json
import csv
from datetime import datetime, timedelta
from tqdm import tqdm

# Request stuff
cookies = {
    'remember_user_token': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczJORGd6WFN3aUpESmhKREV3SkhnMk1TOWtORGRTT0VrMGRVbHFlRmhNY0d0V2NXVWlMQ0l4TnpJd016RTJNemMwTGpNNE5EWXlOamtpWFE9PSIsImV4cCI6IjIwMjQtMDctMjFUMDE6Mzk6MzQuMzg0WiIsInB1ciI6bnVsbH19--8d021b27bc52ee104d917bc13232577f2e744e5c',
    '_thorpepark_session': 'TUFkRjl2SDIreVFTS0x3bDA5b0FrSHdMR1V3THY0Z0xUSXhyM3VjOWZIZTlrbjE2SE5SVWttbTlDL3hLL0hXZ1pMOXNyc0ZKa2RzTkNDL0FrdGU0cE1FSEJ6VWJGMnYxdVNUT3lYcjErVGRBVFBSbDZVY0VkVVREYnpPTCtHNWVYNk8rQ2U0cjhoWGwwWSs5M0JmQ210bUJOanA5VU5tLzNzWlN4N2s2MG1SMm9UVFgranNXNFEzSkthejR5czdSWGE2N3VESnhaSlVtaHR0cm5NY2NTbCtRd2w2aXNRUUZWa2JnbnRaSStjOVlINE5malFYbzZHamwzWHUzSGt4bTcvRHhZRFpNUWd3VGFXa0l5UXlHNHFwUm5XaU9weTY3SURtTTByZ1BLeFFhSmMxQ1NnQkJrZ0NtVlZpYkpMWGxiNi81WjFNMk5pMEtuL0xaR1JZQVFnPT0tLVVMMTBvOURCenNpRkl2cHJWRDBpTWc9PQ%3D%3D--a5ebac6e45bf674e5e933c35b0cabd7e79e305c5',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczJORGd6WFN3aUpESmhKREV3SkhnMk1TOWtORGRTT0VrMGRVbHFlRmhNY0d0V2NXVWlMQ0l4TnpJd016RTJNemMwTGpNNE5EWXlOamtpWFE9PSIsImV4cCI6IjIwMjQtMDctMjFUMDE6Mzk6MzQuMzg0WiIsInB1ciI6bnVsbH19--8d021b27bc52ee104d917bc13232577f2e744e5c; _thorpepark_session=TUFkRjl2SDIreVFTS0x3bDA5b0FrSHdMR1V3THY0Z0xUSXhyM3VjOWZIZTlrbjE2SE5SVWttbTlDL3hLL0hXZ1pMOXNyc0ZKa2RzTkNDL0FrdGU0cE1FSEJ6VWJGMnYxdVNUT3lYcjErVGRBVFBSbDZVY0VkVVREYnpPTCtHNWVYNk8rQ2U0cjhoWGwwWSs5M0JmQ210bUJOanA5VU5tLzNzWlN4N2s2MG1SMm9UVFgranNXNFEzSkthejR5czdSWGE2N3VESnhaSlVtaHR0cm5NY2NTbCtRd2w2aXNRUUZWa2JnbnRaSStjOVlINE5malFYbzZHamwzWHUzSGt4bTcvRHhZRFpNUWd3VGFXa0l5UXlHNHFwUm5XaU9weTY3SURtTTByZ1BLeFFhSmMxQ1NnQkJrZ0NtVlZpYkpMWGxiNi81WjFNMk5pMEtuL0xaR1JZQVFnPT0tLVVMMTBvOURCenNpRkl2cHJWRDBpTWc9PQ%3D%3D--a5ebac6e45bf674e5e933c35b0cabd7e79e305c5',
    'priority': 'u=0, i',
    'referer': 'https://queue-times.com/en-US/parks/16/rides/284',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

# Prepare CSV file
file = open('space_mountain.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerow(["Date", "Time", "Day of Week", "Month", "Time of Day", "Wait Time"])

# Date setup
datetime_str = '2014-12-06'
datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
end_date = datetime.now()

pbar = tqdm(total=(end_date - datetime_object).days + 1, desc="Processing Days")

while datetime_object <= end_date:
    params = {'given_date': datetime_str}
    response = requests.get('https://queue-times.com/en-US/parks/16/rides/284', params=params, cookies=cookies, headers=headers)
    
    # Extract json_park_data
    text = response.text
    start_idx = text.find('"name":"Reported by user"')
    end_idx = text.find('"colors":["#3273dc","#2c3e50"]')
    json_str = text[start_idx-3:end_idx-3]
    json_obj = json.loads(json_str)
    json_park_data = json_obj[1]["data"]
    
    for entry in json_park_data:
        date_part, time_part = entry[0].split()  # Split date and time
        time_obj = datetime.strptime(time_part, '%H:%M:%S')  # Convert time to datetime object
        
        if time_obj.minute % 30 == 0:  # Only write data at 30-minute intervals
            day_of_week = datetime.strptime(date_part, '%m/%d/%y').strftime('%A')  # Get day of week
            month = datetime.strptime(date_part, '%m/%d/%y').month  # Extract month as integer
            time_of_day = time_obj.hour * 60 + time_obj.minute  # Convert to integer (minutes since midnight)
            
            writer.writerow([date_part, time_part, day_of_week, month, time_of_day, entry[1]])
    
    datetime_object += timedelta(days=1)
    datetime_str = datetime_object.strftime('%Y-%m-%d')
    pbar.update(1)  # Manually increment progress bar

# Close file
file.close()