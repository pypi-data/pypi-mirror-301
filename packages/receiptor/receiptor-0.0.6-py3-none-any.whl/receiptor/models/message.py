from typing import Optional, List
from models.attachment import Attachment

class Message:              
    def __init__(self, message_id: str, body: Optional[str], attachments: List[Attachment], company: str ):
        self.id = message_id
        self.body = body
        self.attachments = attachments
        self.company = company
        

    def to_json(self) -> Optional[dict]:
        data = {
            "message_id": self.id,
            "body": self.body,
            "company":self.company,
            "attachments":self.attachments,
            "attachment_extension": self.attachments[0].filename.split(".")[-1] if self.attachments.__len__() > 0 else None,
        }
        return data