"""
This script fetches user activity data from a Matomo Analytics server over a specified date range 
and saves it in a CSV file. It does the following:

1. Prompts the user for a date range (with today as the default if no date is entered).
2. Makes repeated API requests to the Matomo server to retrieve detailed user visit data.
3. Extracts information such as:
   - userId
   - event category, action, and name
   - device type, brand, and model
   - action type (e.g., action or event)
   - URL of the action
4. Handles paginated API results (by using offsets).
5. Stores the extracted data into a pandas DataFrame and saves it as 'event_data.csv'.
6. The script also uses the `tqdm` library to display a progress bar for each date being processed.
"""

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
    url = f"https://demo.matomo.cloud/index.php?module=API&format=JSON&idSite=1&period=day&date={date}&method=Live.getLastVisitsDetails&expanded=1&token_auth=anonymous&showColumns=actionDetails,userId,deviceType,deviceBrand,deviceModel&filter_limit=10000&filter_offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for date {date} with offset {offset}")
        return []

# Main function
def main():
    # Get today's date
    today_date = datetime.today().strftime('%Y-%m-%d')

    # User inputs (defaulting to today's date)
    start_date_str = input(f"Enter the starting date (YYYY-MM-DD) [default: {today_date}]: ") or today_date
    end_date_str = input(f"Enter the ending date (YYYY-MM-DD) [default: {today_date}]: ") or today_date
    max_offset = int(input("Enter the maximum visits in a day: "))

    # Parse dates
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Generate list of dates
    dates = generate_dates(start_date, end_date)

    # Initialize a list to store concatenated data
    all_data = []

    # Loop through dates and fetch data with incremental offsets
    for date in dates:
        offset = 0
        with tqdm(total=max_offset, desc=f'Processing date {date}', unit='offset', ncols=100) as pbar:
            while offset <= max_offset:
                data = fetch_data(date, offset)
                if not data:
                    break
                all_data.extend(data)
                offset += 10000
                pbar.update(10000)

    # Extract relevant data including userId, event details, and device info
    extracted_data = []
    for visit in all_data:
        # Check if visit is a dictionary before proceeding
        if isinstance(visit, dict):
            # Extract userId and device details
            user_id = visit.get('userId', '')  # Allow empty values
            device_type = visit.get('deviceType', '')  # Allow empty values
            device_brand = visit.get('deviceBrand', '')  # Allow empty values
            device_model = visit.get('deviceModel', '')  # Allow empty values

            # Check if actionDetails exists and contains actions
            if 'actionDetails' in visit and visit['actionDetails']:
                for action in visit['actionDetails']:
                    # Extract event details, even if some fields are empty
                    event_category = action.get('eventCategory', '')  # Allow empty values
                    event_action = action.get('eventAction', '')  # Allow empty values
                    event_name = action.get('eventName', '')  # Allow empty values
                    action_type = action.get('type', '')  # To distinguish between 'action' and 'event'
                    url = action.get('url', '')  # URL of the action

                    # Append data to the list, allowing empty fields
                    extracted_data.append({
                        'userId': user_id,
                        'eventCategory': event_category,
                        'eventAction': event_action,
                        'eventName': event_name,
                        'deviceType': device_type,
                        'deviceBrand': device_brand,
                        'deviceModel': device_model,
                        'actionType': action_type,
                        'url': url
                    })

    # Create a DataFrame
    df = pd.DataFrame(extracted_data)
    
    # Save to CSV
    output_path = 'event_data.csv'
    df.to_csv(output_path, index=False)

    print(f"CSV file saved at: {output_path}")

if __name__ == "__main__":
    main()
