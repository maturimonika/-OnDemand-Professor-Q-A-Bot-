import os
import sys
import pinecone
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

# Replicate API token
os.environ['REPLICATE_API_TOKEN'] = "r8_VE6i1v4ZJVkljpZPtqIkhIlds9lA4zf2v3c5G"

# Initialize Pinecone
pinecone.init(api_key='b27cd50e-2af7-4233-8366-e79671927418', environment='gcp-starter')

# List of PDF files to process
pdf_files = ['./Slides.pdf', './textbook.pdf']

# Initialize Pinecone vector database
index_name = "mybotpdf"
index = pinecone.Index(index_name)

# Use HuggingFace embeddings for transforming text into numerical vectors
embeddings = HuggingFaceEmbeddings()

# Set up the Conversational Retrieval Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    Replicate(
        model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
        input={"temperature": 0.75, "max_length": 3000}
    ),
    index.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True
)

# Iterate over PDF files
for pdf_file in pdf_files:
    # Load and preprocess the PDF document
    loader = PyPDFLoader(pdf_file)
    documents = loader.load()

    # Split the documents into smaller chunks for processing
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Add documents to Pinecone vector database
    index.upsert(items=texts, ids=[str(i) for i in range(len(texts))], vectors=embeddings.embed(texts))

    # Start chatting with the chatbot for each document
    chat_history = []
    while True:
        query = input('Prompt: ')
        if query.lower() in ["exit", "quit", "q"]:
            print('Exiting')
            sys.exit()
        result = qa_chain({'question': query, 'chat_history': chat_history})
        print('Answer: ' + result['answer'] + '\n')
        chat_history.append((query, result['answer']))
