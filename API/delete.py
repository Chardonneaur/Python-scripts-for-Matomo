import requests
import pandas as pd

# Function to delete a user in Matomo
def delete_user(base_url, token_auth, user_login, password_confirmation=''):
    params = {
        "module": "API",
        "method": "UsersManager.deleteUser",
        "userLogin": user_login,
        "format": "json",
        "token_auth": token_auth
    }
    
    if password_confirmation:
        params["passwordConfirmation"] = password_confirmation
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        result = response.json()
        if 'result' in result and result['result'] == 'success':
            print(f"Successfully deleted user: {user_login}")
        else:
            print(f"Failed to delete user {user_login}: {result}")
    else:
        print(f"Error deleting user {user_login}: {response.status_code}")

# Main function
def main():
    # Prompt user for inputs
    base_url = input("Enter the Matomo instance URL (e.g., https://demo.matomo.cloud/index.php): ").strip()
    token_auth = input("Enter your Matomo token_auth: ").strip()
    
    user_logins_input = input("Enter the list of user logins to delete, separated by commas (e.g., user1,user2,user3): ").strip()
    password_confirmation = input("Enter the password confirmation if required (leave blank if not applicable): ").strip()
    
    # Convert user login input to a list of strings
    user_logins = [user_login.strip() for user_login in user_logins_input.split(",")]

    # Loop through each user login to delete the user
    for user_login in user_logins:
        print(f"Attempting to delete user {user_login}...")
        delete_user(base_url, token_auth, user_login, password_confirmation)

if __name__ == "__main__":
    main()
