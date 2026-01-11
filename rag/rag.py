import os

import mlflow
from dotenv import load_dotenv
from langchain_community.document_loaders import ArxivLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from mlflow.genai.scorers import Correctness, ExpectationsGuidelines, RelevanceToQuery

from .config import CONFIG

mlflow.set_experiment("LangChain-RAG-MLflow")
mlflow.langchain.autolog()

# Load and process documents
loader = ArxivLoader(
    query="1706.03762",
    load_max_docs=1,
)

docs = loader.load()
print(docs[0].metadata)

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CONFIG["chunk_size"],
    chunk_overlap=CONFIG["chunk_overlap"],
)
chunks = splitter.split_documents(docs)


# Join chunks in a single string
def join_chunks(chunks: list) -> str:
    return "\n\n".join(chunk.page_content for chunk in chunks)


load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("ENDPOINT")
MODEL = os.getenv("DEPLOYMENT_NAME")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_DEPLOYMENT_NAME", MODEL
)  # Use same as MODEL if not set

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, base_url=BASE_URL, temperature=0)

# Create Embeddings and a Vector Store
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=API_KEY, base_url=BASE_URL)

# Create a vector store from documents
vectorstor = InMemoryVectorStore.from_documents(chunks, embeddings)

# Create a retriever from the vector store
retriever = vectorstor.as_retriever(search_kwargs={"k": CONFIG["retriever_k"]})
