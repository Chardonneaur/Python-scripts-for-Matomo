import requests
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

# Function to generate a list of dates between two dates
def generate_dates(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return date_list

# Function to fetch data from the provided URL with a given date and offset
def fetch_data(date, offset):
    url = f"https://demo.matomo.cloud/index.php?module=API&format=JSON&idSite=62&period=day&date={date}&method=Live.getLastVisitsDetails&expanded=1&token_auth=anonymous&showColumns=serverDatePretty,visitorId&filter_limit=10000&filter_offset={offset}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for date {date} with offset {offset}: {response.status_code}")
        return []

# Main function
def main():
    # Get yesterday's date
    yesterday_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    # User inputs (defaulting to yesterday's date)
    start_date_str = input(f"Enter the starting date (YYYY-MM-DD) [default: {yesterday_date}]: ") or yesterday_date
    end_date_str = input(f"Enter the ending date (YYYY-MM-DD) [default: {yesterday_date}]: ") or yesterday_date
    max_offset = input("Enter the maximum visits in a day [default: 10000]: ")

    # Use default value of 10000 if no input is provided
    max_offset = int(max_offset) if max_offset else 10000

    # Parse dates
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Generate list of dates
    dates = generate_dates(start_date, end_date)

    # Initialize a list to store visitor IDs
    all_visitor_ids = []

    # Loop through dates and fetch data with incremental offsets
    for date in dates:
        offset = 0
        while True:
            data = fetch_data(date, offset)
            
            if not data:
                break  # Stop if no data is returned or an error occurred
            
            # Extract visitorIds and add them to the list
            visitor_ids = [visit['visitorId'] for visit in data if 'visitorId' in visit]
            all_visitor_ids.extend(visitor_ids)
            
            # Check if fewer results than the limit are returned, which means we can stop for this date
            if len(data) < 10000:
                break
            
            # Increment the offset to fetch the next batch of data
            offset += 10000

    # Remove duplicate visitorIds to get the unique visitors
    unique_visitors = set(all_visitor_ids)

    # Calculate the total number of unique visitors
    total_unique_visitors = len(unique_visitors)

    print(f"Total number of unique visitors between {start_date_str} and {end_date_str}: {total_unique_visitors}")

if __name__ == "__main__":
    main()
