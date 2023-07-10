import os
import asyncio
from dotenv import load_dotenv
from utils.utils import MeasurementDetails
from langchain.llms import AzureOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from kor import extract_from_documents, from_pydantic, create_extraction_chain
from langchain.document_loaders import WebBaseLoader
from argparse import ArgumentParser

load_dotenv()




def extract_json_info(json_data):
    for record in json_data:
        measurement_list = record.get('data', {}).get('measurementdetails', [])
        for measurement in measurement_list:
            name = measurement.get('name', '')
            property = measurement.get('property', '')
            value = measurement.get('value', '')
            unit = measurement.get('unit', '')
            sentence = measurement.get('sentence', '')
            
            

            print(f'Product: {name}\nProperty: {property}\nValue: {value}\nunit: {unit}\nsentence: {sentence}\n')




async def main(patent_url):  
    loader = WebBaseLoader(patent_url)
    # loader = WebBaseLoader("https://patents.google.com/patent/EP2778146A1/en")
    
    docs = loader.load()


    llm = AzureOpenAI(
        deployment_name="gpt-35-turbo",
        model_name="gpt-35-turbo",
        # temperature=0.0
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
        description="Extract component information from documents, including the product's name, property, value, and measurement unit.",
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



    
    document_extraction_results =  await extract_from_documents(
        chain,
        docs_chunks, 
        max_concurrency=10, 
        use_uid=False, 
        return_exceptions=True
    )
    
    
    extract_json_info(document_extraction_results)




if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--patent_url", default='https://patents.google.com/patent/US8022010B2/en', help="patent url which we want to analysis")
    
    args = parser.parse_args()
    asyncio.run(main(args.patent_url))