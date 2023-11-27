from langchain.vectorstores import Chroma
from langchain.llms import GPT4All
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings

# Load the previously saved vector database
local_db = "./data"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory=local_db, embedding_function=embeddings)
# Initialize GPT-4 language model
local_path = "./model/orca-mini-3b-gguf2-q4_0.gguf"
llm = GPT4All(model=local_path, backend="gptj", verbose=False)

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    verbose=False,
)

# Start a loop for user interaction
while True:
    # Get user input
    user_input = input("Ask a question (type 'exit' to quit): ")

    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        print("Exiting...")
        break

    # Query the QA chain
    result = qa_chain(user_input)
    # print("result",result)
# Extract the first answer and its citation
    if result['result']:
        first_answer = result['result']
        print(f"Answer: {first_answer}")
    else:
        print("No answer found.\n")
    
    if result['source_documents']:
    #    first_citation = result['source_documents'][0].metadata.get('page', 'Unknown Page')
       first_citation = result['source_documents'][0].metadata
       print(f"Citation: Page {first_citation}\n")
    
