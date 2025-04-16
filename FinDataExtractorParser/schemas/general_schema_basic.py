from pydantic import BaseModel, Extra, Field

class CompanyInfo(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    website: str

class PersonalInfo(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    bank_account_number: str

class FinancialData(BaseModel):
    personal_Info: PersonalInfo
    company_Info: CompanyInfo
    financial_info: dict = Field(..., description="This is where the financial data will go")

    class Config:
        extra = 'allow'  # Allow extra fields to be added by Ollama