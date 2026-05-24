from typing import Optional, Literal
from pydantic import BaseModel, Field, computed_field, field_validator
from config.cities import tier_1_cities, tier_2_cities # you can import vairibales also..

# from other file you can import class, variables, functions..

class Insurance(BaseModel):
    age:int
    weight:float = Field(gt=0, description="Weight of the person")
    height: float = Field(gt=0, description="Height of the person")
    income_lpa: float
    smoker: Literal['True', "False"]
    city: str = Field(max_length=30)
    occupation: str = Field(max_length=30)

    @field_validator('city')
    @classmethod
    def title(cls,value):
        v = value.title()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker=="True" and self.bmi > 30:
            return "High"
        elif self.smoker=="True" or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
