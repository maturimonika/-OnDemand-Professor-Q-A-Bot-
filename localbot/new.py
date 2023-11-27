from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

loader = PyPDFDirectoryLoader("documents")
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load docs into Chroma DB
db = Chroma.from_documents(docs, embedding_function)

# query the DB
query = "What is Rachel Green's Address"
docs = db.similarity_search(query)

# print results
print(docs[0].page_content)

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# documents = text_splitter.split_documents(pages)

# vectordb = Chroma.from_documents(
#     documents,
#     persist_directory='./data'
# )
# vectordb.persist()