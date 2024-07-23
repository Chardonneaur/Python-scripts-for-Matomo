import requests
import pandas as pd
from datetime import datetime, timedelta

# Function to generate a list of dates between two dates
def generate_dates(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return date_list

# Function to fetch data from the API with a given date and offset
def fetch_data(date, offset):
    url = f"https://demo.matomo.cloud/index.php?module=API&format=JSON&idSite=1&period=day&date={date}&method=Live.getLastVisitsDetails&expanded=1&token_auth=anonymous&showColumns=actionDetails&filter_limit=10000&filter_offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for date {date} with offset {offset}")
        return []

# Main function
def main():
    # User inputs
    start_date_str = input("Enter the starting date (YYYY-MM-DD): ")
    end_date_str = input("Enter the ending date (YYYY-MM-DD): ")
    max_offset = int(input("Enter the maximum offset: "))

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
        while offset <= max_offset:
            data = fetch_data(date, offset)
            if not data:
                break
            all_data.extend(data)
            offset += 10000

    # Extract URLs where type is 'action'
    url_count = {}
    for visit in all_data:
        if 'actionDetails' in visit:
            for action in visit['actionDetails']:
                if action.get('type') == 'action':
                    url = action.get('url')
                    if url in url_count:
                        url_count[url] += 1
                    else:
                        url_count[url] = 1

    # Create a DataFrame
    df = pd.DataFrame(list(url_count.items()), columns=['URL', 'Total'])
    df = df.sort_values(by='Total', ascending=False)

    # Calculate total count and insert as the first and last row
    total_row = pd.DataFrame([['Total', df['Total'].sum()]], columns=['URL', 'Total'])
    df = pd.concat([total_row, df, total_row], ignore_index=True)

    # Save to CSV
    output_path = 'url_totals.csv'
    df.to_csv(output_path, index=False)

    print(f"CSV file saved at: {output_path}")

if __name__ == "__main__":
    main()
