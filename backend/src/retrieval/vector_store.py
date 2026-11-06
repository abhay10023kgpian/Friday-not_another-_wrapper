from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_elasticsearch import ElasticsearchStore

load_dotenv()

def getStore(docName: str) -> ElasticsearchStore:
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        dimensions=512
    )

    vector_store = ElasticsearchStore(
        index_name=docName,
        es_url="http://localhost:9200",
        # es_api_key=os.environ["ES_API_KEY"],
        embedding=embeddings,
        strategy=ElasticsearchStore.ApproxRetrievalStrategy(
            hybrid=True
        ),
    )

    return vector_store
