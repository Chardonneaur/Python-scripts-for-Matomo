import requests
import pandas as pd
import xml.etree.ElementTree as ET

# Function to fetch custom report data for a single idSite
def fetch_custom_reports(base_url, token_auth, idSite):
    params = {
        "module": "API",
        "method": "CustomReports.getConfiguredReports",
        "idSite": idSite,
        "format": "xml",
        "token_auth": token_auth
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error for idSite {idSite}: {response.status_code}")
        return None

# Function to parse XML and extract relevant data
def parse_custom_reports(xml_data, idSite):
    rows = []
    root = ET.fromstring(xml_data)
    for row in root.findall("row"):
        idcustomreport = row.find("idcustomreport").text if row.find("idcustomreport") is not None else None
        name = row.find("name").text if row.find("name") is not None else None
        rows.append({
            "idsite": idSite,
            "idcustomreport": idcustomreport,
            "name": name
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

    # Loop through each idSite to fetch and parse data
    for idSite in idSites:
        print(f"Fetching custom reports for idSite {idSite}...")
        xml_data = fetch_custom_reports(base_url, token_auth, idSite)
        if xml_data:
            all_data.extend(parse_custom_reports(xml_data, idSite))

    # Convert the data to a DataFrame and display/save it
    df = pd.DataFrame(all_data)
    print("\nFetched Custom Reports Data:")
    print(df)

    # Save the output to a CSV file
    output_file = "custom_reports_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\nData has been saved to {output_file}.")

if __name__ == "__main__":
    main()
