from pydantic import BaseModel, Field

class MeasurementDetails(BaseModel):
    name: str = Field(
        ...,
        description="Name of the component for measurement.",
    )
    property: str = Field(
        ...,
        description="Measurement property for the component.",
    )
    value: str = Field(
        ...,
        description="Value of the measurement property of the component",
    )
    unit: str = Field(
        ...,
        description="measurement unit for the property of the component",
    )
    


