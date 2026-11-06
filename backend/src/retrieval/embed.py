from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#

#import vector store from parent dir
from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

from vector_store import getStore

def embed():
    print("Loading documents...")
    
    docs = (
        PyPDFLoader(str(DATA_DIR / "Company_Policies.pdf")).load()
        + PyPDFLoader(str(DATA_DIR / "Company_Profile.pdf")).load()
        + PyPDFLoader(str(DATA_DIR / "Product_and_Pricing.pdf")).load()
    )
    print("Splitting documents...") 

    chunks = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150).split_documents(docs)
    
    for d in chunks:
        d.page_content = d.page_content.encode("utf-8", "ignore").decode("utf-8", "ignore")

    print(f"Uploading {len(chunks)} chunks to Elasticsearch...")

    # vector_store = getStore("company-documents")
    
    vector_store = getStore("company-documents")

    # vector_store.add_documents(chunks)
    
    print("Successfully indexed into 'company-documents'!")

if __name__ == "__main__":
    embed()

