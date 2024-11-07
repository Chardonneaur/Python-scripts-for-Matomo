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
    url = f"https://demo.matomo.cloud/index.php?module=API&format=JSON&idSite=1&period=day&date={date}&method=Live.getLastVisitsDetails&expanded=1&token_auth=anonymous&showColumns=actionDetails,referrerType&idVisit&filter_limit=10000&filter_offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for date {date} with offset {offset}")
        return []

# Main function
def main():
    # Get yesterday's date
    yesterday_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    # User inputs (defaulting to yesterday's date)
    start_date_str = input(f"Enter the starting date (YYYY-MM-DD) [default: {yesterday_date}]: ") or yesterday_date
    end_date_str = input(f"Enter the ending date (YYYY-MM-DD) [default: {yesterday_date}]: ") or yesterday_date
    goal_id = input("Enter the goal ID to track: ")
    max_offset = input("Enter the maximum visits in a day [default: 10000]: ")
    
    # Use default value of 10000 if no input is provided
    max_offset = int(max_offset) if max_offset else 10000

    # Parse dates
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Generate list of dates
    dates = generate_dates(start_date, end_date)

    # Initialize a list to store data
    extracted_data = []

    # Loop through dates and fetch data with incremental offsets
    for date in dates:
        offset = 0
        with tqdm(total=max_offset, desc=f'Processing date {date}', unit='offset', ncols=100) as pbar:
            while offset <= max_offset:
                data = fetch_data(date, offset)
                if not data:
                    break
                for visit in data:
                    if 'actionDetails' in visit and visit['actionDetails']:
                        entry_page = visit['actionDetails'][0].get('url', '')  # Get entry page from first action's URL
                        channel_type = visit.get('referrerType', '')  # Get channel type as referrerType
                        
                        # Count occurrences of the specified goal ID in actionDetails
                        goal_count = sum(1 for action in visit['actionDetails'] if action.get('type') == 'goal' and str(action.get('goalId')) == goal_id)

                        extracted_data.append({
                            'Entry Page': entry_page,
                            'Channel Type': channel_type,
                            'Number of Visits': 1,  # Increment by 1 per visit
                            'Goals': goal_count  # Count of specified goal ID occurrences
                        })
                offset += 10000
                pbar.update(10000)

    # Create a DataFrame
    df = pd.DataFrame(extracted_data)
    # Group by entry page and channel type to count visits and sum goals
    df = df.groupby(['Entry Page', 'Channel Type']).agg({
        'Number of Visits': 'sum',
        'Goals': 'sum'
    }).reset_index()

    # Display the DataFrame
    print(df)

    # Save to CSV
    output_path = 'entry_channel_visits_with_goals.csv'
    df.to_csv(output_path, index=False)

    print(f"CSV file saved at: {output_path}")

if __name__ == "__main__":
    main()
