import streamlit as st
from PyPDF2 import PdfWriter
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
import os

# Access the shared secret
open_api_key = st.secrets["OPEN_API_KEY"]

if not open_api_key:
    raise ValueError("API key not found.")

# Inject custom CSS
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f8f9fa;
    }
    .css-18e3th9 {
        padding: 2rem;
    }
    h1 {
        color: #4CAF50;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    h2, h3 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .st-sidebar {
        background-color: #f3f4f6;
        padding: 2rem 1rem;
    }
    .stSidebar .stButton {
        color: white;
        background-color: #007BFF;
    }
    .st-file-uploader {
        margin: 1rem 0;
    }
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #ccc;
        padding: 0.5rem;
        font-size: 1rem;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        font-size: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: none;
        margin-top: 1rem;
    }
    .stMarkdown {
        color: #34495e;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main application header
st.header("📄 DocuQuery AI: Intelligent Document Assistant", divider=True)

# Sidebar for document upload
with st.sidebar:
    st.title("📂 Upload Your Document")
    st.markdown("Use the uploader below to select your PDF file.")
    file = st.file_uploader("Upload a PDF file to ask questions and extract insights:", type="pdf")

# Process the uploaded file
if file is not None:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # Split the document into smaller chunks for efficient processing
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=400,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Generate embeddings for the text chunks
    embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)

    # Create a vector store for similarity search
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Input field for user queries
    user_question = st.text_input(
        "💬 Ask a question about your document:",
        placeholder="Type your question here:"
    )

    # Perform similarity search and generate response
    match = None
    if user_question:
        match = vector_store.similarity_search(user_question)

    # Define the language model
    llm = ChatOpenAI(
        openai_api_key=open_api_key,
        temperature=0,
        max_tokens=1000,
        model_name="gpt-3.5-turbo"
    )

    # Provide the answer if relevant matches are found
    if match:
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=match, question=user_question)
        st.markdown(f"### 📜 Response:\n{response}")







# import streamlit as st
# from PyPDF2 import PdfWriter
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain.chains.question_answering import load_qa_chain
# from langchain_openai.chat_models import ChatOpenAI
# from langchain_community.vectorstores import FAISS
# from dotenv import load_dotenv
# import os

# # # Load environment variables
# # load_dotenv()
# # # Access the OpenAI API key
# # open_api_key = os.getenv("OPEN_API_KEY")

# # Access the shared secret
# open_api_key = st.secrets["OPEN_API_KEY"]

# if not open_api_key:
#     raise ValueError("API key not found.")

# # Main application header
# st.header("📄 DocuQuery AI: Intelligent Document Assistant", divider=True)

# # Sidebar for document upload
# with st.sidebar:
#     st.title("📂 Upload Your Document")
#     file = st.file_uploader("Upload a PDF file to ask questions and extract insights:", type="pdf")

# # Process the uploaded file
# if file is not None:
#     pdf_reader = PdfReader(file)
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text()

#     # Split the document into smaller chunks for efficient processing
#     text_splitter = RecursiveCharacterTextSplitter(
#         separators="\n",
#         chunk_size=400,
#         chunk_overlap=150,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(text)

#     # Generate embeddings for the text chunks
#     embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)

#     # Create a vector store for similarity search
#     vector_store = FAISS.from_texts(chunks, embeddings)

#     # Input field for user queries
#     user_question = st.text_input("💬 Ask a question about your document:", placeholder="Type your question here...")

#     # Perform similarity search and generate response
#     match = None
#     if user_question:
#         match = vector_store.similarity_search(user_question)

#     # Define the language model
#     llm = ChatOpenAI(
#         openai_api_key=open_api_key,
#         temperature=0,
#         max_tokens=1000,
#         model_name="gpt-3.5-turbo"
#     )

#     # Provide the answer if relevant matches are found
#     if match:
#         chain = load_qa_chain(llm, chain_type="stuff")
#         response = chain.run(input_documents=match, question=user_question)
#         st.write(response)
