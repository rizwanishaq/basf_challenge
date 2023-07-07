from pydantic import BaseModel, Field

class MeasurementDetails(BaseModel):
    name: str = Field(
        ...,
        description="Name of the product being measured.",
    )
    property: str = Field(
        ...,
        description="Property being measured for the product.",
    )
    value: str = Field(
        ...,
        description="Value of the measured property for the product.",
    )
    unit: str = Field(
        ...,
        description="Unit of measurement for the property of the product.",
    )
    sentence: str = Field(
        ...,
        description="The exact sentence from which the measurement was extracted.",
    )


    


