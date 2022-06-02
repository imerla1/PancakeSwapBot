from lib2to3.pytree import Base
from pydantic import BaseModel

class SmtpConfigSchema(BaseModel):
    smtp_server: str
    smtp_port: int
    sender: str
    password: str
    
class TwillioConfigSchema(BaseModel):
    account_sid: str
    auth_token: str
    from_number: str
