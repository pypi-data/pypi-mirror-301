from typing import List, Tuple, Dict, Any , Optional
from concurrent.futures import ThreadPoolExecutor
from gmail_connector.gmail_message_parser import MessageParser
from gmail_connector.gmail_message_parser_with_struct_data import StructMessageParser
from gmail_connector.gmail_connector import GmailConnector
import concurrent.futures
import time
import os
from dotenv import load_dotenv
load_dotenv()
class Receiptor:

    def fetch_receipt_data(self,access_token: str, brand_name: Optional[str]=None , add_delay : Optional[bool] = False , enable_logs : Optional[bool] = False , structure_data : Optional[bool] = False,openai_api_key:Optional[str] = os.getenv('OPENAI_API_KEY') , org_id:Optional[str] = os.getenv('ORG_ID')):
        total_processed = 0
        
        page_token = None
        messages = []
        gmail_message_data = []

        
        def fetch_message_wrapper(message_data):
            message_id = message_data.get("id")
            if message_id:
                message_data = GmailConnector.fetch_message(message_id=message_id, access_token=access_token)
                if message_data:
                    if structure_data:
                        print("Structuring the data")
                        return StructMessageParser(message_data=message_data , access_token=access_token).extract_message(message_id=message_id,openai_api_key=openai_api_key , org_id=org_id)
                    return MessageParser(message_data, access_token).extract_message(message_id)
            return None

        while True:
            if enable_logs:
                print(f"Current receipts that are processed: {total_processed}")
            messages, next_page_token = GmailConnector.fetch_emails(
                brand_name=brand_name,
                page_token=page_token,
                access_token=access_token,
            )


            if messages:
                with ThreadPoolExecutor(max_workers=50) as executor:
                    futures=[executor.submit(fetch_message_wrapper, message_data) for message_data in messages]
                    for future in concurrent.futures.as_completed(futures):
                        message = future.result()
                        yield message
                        if message:
                            total_processed += 1
                            
            
            if add_delay:
                time.sleep(5)
                            
            if next_page_token:
                page_token = next_page_token
            else:
                break
        if enable_logs:
            print(f"Total messages processed: {total_processed}")
        return gmail_message_data
