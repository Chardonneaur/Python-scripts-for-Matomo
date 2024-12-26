import requests

# Function to add segments
def add_segments(idSite, matomo_url, token_auth):
    segments = [
        {"name": "bounces", "definition": "actions<=1"},
        {"name": "desktop", "definition": "deviceType==desktop"},
        {"name": "direct", "definition": "referrerType==direct"},
        {"name": "new visitors", "definition": "visitorType==new"},
        {"name": "returning visitors", "definition": "visitorType==returning"},
        {"name": "search", "definition": "referrerType==search"},
        {"name": "smartphone", "definition": "deviceType==smartphone"},
        {"name": "social", "definition": "referrerType==social"},
        {"name": "tablet", "definition": "deviceType==tablet"},
        {"name": "unbounces", "definition": "actions>=2"},
        {"name": "website", "definition": "referrerType==website"}
    ]
    
    for segment in segments:
        url = f"{matomo_url}?module=API&method=SegmentEditor.add&name={segment['name']}&definition={segment['definition']}&idSite={idSite}&autoArchive=1&enabledAllUsers=1&token_auth={token_auth}"
        response = requests.post(url)
        if response.status_code == 200:
            print(f"Segment '{segment['name']}' added successfully.")
        else:
            print(f"Failed to add segment '{segment['name']}'. Status code: {response.status_code}")

# Main function
def main():
    # User inputs
    matomo_url = input("Enter the Matomo instance URL: ")
    token_auth = input("Enter your Matomo token_auth: ")
    idSite = input("Enter the site ID to add segments: ")

    # Add segments
    add_segments(idSite, matomo_url, token_auth)

if __name__ == "__main__":
    main()
