from pydantic import BaseModel, Field
from kor import extract_from_documents, from_pydantic

class MeasurementDetails(BaseModel):
    name: str = Field(
        ...,
        description="Name of the product, component, or compound being measured.",
    )
    property: str = Field(
        ...,
        description="Property being measured for the product, component, or compound.",
    )
    value: str = Field(
        ...,
        description="Value of the measured property for the product, component, or compound.",
    )
    unit: str = Field(
        ...,
        description="Unit of measurement for the property of the product, component, or compound.",
    )
    sentence: str = Field(
        ...,
        description="The exact sentence from which the measurement was extracted.",
    )


    



def get_schema():
    schema, validator = from_pydantic(
        MeasurementDetails,
        description="Efficiently extract comprehensive component information from documents, encompassing the name, property, value, and measurement unit of the product, component, or compound.",
        examples=[
            (
                "the resulting BaCO3 had a crystallite size of between about 20 and 40 nm.",
                {
                    "name": "BACO3", 
                    "property": "crystallite size", 
                    "value": "between 20 and 40", 
                    "unit": "nm", 
                    "sentence":"the resulting BaCO3 had a crystallite size of between about 20 and 40 nm."
                },
            ),
            (
                "Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm.",
                {
                     "name": "CUBIC BORON NITRIDE", 
                    "property": "average grain size", 
                    "value": "0.5 to 5", 
                    "unit": "µm", 
                    "sentence":"Therefore, the average grain size of the cubic boron nitride of the present invention is preferably 0.5 to 5 µm."
                }
            )
        ],
        many=True,
    )


    return schema, validator