import os
import json
import tiktoken
from constants import LLM_MODEL , MAX_TOKENS , TEMPERATURE
from utils.helpers import make_request
from models.ocr_text_object import Candidate
from typing import Dict ,Any , Optional
from dotenv import load_dotenv
load_dotenv()

class DocumentStructureExtractor:
    @staticmethod
    def construct_prompt(raw_text: str) -> str:
        system_prompt = f"""Extract information from the following receipt OCR text and return a JSON object with these exact keys: brand, total_cost, location, purchase_category, brand_category, Date, currency, filename, payment_method, metadata.
        Rules:
        1. For total_cost, use the highest monetary value in the text.
        2. For brand_category, choose the closest match from: ["Fashion and Apparel", "Jewelry and Watches", "Beauty and Personal Care", "Automobiles", "Real Estate", "Travel and Leisure", "Culinary Services", "Home and Lifestyle", "Technology and Electronics", "Sports and Leisure", "Art and Collectibles", "Health and Wellness", "Stationery and Writing Instruments", "Children and Baby", "Pet Accessories", "Financial Services", "Airline Services", "Accommodation Services", "Beverages Services", "Services", "Insurance"]
        3. Format Date as dd-mm-yyyy. Strictly return the date in the format dd-mm-yyyy.
        4. For metadata field, return a json which gives summary of the receipt. Only consider the insurance receipt, return metadata json with fields like insurance_number, insurance_expiry, agent_details etc. metadata field will have only a json object strictly that summarize the receipt contents provided, if not an insurance receipt add it as null. 
        5. Use currency codes (e.g., USD, EUR) instead of symbols.
        6. Generate filename as 'PURCHASE_TYPE_BRAND_DATE' (e.g., 'clothing_gucci_20230715').
        7. If a value is not found, return null.
        8. If all values are null, return null.
        Ensure strictly that output is a valid JSON object containing strictly the above keys, without any explanations.
        Here's the OCR text below analyse it and convert into json using keys provided in first line and using the rules provided in rules section:\n\n
        {raw_text}\n
        Generate a JSON response in the following format without using the ```json block. Ensure the output is properly formatted as plain text JSON.\n
        \n
        """
        return system_prompt
    @staticmethod
    def ensure_token_limit( text: str,max_tokens:int,llm_model :Optional[str] = 'gpt-4o-mini') -> str:
        tokenizer = tiktoken.encoding_for_model(llm_model)
        tokens = tokenizer.encode(text)
        
        if len(tokens) > max_tokens:
            truncated_tokens = tokens[:max_tokens]
            truncated_text = tokenizer.decode(truncated_tokens)
            print("Truncated text")
            return truncated_text
        else:
            return text
    
    @staticmethod
    def structure_document_data(raw_text: str,openai_api_key: Optional[str] = None, org_id: Optional[str] = None,
                  llm_model: Optional[str] = LLM_MODEL, max_tokens: Optional[int] = MAX_TOKENS ,
                  temperature: Optional[float] = TEMPERATURE) -> Dict[str, Any]:
        prompt_to_llm = DocumentStructureExtractor.construct_prompt(raw_text)

        if openai_api_key is None:
            raise ValueError("OpenAI API key is but not provided.")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }   

        if org_id is not None:
            headers["OpenAI-Organization"] = org_id

        data = {
            "model": llm_model,
            "max_tokens": max_tokens, 
            "messages": [{"role": "user", "content": prompt_to_llm}],
            "temperature": temperature
        }

        try:
            output = make_request(url, headers=headers, data=data,method='POST')
            print("API Response:", output)
            content = output['choices'][0]['message']['content']
            print("Extracted Content:", content)
            
            candidate_data = json.loads(content)
            
            if isinstance(candidate_data.get('metadata'), dict):
                candidate_data['metadata'] = json.dumps(candidate_data['metadata'])
            elif candidate_data.get('metadata'):
                candidate_data['metadata'] = str(candidate_data['metadata'])
            else:
                candidate_data['metadata'] = None
            
            return candidate_data
        except Exception as e:
            print(f"Request failed: {e}")
            return None