import os
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from utils.utils import MeasurementDetails
from kor import extract_from_documents, from_pydantic, create_extraction_chain




# https://colab.research.google.com/drive/1Hj55qsYgHX9mMC_81BwpjORIEjajxOPp?usp=sharing#scrollTo=Kk3c8z0PBgeI

# // TODO:  one-shot inference
# // TDOD:  Chunking the pdf/website



# # OpenAI API key
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
)





#Splitting the documents into chunks
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
    encoder_or_encoder_class="csv",
    validator=validator,
    input_formatter="triple_quotes",
)




document_extraction_results = extract_from_documents(
    chain,
    docs_chunks, 
    max_concurrency=5, 
    use_uid=False, 
    return_exceptions=True
)
    

print(document_extraction_results)