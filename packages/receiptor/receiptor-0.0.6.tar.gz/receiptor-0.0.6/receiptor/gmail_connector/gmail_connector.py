from utils.helpers import make_request
from constants import G_BRAND_QUERY,G_QUERY

class GmailConnector:
    @staticmethod
    def fetch_message(message_id: str, access_token: str):
        message_url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}"
        message_data = make_request(message_url, headers={"Authorization": f"Bearer {access_token}"})
        return message_data

    @staticmethod
    def fetch_emails(brand_name: str, page_token: int, access_token: str):
        g_query = G_QUERY
        if brand_name is not None:
            g_query = G_BRAND_QUERY(brand_name)
        
        gmail_url = f"https://www.googleapis.com/gmail/v1/users/me/messages?q={g_query}&maxResults=20"
        if page_token:
            gmail_url += f"&pageToken={page_token}"

        gmail_data = make_request(gmail_url, headers={"Authorization": f"Bearer {access_token}"})

        
        if "messages" in gmail_data:
            return gmail_data['messages'], gmail_data.get("nextPageToken", None)
        
        return [], gmail_data.get("nextPageToken", None)