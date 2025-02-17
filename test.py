import os
import webbrowser
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
def open_google_cloud_console():
    print("Step 1: Create a Google Cloud Project")
    print("Go to the following URL to create a new project or select an existing project:")
    webbrowser.open("https://console.cloud.google.com/")
    input("Press Enter after you have created or selected a project...")
def enable_youtube_data_api():
    print("Step 2: Enable the YouTube Data API")
    print("Go to the following URL to enable the YouTube Data API for your project:")
    webbrowser.open("https://console.cloud.google.com/apis/library/youtube.googleapis.com")
    input("Press Enter after you have enabled the YouTube Data API...")
def create_oauth_credentials():
    print("Step 3: Create OAuth 2.0 Credentials")
    print("Go to the following URL to create OAuth 2.0 credentials:")
    webbrowser.open("https://console.cloud.google.com/apis/credentials")
    print("1. Click on 'Create Credentials' and select 'OAuth 2.0 Client ID'.")
    print("2. Configure the consent screen if prompted.")
    print("3. Select 'Desktop app' as the application type.")
    print("4. Download the JSON file containing your client credentials.")
    input("Press Enter after you have created and downloaded the OAuth 2.0 credentials...")
def ensure_client_secrets_file():
    default_path = os.path.join(os.getcwd(), "client_secret.json")
    if not os.path.exists(default_path):
        print(f"Please place your 'client_secret.json' file in the following directory:\n{default_path}")
        input("Press Enter after you have placed the file in the specified directory...")
    return default_path
def main():
    open_google_cloud_console()
    enable_youtube_data_api()
    create_oauth_credentials()

    # Ensure the client secrets file is in the default location
    client_secrets_file = ensure_client_secrets_file()

    # Set up the OAuth 2.0 flow
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Run the OAuth 2.0 flow to get credentials
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()

    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # Get the user's subscriptions
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine=True
    )
    response = request.execute()

    # Print the results
    for item in response["items"]:
        print(f"Title: {item['snippet']['title']}")
        print(f"Channel ID: {item['snippet']['resourceId']['channelId']}\n")
if __name__ == "__main__":
  main()
