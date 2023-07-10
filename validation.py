import json
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




async def main(json_file_path):  
    


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



    
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    
    for _record in data:
        if _record['publication_title'] == 'Process for the production of titanium dioxide, and titanium dioxide obtained thereby':    
            doc = text_splitter.create_documents(f"{_record['abstract']} {_record['descriptions']} {_record['claims']}")   
            docs_chunks = text_splitter.split_documents(doc)
            document_extraction_results =  await extract_from_documents(
                chain,
                docs_chunks, 
                max_concurrency=5, 
                use_uid=False, 
                return_exceptions=True
            )

                
                    
            
            extract_json_info(document_extraction_results)
        else:
            continue
        break




if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--json_file_path", default='data/ipg230103.json', help="validation file")
    
    args = parser.parse_args()
    asyncio.run(main(args.json_file_path))