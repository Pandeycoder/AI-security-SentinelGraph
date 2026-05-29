from pydantic import BaseModel, HttpUrl

class WebsiteScanRequest(BaseModel):
    url: str
