import requests
import pandas as pd

# Function to fetch data for a single idSite
def fetch_segment_data(base_url, token_auth, idSite):
    params = {
        "module": "API",
        "method": "SegmentEditor.getAll",
        "idSite": idSite,
        "format": "Tsv",
        "token_auth": token_auth,
        "translateColumnNames": 1
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error for idSite {idSite}: {response.status_code}")
        return None

# Function to process the fetched TSV data
def process_tsv_data(tsv_data, idSite):
    rows = []
    lines = tsv_data.strip().split("\n")
    header = lines[0].split("\t")
    idsegment_idx = header.index("idsegment")
    name_idx = header.index("name")
    enable_only_idsite_idx = header.index("enable_only_idsite")

    for line in lines[1:]:
        columns = line.split("\t")
        rows.append({
            "idsite": idSite,
            "idsegment": columns[idsegment_idx],
            "name": columns[name_idx],
            "enable_only_idsite": columns[enable_only_idsite_idx]
        })
    return rows

# Main function
def main():
    # Prompt user for inputs
    base_url = input("Enter the Matomo instance URL (e.g., https://demo.matomo.cloud/index.php): ").strip()
    token_auth = input("Enter your Matomo token_auth: ").strip()
    idSites_input = input("Enter the list of idSite values separated by commas (e.g., 1,2,3): ").strip()
    
    # Convert idSite input to a list of integers
    idSites = [int(idSite.strip()) for idSite in idSites_input.split(",")]

    all_data = []

    # Loop through each idSite to fetch and process data
    for idSite in idSites:
        print(f"Fetching data for idSite {idSite}...")
        tsv_data = fetch_segment_data(base_url, token_auth, idSite)
        if tsv_data:
            all_data.extend(process_tsv_data(tsv_data, idSite))

    # Convert the data to a DataFrame and display/save it
    df = pd.DataFrame(all_data)
    print("\nFetched Data:")
    print(df)

    # Save the output to a CSV file
    output_file = "segment_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\nData has been saved to {output_file}.")

if __name__ == "__main__":
    main()
	
