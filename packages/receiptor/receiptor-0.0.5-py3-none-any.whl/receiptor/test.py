from receiptor import Receiptor
from llm_parser.gpt_4o_mini_parser.gpt_4o_mini import DocumentStructureExtractor
from dotenv import load_dotenv
load_dotenv()

obj = Receiptor() #Initialising the object for the Receiptor class

access_token = "Gmail access token obtained from oauth2 flow "
for data in obj.fetch_receipt_data(access_token=access_token) :
    print(data)    # data contains the extracted receipt / invoice data
    if data.attachments: #This checks if the email contains an attachment or not and then extracts text from the attachment
        print(data.attachments[0].attachment_raw_text)
        print(DocumentStructureExtractor.structure_document_data(raw_text=data.attachments[0].attachment_raw_text,)) # DocumentStructureExtractor structures the text using a json object
