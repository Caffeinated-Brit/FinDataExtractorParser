from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr, HttpUrl, Extra
#
# class CompanyInfo(BaseModel):
#     name: str
#     address: str
#     phone_number: str
#     email: str
#     website: str
#
# class PersonalInfo(BaseModel):
#     name: str
#     address: str
#     phone_number: str
#     email: str
#     bank_account_number: str
#
# class FinancialData(BaseModel):
#     personal_Info: PersonalInfo
#     company_Info: CompanyInfo
#     financial_info: dict = Field(..., description="This is where the financial data will go")
#
#     class Config:
#         extra = 'allow'  # Allow extra fields to be added by Ollama



class CompanyInfo(BaseModel):
    name: Optional[str] = Field(None, description="Company name")
    address: Optional[str] = Field(None, description="Company address")
    phone_number: Optional[str] = Field(None, description="Company phone number")
    email: Optional[str] = Field(None, description="Company email address")
    website: Optional[HttpUrl] = Field(None, description="Company website URL")

    class Config:
        extra = Extra.ignore  # Ignore unexpected fields
        allow_population_by_field_name = True


class PersonalInfo(BaseModel):
    name: Optional[str] = Field(None, description="Person's full name")
    address: Optional[str] = Field(None, description="Person's home address")
    phone_number: Optional[str] = Field(None, description="Person's phone number")
    email: Optional[str] = Field(None, description="Person's email address")
    bank_account_number: Optional[str] = Field(None, description="Bank account number")

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True


class FinancialData(BaseModel):
    personal_info: Optional[PersonalInfo] = Field(None, alias="personal_Info")
    company_info: Optional[CompanyInfo] = Field(None, alias="company_Info")
    financial_info: Optional[Dict[str, Any]] = Field(
        None, description="Structured or semi-structured financial information"
    )

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True

    def model_dump(self, **kwargs):
        # Only include fields that are not None
        return super().model_dump(exclude_none=True, **kwargs)
