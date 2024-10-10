import re
import base64
from models.message import Message
from models.attachment import Attachment
from constants import personalDomains_set
from utils.helpers import make_request
from ocr.text_extractor import DocumentTextExtractor
from typing import Optional, List, Dict
from bs4 import BeautifulSoup


class MessageParser:


    def __init__(self, message_data: dict, access_token: str) -> None:
        self.message_data = message_data
        self.access_token = access_token

    def extract_message(self, message_id: str):
        subject = MessageParser.extract_subject_from_mail(self.message_data)
        company_from_mail = MessageParser.extract_domain_name(
            self.message_data['payload']['headers'], subject)
        body = MessageParser.extract_body_from_mail(self.message_data)
        attachments = MessageParser.extract_attachments_from_mail(
            access_token=self.access_token, message_data=self.message_data)
        
        return Message(message_id=message_id, body=body, attachments=attachments, company=company_from_mail)

    @staticmethod
    def extract_text_from_html_body(html_content: str) -> str:
        if not html_content:
            raise ValueError("HTML content is empty or None")

        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ')
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    @staticmethod
    def extract_body_from_mail(message_data: dict) -> str:
        body = None
        if "payload" in message_data:
            payload = message_data["payload"]
            if "parts" in payload:
                for part in payload["parts"]:
                    if 'mimeType' in part and (part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html'):
                        body_data = part['body'].get('data', '')
                        if body_data:
                            body_base64 = base64.urlsafe_b64decode(body_data)
                            body = MessageParser.extract_text_from_html_body(
                                body_base64)

            elif 'body' in payload:
                body_data = payload['body'].get('data', '')
                if body_data:
                    body_base64 = base64.urlsafe_b64decode(body_data)
                    body = MessageParser.extract_text_from_html_body(
                        body_base64)
            elif 'parts' in payload['body']:
                for part in payload['body']['parts']:
                    if 'mimeType' in part and (part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html'):
                        body_data = part['body'].get('data', '')
                        if body_data:
                            body_base64 = base64.urlsafe_b64decode(body_data)
                            body = MessageParser.extract_text_from_html_body(
                                body_base64)

        if not body:
            body = message_data.get('snippet', '')
        return body
    @staticmethod
    def extract_html_from_mail(message_data: dict) -> str:
        html_body = None
        if "payload" in message_data:
            payload = message_data["payload"]
            if "parts" in payload:
                for part in payload["parts"]:
                    if 'mimeType' in part and part['mimeType'] == 'text/html':
                        body_data = part['body'].get('data', '')
                        if body_data:
                            html_body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                            break

            elif 'body' in payload:
                body_data = payload['body'].get('data', '')
                if body_data:
                    html_body = base64.urlsafe_b64decode(body_data).decode('utf-8')

            elif 'parts' in payload['body']:
                for part in payload['body']['parts']:
                    if 'mimeType' in part and part['mimeType'] == 'text/html':
                        body_data = part['body'].get('data', '')
                        if body_data:
                            html_body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                            break

        if not html_body:
            html_body = f"<html><body>{message_data.get('snippet', '')}</body></html>"

        return html_body
    @staticmethod
    def extract_domain_name(payload: dict, subject: str) -> str:
        def extract_domain_from_email(email_string: str) -> Optional[str]:
            email_address = re.search(
                r'[\w\.-]+@[\w\.-]+', email_string).group()
            domain = email_address.split('@')[-1]
            if email_address and domain:
                return domain
            else:
                return None

        domain_name = 'others'
        for fromdata in payload:
            if fromdata['name'] == 'From':
                domain_name = extract_domain_from_email(fromdata['value'])
                break

        if domain_name in personalDomains_set:
            print(f"Skipping email from {domain_name} as it belongs to a personal domain.")
            return None

        if 'chanel' in subject.lower():
            return 'chanel'
        if 'louis vuitton' in subject.lower():
            return 'Louis Vuitton'
        return domain_name
    @staticmethod
    def extract_subject_from_mail(message_data: dict) -> str:
        if 'payload' in message_data and 'headers' in message_data['payload']:
            headers = message_data['payload']['headers']
            for header in headers:
                if header['name'] == 'Subject':
                    return header['value']
            return ""
        else:
            return ""
    @staticmethod
    def fetch_attachment_data(access_token: str, message_id: str, attachment_id: str) -> Dict:
        attachment_url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}/attachments/{attachment_id}"
        attachment_response = make_request(attachment_url, headers={"Authorization": f"Bearer {access_token}"})
        return attachment_response
    
    @staticmethod
    def extract_attachments_from_mail(access_token: str, message_data: dict) -> List[Attachment]:
        attachments = []
        structured_data = []
        st_str = {
            "brand": "INSERT BRAND NAME",
            "total_cost": "INSERT TOTAL COST",
            "location": "INSERT LOCATION FROM",
            "purchase_category": "INSERT PURCHASE CATEGORY",
            "brand_category": "INSERT BRAND CATEGORY",
            "Date": "INSERT RECEIPT DATE",
            "currency": "INSERT CURRENCY",
            "filename": "GENERATE A FILENAME",
            "payment_method": "INSERT PAYMENT METHOD"
        }
        
        struct_data = None
                    
        if "payload" in message_data and "parts" in message_data["payload"]:
            for part in message_data["payload"]["parts"]:
                if "body" in part and "attachmentId" in part["body"]:
                    attachment_id = part["body"]["attachmentId"]
                    attachment_data = MessageParser.fetch_attachment_data(
                        access_token, message_data["id"], attachment_id)
                    
                    if not attachment_data:
                        continue
                    
                    data = attachment_data.get("data", "")

                    filename = part.get("filename", "untitled.txt")
                    if filename.endswith(".zip") or filename.endswith(".ics") or filename.endswith(".txt") or filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".gif"):
                        continue

                    attachments.append(Attachment(attachment_len=len(attachment_data.get(
                        "data", "")), filename=filename,attachment_id=attachment_id , attachment_raw_text = DocumentTextExtractor.extract_text_from_attachment(filename=filename , data=data)))

        return attachments