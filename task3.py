import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import os
import tempfile
import uuid

class DocumentProcessor:
    """
    This class encapsulates the functionality for processing uploaded PDF documents using Streamlit
    and Langchain's PyPDFLoader. It provides a method to render a file uploader widget, process the
    uploaded PDF files, extract their pages, and display the total number of pages extracted.
    """
    def __init__(self):
        self.pages = []  # List to keep track of pages from all documents

    def ingest_documents(self):
        """
        Renders a file uploader in a Streamlit app, processes uploaded PDF files,
        extracts their pages, and updates the self.pages list with the total number of pages.
        """
        # Step 1: Render a file uploader widget
        uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Step 1: Add UUID to the original file name for source file naming
                unique_filename = str(uuid.uuid4()) + "_" + uploaded_file.name
                
                # Step 2: Write the uploaded PDF to a temporary file
                temp_file_path = os.path.join(tempfile.gettempdir(), unique_filename)
                with open(temp_file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())
                
                # Step 3: Process the temporary file
                # Use PyPDFLoader to load the PDF and extract pages
                loader = PyPDFLoader(temp_file_path)
                pages = loader.load()

                # Step 4: Add the extracted pages to the 'pages' list
                self.pages.extend(pages)

                # Clean up by deleting the temporary file
                os.unlink(temp_file_path)

        # Display the total number of pages processed
        st.write(f"Total pages processed: {len(self.pages)}")

# Main Streamlit app logic
if __name__ == "__main__":
    st.title("Task 3: Document Ingestion")
    st.write("Upload PDF files to process them.")
    
    doc_processor = DocumentProcessor()
    doc_processor.ingest_documents()
