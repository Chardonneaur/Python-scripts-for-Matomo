import requests

# Function to add custom alerts
def add_alerts(idSites, matomo_url, token_auth):
    """
    Adds predefined custom alerts to the specified Matomo site IDs.

    Parameters:
        idSites (list): List of site IDs to add alerts to.
        matomo_url (str): URL of the Matomo instance.
        token_auth (str): Authentication token for Matomo API.
    """
    alerts = [
        {
            "name": "Visits Spike Alert +50% previous day",
            "period": "day",
            "report": "VisitsSummary_get",
            "metric": "nb_visits",
            "metricCondition": "percentage_increase_more_than",
            "metricValue": 50,
            "comparedTo": 1
        },
        {
            "name": "Visits Drop Alert -50% previous day",
            "period": "day",
            "report": "VisitsSummary_get",
            "metric": "nb_visits",
            "metricCondition": "percentage_decrease_more_than",
            "metricValue": 50,
            "comparedTo": 1
        },
        {
            "name": "Spam Alert +300 actions in one visit",
            "period": "day",
            "report": "VisitsSummary_get",
            "metric": "max_actions",
            "metricCondition": "greater_than",
            "metricValue": 299,
            "comparedTo": 7
        },
        {
            "name": "Not found pages Alert",
            "period": "day",
            "report": "Actions_getPageTitles",
            "reportCondition": "contains",
            "reportMatched": "404",
            "metric": "nb_hits",
            "metricCondition": "greater_than",
            "metricValue": 0,
            "comparedTo": 7
        },
        {
            "name": "Conversion Alert - No tracking",
            "period": "day",
            "report": "Goals_get",
            "metric": "nb_conversions",
            "metricCondition": "less_than",
            "metricValue": 1,
            "comparedTo": 7
        }
    ]

    for site_id in idSites:
        print(f"Adding alerts for site ID: {site_id}")
        for alert in alerts:
            # Construct the API URL
            url = (
                f"{matomo_url}?module=API&method=CustomAlerts.addAlert"
                f"&name={alert['name']}"
                f"&idSites={site_id}"
                f"&period={alert['period']}"
                f"&report={alert['report']}"
                f"&metric={alert['metric']}"
                f"&metricCondition={alert['metricCondition']}"
                f"&metricValue={alert['metricValue']}"
                f"&comparedTo={alert['comparedTo']}"
                f"&emailMe=0"
                f"&token_auth={token_auth}"
            )

            # Include optional conditions if defined
            if "reportCondition" in alert and "reportMatched" in alert:
                url += f"&reportCondition={alert['reportCondition']}"
                url += f"&reportMatched={alert['reportMatched']}"

            # Make the API request
            response = requests.post(url)
            if response.status_code == 200:
                print(f"Alert '{alert['name']}' added successfully for site ID {site_id}.")
            else:
                print(f"Failed to add alert '{alert['name']}' for site ID {site_id}. Status code: {response.status_code}, Response: {response.text}")

# Main function
def main():
    """
    Main function to prompt user inputs and call the add_alerts function.
    """
    print("Example for Matomo instance URL: https://your-matomo-instance.com/index.php")
    matomo_url = input("Enter the Matomo instance URL: ")
    token_auth = input("Enter your Matomo token_auth: ")

    # Accept multiple site IDs from user
    idSites_input = input("Enter the site IDs to add alerts (comma-separated): ")
    idSites = [site.strip() for site in idSites_input.split(",")]

    # Add alerts for each site ID
    add_alerts(idSites, matomo_url, token_auth)

if __name__ == "__main__":
    main()
