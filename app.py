import os
import sys
import csv
import json
import asyncio
from dotenv import load_dotenv
from utils.utils import MeasurementDetails
from langchain.llms import AzureOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader
from kor import extract_from_documents, from_pydantic, create_extraction_chain
from langchain.document_loaders import WebBaseLoader
from langchain.callbacks import get_openai_callback

load_dotenv()



# parsed_csv_file = 'data/ipg230103.csv'




# # loading the csv file
# maxInt = sys.maxsize
# csv.field_size_limit(maxInt)
# loader = CSVLoader(file_path=parsed_csv_file)

# data = loader.load()


# for row in data:
#     print(len(row))
#     docs = row.copy()
#     break



def extract_json_info(json_data):
    for record in json_data:
        measurement_list = record.get('data', {}).get('measurementdetails', [])
        for measurement in measurement_list:
            name = measurement.get('name', '')
            property = measurement.get('property', '')
            value = measurement.get('value', '')
            unit = measurement.get('unit', '')
            
            

            print(f'Component Name: {name}\nProperty: {property}\nValue: {value}\nunit: {unit}\n')




async def main():  

    # docs = (data[0])
    loader = WebBaseLoader("https://patents.google.com/patent/US8022010B2/en")
    docs = loader.load()





    llm = AzureOpenAI(
        deployment_name="gpt-35-turbo",
        model_name="gpt-35-turbo",
    )




    # #Splitting the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap  = 200,
        length_function = len,
    )


    docs_chunks = text_splitter.split_documents(docs)




    schema, validator = from_pydantic(
        MeasurementDetails,
        description="Extract component information from the documents including their name, property, property value and property measurement unit.",
        examples=[
            (
                "the resulting BaCO3 had a crystallite size of between about 20 and 40 nm.",
                {"name": "BACO3", "property": "crystallite size", "value": "between 20 and 40", "unit": "nm"},
            )
        ],
        many=True,
    )

    chain = create_extraction_chain(
        llm,
        schema,
        encoder_or_encoder_class="json",
        validator=validator,
        input_formatter="triple_quotes",
    )



    with get_openai_callback() as cb:  
        document_extraction_results =  await extract_from_documents(
            chain,
            docs_chunks[25:30], 
            max_concurrency=5, 
            use_uid=False, 
            return_exceptions=True
        )
    
        # print(f"Total Tokens: {cb.total_tokens}")
        # print(f"Prompt Tokens: {cb.prompt_tokens}")
        # print(f"Completion Tokens: {cb.completion_tokens}")
        # print(f"Successful Requests: {cb.successful_requests}")
        # print(f"Total Cost (USD): ${cb.total_cost}")
            
    
    extract_json_info(document_extraction_results)


asyncio.run(main())