# Receiptor Package

## Overview

Receiptor is a Python package designed to extract receipt, invoice, and order data from a user's Gmail account. It provides an easy-to-use interface for developers to fetch and structure email data, including attachments. The package also includes a feature that uses LLMs (Language Model Models) to structure the extracted data into JSON format.

## Features

- Extract receipt/invoice/order data from Gmail
- Parse email attachments
- Structure extracted data using LLMs

## Installation

To install the Receiptor package, use pip:

```bash
pip install receiptor
```

## Usage

### 1. Import required modules

```python
from receiptor import Receiptor
from llm_parser.gpt_4o_mini_parser.gpt_4o_mini import DocumentStructureExtractor
from dotenv import load_dotenv
```

### 2. Load environment variables (if needed)

```python
load_dotenv()
```
### 3. You can setup OpenAi Api Keys by : 
 Create a .env file and set the keys as follows : 
  ```python
OPENAI_API_KEY="your api key"
ORG_ID = "org_id" #Optional
```
 API keys can be passed into the function directly. 

 ```python 

structured_data = DocumentStructureExtractor.structure_document_data(
        raw_text=data.attachments[0].attachment_raw_text
        ,openai_api_key = "" , org_id = ""
    )

 ```
### 3. Initialize the Receiptor object

```python
obj = Receiptor()
```

### 4. Set up Gmail access token

Obtain a Gmail access token through the OAuth2 flow. Store this token securely.
```python
access_token = "Your_Gmail_access_token_here"
```

### 5. Fetch and process receipt data

```python

for data in obj.fetch_receipt_data(access_token=access_token):
    print(data)
    if data.attachments:
        # Print the raw text of the first attachment
        print(data.attachments[0].attachment_raw_text)
        
        # Structure the attachment text using DocumentStructureExtractor
        structured_data = DocumentStructureExtractor.structure_document_data(
            raw_text=data.attachments[0].attachment_raw_text
        )
        print(structured_data)


```

## Example Output

### Main Data

```json
{
"message_id": "1dsse2342dfs3",
"body": "body text",
"company": "zomato.com",
"attachments": [
"<models.attachment.Attachment object at 0x1040d45c0>",
"<models.attachment.Attachment object at 0x10407b440>",
"<models.attachment.Attachment object at 0x103f90980>"
],
"attachment_extension": "pdf"
}
```
Attachment Raw Text
```
Zomato Food Order: Summary and Receipt

```
Structured Document Data
```json
{
"brand": "brand name",
"total_cost": "189",
"location": "New york",
"purchase_category": "Food",
"brand_category": "Culinary Services",
"Date": "01-01-2024",
"currency": "INR",
"filename": "filename",
"payment_method": null,
"metadata": null
}
```
Contributing
We welcome contributions to the Receiptor package. Please feel free to submit issues, feature requests, or pull requests on our GitHub repository.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Support

Thank you for using Receiptor! We hope this package simplifies your receipt and invoice data extraction process.
