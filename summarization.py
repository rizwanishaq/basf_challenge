from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader
from langchain.llms import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

loader = WebBaseLoader("https://patents.google.com/patent/US8022010B2/en")
doc = loader.load()



llm = AzureOpenAI(
    deployment_name="gpt-35-turbo",
    model_name="gpt-35-turbo",
    temperature=0
)


# #Splitting the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap  = 200,
    length_function = len,
)


docs_chunks = text_splitter.split_documents(doc)


chain = load_summarize_chain(llm, chain_type="map_reduce")
print(chain.run(docs_chunks))