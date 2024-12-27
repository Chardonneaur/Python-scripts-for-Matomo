import requests

def delete_all_segments(matomo_url, token_auth, id_site):
    """
    Fetch all segments for the specified idSite and delete them from the Matomo instance.

    Args:
        matomo_url (str): The base URL of the Matomo instance.
        token_auth (str): The authentication token for API access.
        id_site (str): The site ID to filter segments.
    """
    # Fetch all segments for the specified idSite
    get_all_url = f"{matomo_url}?module=API&method=SegmentEditor.getAll&idSite={id_site}&format=JSON&token_auth={token_auth}"
    try:
        response = requests.get(get_all_url)
        response.raise_for_status()
        segments = response.json()

        if not segments:
            print(f"No segments found for site ID {id_site}.")
            return

        print(f"Found {len(segments)} segments for site ID {id_site}. Deleting...")

        # Delete each segment
        for segment in segments:
            delete_url = f"{matomo_url}?module=API&method=SegmentEditor.delete&idSegment={segment['idsegment']}&token_auth={token_auth}"
            delete_response = requests.post(delete_url)
            if delete_response.status_code == 200:
                print(f"Deleted segment: {segment['name']}")
            else:
                print(f"Failed to delete segment: {segment['name']}, Status Code: {delete_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")

if __name__ == "__main__":
    # Replace these with your Matomo instance details
    matomo_url = input("Enter your Matomo instance URL: ").strip()
    token_auth = input("Enter your Matomo token_auth: ").strip()
    id_site = input("Enter the site ID (idSite) to delete segments from: ").strip()

    delete_all_segments(matomo_url, token_auth, id_site)
