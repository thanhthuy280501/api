import os
import webbrowser
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def open_google_cloud_console():           # Guide user to create/select a project
    try:
        print("Step 1: Create a Google Cloud Project")
        print("Go to the following URL to create a new project or select an existing project:")
        webbrowser.open("https://console.cloud.google.com/")
        input("Press Enter after you have created or selected a project...")
    except Exception as e:
        print(f"Error: {e}")     # Add try-except blocks to handle potential errors gracefully
    
def enable_youtube_data_api():             # Help user enable the necessary API
    try:
        print("Step 2: Enable the YouTube Data API")
        print("Go to the following URL to enable the YouTube Data API for your project:")
        webbrowser.open("https://console.cloud.google.com/apis/library/youtube.googleapis.com")
        input("Press Enter after you have enabled the YouTube Data API...")
    except Exception as e:
        print(f"Error: {e}")     # Add try-except blocks to handle potential errors gracefully

def create_oauth_credentials():              # Assists in creating and downloading OAuth 2.0 credentials
    try:
        print("Step 3: Create OAuth 2.0 Credentials")
        print("Go to the following URL to create OAuth 2.0 credentials:")
        webbrowser.open("https://console.cloud.google.com/apis/credentials")
        print("1. Click on 'Create Credentials' and select 'OAuth 2.0 Client ID'.")
        print("2. Configure the consent screen if prompted.")
        print("3. Select 'Desktop app' as the application type.")
        print("4. Download the JSON file containing your client credentials.")
        input("Press Enter after you have created and downloaded the OAuth 2.0 credentials...")
    except Exception as e:
        print(f"Error: {e}")     # Add try-except blocks to handle potential errors gracefully

def ensure_client_secrets_file():    # Checks for the presence of the client secret JSON file
    try:
        default_path = os.path.join(os.getcwd(), "client_secret.json")
        if not os.path.exists(default_path):
            print(f"Please place your 'client_secret.json' file in the following directory:\n{default_path}")
            input("Press Enter after you have placed the file in the specified directory...")
        return default_path
    except Exception as e:
        print(f"Error: {e}")     # Add try-except blocks to handle potential errors gracefully
        return None

def authenticate_with_oauth(client_secrets_file):
    try:
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        return flow.run_console()
    except Exception as e:
        print(f"Error: {e}")
        return None

def build_youtube_client(credentials):
    try:
        return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_user_subscriptions(youtube):
    try:
        request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            mine=True
        )
        response = request.execute()
        for item in response["items"]:
            print(f"Title: {item['snippet']['title']}")
            print(f"Channel ID: {item['snippet']['resourceId']['channelId']}\n")
    except Exception as e:
        print(f"Error: {e}")

def main():                     # Coordinates the entire authentication and API interaction process
    open_google_cloud_console()
    enable_youtube_data_api()
    create_oauth_credentials()
    client_secrets_file = ensure_client_secrets_file()
    if client_secrets_file:
        credentials = authenticate_with_oauth(client_secrets_file)
        if credentials:
            youtube = build_youtube_client(credentials)
            if youtube:
                get_user_subscriptions(youtube)

if __name__ == "__main__":
    main()
