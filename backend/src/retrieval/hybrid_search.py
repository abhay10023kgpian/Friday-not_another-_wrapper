import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone import Pinecone, ServerlessSpec
from pinecone_text.sparse import BM25Encoder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_elasticsearch import ElasticsearchStore

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    dimensions=512
)

vector_store = ElasticsearchStore(
    index_name="company-documents",
    es_url="http://localhost:9200",
    # es_api_key=os.environ["ES_API_KEY"],
    embedding=embeddings,
    strategy=ElasticsearchStore.ApproxRetrievalStrategy(
        hybrid=True
    ),
)

# vector_store.add_documents(docs)