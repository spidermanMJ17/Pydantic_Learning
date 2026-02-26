# def insert_patient_data(name: str, age: int):
#     if type(name)==str and type(age)==int: 
#         print(name)
#         print(age)
#         print('updated in Database')
#     else:
#         raise TypeError('name should be string and age should be in int')

# insert_patient_data('Meet', '21')

# from pydantic import BaseModel, EmailStr, AnyUrl, Field
# from typing import List, Dict, Optional, Annotated

# class contact_details(BaseModel):
#     email: EmailStr
#     phone: str

# class patient(BaseModel):
#     name: Annotated[str, Field(max_length=50, title='Name of the patient', description='It should be less than 50', examples=['Meet', 'Mann'])]
#     age: int
#     linkedin_url : AnyUrl
#     gmail : EmailStr
#     weight : Annotated[float, Field(gt=0, strict=True)] #strict will stop allowing TypeVersion
#     married : Annotated[bool, Field(default=False, description='Is patient Married?')]
#     # allergies: Optional[List[str]] = None
#     allergies: Optional[List[str]] = Field(default=None, max_length=10)
#     # allergies : Annotated[optional[List[str]], Filed(default=None, max+length=10)]
#     contact_details :contact_details

# def insert_patient_info(patient1 : patient):
#     print(patient1.name)
#     print(patient1.age)
#     print(patient1.contact_details.phone)
#     print(patient1.married)
#     print(patient1.allergies)
#     print('Entry inserted into database')

# patient_info = {'gmail':'xyz@gmail.com', 'linkedin_url':'https://linkedin.com/1718', 'name':'Meet', 'age':21, 'weight' : 74.2, 'contact_details': {'email': 'abc@gmail.com', 'phone':'0123456789'}}
# patient1 = patient(**patient_info)

# insert_patient_info(patient1)

# FIELD VALIDATOR

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class contact_details(BaseModel):
    email: EmailStr
    phone: str
    emergency : Optional[str] = None

class patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='It should be less than 50', examples=['Meet', 'Mann'])]
    age: int
    linkedin_url : AnyUrl
    gmail : EmailStr
    height : Annotated[float, Field(gt=0, strict=True)] #m
    weight : Annotated[float, Field(gt=0, strict=True)] #kg
    #strict will stop allowing TypeVersion
    married : Annotated[bool, Field(default=False, description='Is patient Married?')]
    # allergies: Optional[List[str]] = None
    allergies: Optional[List[str]] = Field(default=None, max_length=10)
    # allergies : Annotated[optional[List[str]], Filed(default=None, max_length=10)]
    contact_details :contact_details

    @field_validator('gmail')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'sbi.com']
        check_data = value.split('@')[-1]
        if check_data not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name')
    @classmethod
    def uppercase_name(cls,value):
        return value.upper()
    
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls,value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in valid range')
        
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 65 and not model.contact_details.emergency:
            raise ValueError('Patient above age 65 must have Emergency contact')
        else:
            return model

    @computed_field
    # @property
    def calculate_bmi(self) -> float:
        bmi_value = round(self.weight / (self.height**2), 2)
        return bmi_value

def insert_patient_info(patient1 : patient):
    # print(patient1.name)
    # print(patient1.age)
    # print(patient1.contact_details.phone)
    # print(patient1.married)
    # print(patient1.allergies)
    print(f'Bmi value of the patient is {patient1.calculate_bmi}')
    print('Entry inserted into database')

contact_details_patient = {'email': 'abc@gmail.com', 'phone':'0123456789', 'emergency' : '+919624617801'}
contact1 = contact_details(**contact_details_patient)

patient_info = {'gmail':'xyz@hdfc.com', 'linkedin_url':'https://linkedin.com/1718', 'name':'Meet', 'age':69, 'weight' : 74.2, 'contact_details': contact1, 'height': 1.72}

patient1 = patient(**patient_info)

insert_patient_info(patient1)

# temp = patient1.model_dump()
# print(temp)
# print(type(temp))

# temp_json = patient1.model_dump_json(exclude={'contact_details':['emergency']})
# print(temp_json)
# print(type(temp_json))

# temp = patient1.model_dump(exclude_unset=True)
# print(temp)
# print(type(temp))