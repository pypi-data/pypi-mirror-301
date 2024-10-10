class Attachment:
    def __init__(self, attachment_len:int,filename: str,attachment_id:str,attachment_raw_text:str):
        self.attachment_len = attachment_len
        self.filename = filename
        # self.data = data
        self.attachment_id =attachment_id
        self.attachment_raw_text = attachment_raw_text