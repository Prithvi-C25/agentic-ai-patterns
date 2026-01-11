import os

import mlflow
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
