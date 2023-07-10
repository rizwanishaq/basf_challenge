import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from utils.utils import get_schema
from langchain.llms import AzureOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader
from kor import extract_from_documents, from_pydantic, create_extraction_chain
from langchain.document_loaders import JSONLoader


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
            
            

            print(f'Component Name: {name}\nProperty: {property}\nValue: {value}\nunit: {unit}\nsentence: {sentence}\n')




async def main():  
    llm = AzureOpenAI(
        deployment_name="gpt-35-turbo",
        model_name="gpt-35-turbo",
        temperature=0.0
    )




    # #Splitting the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap  = 200,
    )
    


    schema, validator = get_schema()

    chain = create_extraction_chain(
        llm,
        schema,
        encoder_or_encoder_class="json",
        validator=validator,
        input_formatter="triple_quotes",
    )


    parsed_json_file = 'data/ipg230103.json'


    
    with open(parsed_json_file) as json_file:
        data = json.load(json_file)

    
    for _record in data:
        if _record['publication_title'] == 'Process for the production of titanium dioxide, and titanium dioxide obtained thereby':    
            doc = text_splitter.create_documents([f"{_record['abstract']} {_record['descriptions']} {_record['claims']}"])   
            docs_chunks = text_splitter.split_documents(doc)
            document_extraction_results =  await extract_from_documents(
                chain,
                docs_chunks, 
                max_concurrency=15, 
                use_uid=False, 
                return_exceptions=True
            )

                
                    
            # print(document_extraction_results)
            extract_json_info(document_extraction_results)
        else:
            continue
        break




if __name__ == "__main__":
    asyncio.run(main())