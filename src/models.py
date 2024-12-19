from dataclasses import dataclass

@dataclass
class Company:
    company_name : str
    contact_name : str
    address : str
    website : str
    email : str
    company_description : str
    member_since : str
    tags : str
    location : str