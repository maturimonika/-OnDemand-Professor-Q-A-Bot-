from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

def process_and_save_vectors():
    # Load PDF documents from a directory
    #PyPDFDirectoryLoader load and split the pdf present in documents into pages

    loader = PyPDFDirectoryLoader("documents")
    pages = loader.load_and_split()
    print(len(pages))
    #RecursiveCharacterTextSplitter split pages into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=20)
    documents = text_splitter.split_documents(pages)
    print(len(documents))

    # Initialize HuggingFaceEmbeddings for sentence embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create and persist a Chroma vector database from the documents
    vectordb = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory='./data'
    )
    vectordb.persist()

if __name__ == "__main__":
    process_and_save_vectors()
