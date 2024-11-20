import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access the OpenAI API key
open_api_key = os.getenv("OPEN_API_KEY")

# App header
st.title("📄 DocuQuery AI")
st.subheader("Ask Questions and Extract Insights from Your Documents Effortlessly")

# Sidebar for file upload
st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF file to get started", type="pdf")

if uploaded_file:
    # Extract text from uploaded PDF
    pdf_reader = PdfReader(uploaded_file)
    document_text = ""
    for page in pdf_reader.pages:
        document_text += page.extract_text()

    # Display success message
    st.sidebar.success("Document uploaded successfully!")

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=400,
        chunk_overlap=150,
        length_function=len,
    )
    chunks = text_splitter.split_text(document_text)

    # Generate embeddings for text chunks
    embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Main app functionality
    st.header("🔍 Document Query")
    user_question = st.text_input("Type your question below:", placeholder="e.g., What is this document about?")

    if user_question:
        # Perform similarity search for relevant chunks
        matched_chunks = vector_store.similarity_search(user_question, k=3)

        # Initialize the LLM
        llm = ChatOpenAI(
            openai_api_key=open_api_key,
            temperature=0,
            max_tokens=1000,
            model_name="gpt-3.5-turbo",
        )

        # Load QA chain
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=matched_chunks, question=user_question)

        # Display the response
        st.write("### 📜 Answer:")
        st.write(response)

else:
    st.info("Please upload a PDF file to start querying.")

# Footer
st.markdown("---")
st.markdown("DocuQuery AI | Powered by OpenAI and LangChain")
