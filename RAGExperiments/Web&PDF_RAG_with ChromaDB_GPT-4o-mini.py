# pip install langchain langchainhub langchain_objectbox langchain_community
#ollama pull llama3.1 -- for 8b model

## References (with modifications) - https://github.com/krishnaik06/Updated-Langchain/blob/main/openai/GPT4o_Lanchain_RAG.ipynb

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain import hub

load_dotenv(os.getcwd()+"/local.env")
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
os.environ['USER_AGENT'] = 'test_agent'
llm_gpt = ChatOpenAI(model="gpt-4o-mini") ## Calling Gpt-4o-mini
prompt = hub.pull("rlm/rag-prompt")
print(prompt)
llm_ollama = ChatOllama(                  ## Calling llama3.1
    model="llama3.1",
    temperature=.7,
)

ef_openai = OpenAIEmbeddings()

# 1. Get a Data Loader

print("Loading from the Web")
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
data = loader.load()
data

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(data)
documents

# 2. Add Web data to Vector Database

# persist to disk
vector = Chroma.from_documents(collection_name="test_chroma_db", documents=documents, embedding=ef_openai, persist_directory='RAGExperiments/chromaDB') 
print(vector)

# 3. Repeat for PDFs

print("Loading from the PDF")
path_to_pdfs = 'RAGExperiments/pdfFiles/'
pdf_splits = []
if os.path.exists(path_to_pdfs):
    print("Steps ++++\n1..")
    file_list = os.listdir(path_to_pdfs)
    if len(file_list) > 0:
        print("2..")
        for file in file_list:
            print("3..")
            file = os.path.join(path_to_pdfs,file)
            print(file)
            loader = PyPDFLoader(file)
            data = loader.load()
            print("4..")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=200,
                length_function=len
            )
            pdf_splits.extend(text_splitter.split_documents(data))

# 4. Add PDF data to Vector Database
if pdf_splits is not []:
    vector.add_documents(pdf_splits,embedding=ef_openai)
print(vector)

# 5. Make a RAG pipeline

qa_chain = RetrievalQA.from_chain_type(
        llm_gpt,
        retriever=vector.as_retriever(),
        chain_type_kwargs={"prompt": prompt}
    )

question = "How is Langchain used" # "Explain Monitoring and A/B Testing in langsmith"
result = qa_chain.invoke({"query": question })
print(result)

print(result["result"])

import pprint
pp = pprint.PrettyPrinter(indent=5)
pp.pprint(result["result"])


# Other Trials
#-------------------

# from langchain.embeddings import SentenceTransformerEmbeddings
#from langchain_huggingface import HuggingFaceEmbeddings
# import chromadb
# from chromadb.utils import embedding_functions

# ef_openai = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key=os.environ["OPENAI_API_KEY"],
#                 model_name="gpt-4o-mini"
            # )
# client = chromadb.Client()
# vector = client.get_or_create_collection("oscars-2023",embedding_function=openai_ef)
#embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")