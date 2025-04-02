import requests
import json
import csv
from datetime import datetime, timedelta

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
writer.writerow(["Date", "Time", "Wait Time"])

# Date stuff
datetime_str = '2014-12-06'
datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
# end_date = datetime.now()
end_date = datetime.strptime('2014-12-20', '%Y-%m-%d')
while datetime_object <= end_date:
    params = {
        'given_date': datetime_str,
    }
    # THERE IS A BETTER URL GO TO CALENDAR --> https://queue-times.com/en-US/parks/16/calendar/2017/07/17
    response = requests.get('https://queue-times.com/en-US/parks/16/rides/284', params=params, cookies=cookies, headers=headers)
    # Extract json_park_data
    text = response.text
    # print(text)
    start_idx = text.find('"name":"Reported by user"')
    end_idx = text.find('"colors":["#3273dc","#2c3e50"]')
    json_str = text[start_idx-3:end_idx-3]
    json_obj = json.loads(json_str)
    json_pretty_str = json.dumps(json_obj, indent=2)
    # print(json_pretty_str)
    json_park_data = json_obj[1]["data"]
    # print("Index test:", json_park_data)
    # print("LENGTH:", len(json_park_data))
    # Fill in CSV file
# Fill in CSV file
    for entry in json_park_data:
        date_str, time_str = entry[0].split()  # Split into date and time parts
        wait_time = entry[1]
        
        # Parse the time
        time_obj = datetime.strptime(time_str, '%H:%M:%S')

        # Only write to CSV if the time is at a 30-minute interval (e.g., 00:00, 00:30, 01:00, etc.)
        if time_obj.minute % 30 == 0:
            writer.writerow([date_str, time_str, wait_time])
            
    datetime_object += timedelta(days=1)
    datetime_str = datetime_object.strftime('%Y-%m-%d')

# Close file
file.close()