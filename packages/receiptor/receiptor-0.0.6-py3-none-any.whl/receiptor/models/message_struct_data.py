from typing import Optional, List
from models.attachment import Attachment

class MessageStruct:              
    def __init__(self, message_id: str, body: Optional[str], attachments: Optional[List[Attachment]], company: str ,structured_data:Optional[List]):
        self.id = message_id
        self.body = body
        self.attachments = attachments
        self.company = company
        self.structured_data = structured_data

    def to_json(self) -> Optional[dict]:
        data = {
            "message_id": self.id,
            "body": self.body,
            "company":self.company,
            "attachment_extension": self.attachments[0].filename.split(".")[-1] if self.attachments.__len__() > 0 else None,
            "attachment_id":self.attachments[0].attachment_id if self.attachments.__len__() > 0 else None,
        }
        try:
            if self.structured_data:
                data.update(self.structured_data[0])
            return data
        except:
            return None