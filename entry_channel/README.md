# Entry Channel Visits with Goals Tracker

This script, `entry_channel_visits_with_goals.py`, extracts visit data from the Matomo API and generates a report of website entry pages, their channel types, and counts for a specified goal ID. The output is saved as a CSV file that includes the number of visits and occurrences of a particular goal within each visit’s actions.

## Requirements

- **Python 3.x**
- Required packages: `requests`, `pandas`, `tqdm`

Install the required packages using:
```bash
pip install requests pandas tqdm
```

## Usage

1. **Clone or Download the Script**: Save the script as `entry_channel_visits_with_goals.py`.

2. **Run the Script**:
   ```bash
   python entry_channel_visits_with_goals.py
   ```

3. **User Prompts**:
   - **Starting Date**: Enter the starting date for the data extraction in `YYYY-MM-DD` format. Defaults to yesterday's date if left blank.
   - **Ending Date**: Enter the ending date for the data extraction in `YYYY-MM-DD` format. Also defaults to yesterday if left blank.
   - **Goal ID**: Enter the goal ID to track within visits. This is required to filter actions containing this specific goal.
   - **Maximum Visits per Day**: The script fetches a maximum of 10,000 visits per day by default. You can adjust this limit as needed.

4. **Output**:
   - The script outputs a CSV file named `entry_channel_visits_with_goals.csv` in the same directory. It contains the following columns:
     - **Entry Page**: The URL of the first action in each visit (entry page).
     - **Channel Type**: The referrer type for each visit (e.g., search, direct).
     - **Number of Visits**: The total number of visits for each unique entry page and channel type combination.
     - **Goals**: The number of times the specified goal was achieved within each entry page and channel type combination.

## Example Output

An example row in `entry_channel_visits_with_goals.csv`:
| Entry Page                                         | Channel Type | Number of Visits | Goals |
|----------------------------------------------------|--------------|------------------|-------|
| https://www.example.com/product                    | search       | 15               | 5     |
| https://www.example.com/about                      | direct       | 10               | 2     |

## Script Explanation

The script performs the following actions:
1. **Date Range Generation**: Generates a list of dates based on the user-provided start and end dates.
2. **Data Fetching**: Pulls visit data for each day from the Matomo API, with pagination using offsets.
3. **Data Extraction**:
   - Counts the occurrences of the specified goal ID within each visit’s `actionDetails`.
   - Aggregates data by `Entry Page` and `Channel Type` to get total visits and goal counts.
4. **Data Output**: Saves the aggregated data as a CSV file.

## Notes
- **API Token**: This script uses an open demo Matomo instance (`token_auth=anonymous`). Replace `token_auth` with your API key if accessing a private Matomo instance.
- **Data Limits**: The script may require adjustment if you need more than the default limit of 10,000 visits per day.

## Troubleshooting

If data retrieval fails or the CSV file appears empty:
- Verify your API token (if using a private Matomo instance).
- Ensure date formats are correct.
- Check the goal ID is valid and that the Matomo instance has data for the specified goal.
