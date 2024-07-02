import sys
import os
import streamlit as st
from threading import Lock

# Ensure these paths are correct relative to your project structure
sys.path.append(os.path.abspath('../../'))
from task3 import DocumentProcessor
from task4 import EmbeddingClient
from task5 import ChromaCollectionCreator

from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Create a lock object to ensure thread safety
lock = Lock()

if __name__ == "__main__":
    st.header("Quizzify")

    # Configuration for EmbeddingClient
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "sample-mission",
        "location": "us-central1"
    }

    screen = st.empty()  # Screen 1, ingest documents
    with screen.container():
        st.header("Quizzify")

        # 1) Initialize DocumentProcessor and Ingest Documents from Task 3
        processor = DocumentProcessor()
        processor.ingest_documents()

        # 2) Initialize the EmbeddingClient from Task 4 with embed config
        with lock:
            embed_client = EmbeddingClient(**embed_config)

        # 3) Initialize the ChromaCollectionCreator from Task 5
        chroma_creator = ChromaCollectionCreator(processor, embed_client)

        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")

            # 4) Use streamlit widgets to capture the user's input
            topic_input = st.text_input("Enter the Quiz Topic")
            num_questions = st.slider("Select Number of Questions", min_value=1, max_value=10, value=5)

            submitted = st.form_submit_button("Generate a Quiz!")
            document = None
            if submitted:
                if not topic_input.strip():
                    st.error("Quiz topic cannot be empty!")
                else:
                    # 5) Use the create_chroma_collection() method to create a Chroma collection from the processed documents
                    try:
                        chroma_creator.create_chroma_collection()
                        st.success("Chroma collection created successfully!")

                        # Test the query_chroma_collection() method
                        document = chroma_creator.query_chroma_collection(topic_input)
                        if document:
                            st.write(document)
                        else:
                            st.error("No matching documents found!")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.write(f"Details: {str(e)}")

    if document:
        screen.empty()  # Screen 2
        with st.container():
            st.header("Query Chroma for Topic, top Document: ")
            st.write(document)


# In task5.py
class ChromaCollectionCreator:
    def __init__(self, processor, embed_model):
        """
        Initializes the ChromaCollectionCreator with a DocumentProcessor instance and embeddings configuration.
        :param processor: An instance of DocumentProcessor that has processed documents.
        :param embed_model: An embedding client for embedding documents.
        """
        self.processor = processor  # This will hold the DocumentProcessor from Task 3
        self.embed_model = embed_model  # This will hold the EmbeddingClient from Task 4
        self.db = None  # This will hold the Chroma collection

    def create_chroma_collection(self):
        """
        Task: Create a Chroma collection from the documents processed by the DocumentProcessor instance.

        Steps:
        1. Check if any documents have been processed by the DocumentProcessor instance. If not, display an error message using streamlit's error widget.

        2. Split the processed documents into text chunks suitable for embedding and indexing. Use the CharacterTextSplitter from Langchain to achieve this. You'll need to define a separator, chunk size, and chunk overlap.

        3. Create a Chroma collection in memory with the text chunks obtained from step 2 and the embeddings model initialized in the class. Use the Chroma.from_documents method for this purpose.

        Instructions:
        - Begin by verifying that there are processed pages available. If not, inform the user that no documents are found.

        - If documents are available, proceed to split these documents into smaller text chunks. This operation prepares the documents for embedding and indexing. Look into using the CharacterTextSplitter with appropriate parameters (e.g., separator, chunk_size, chunk_overlap).

        - Next, with the prepared texts, create a new Chroma collection. This step involves using the embeddings model (self.embed_model) along with the texts to initialize the collection.

        - Finally, provide feedback to the user regarding the success or failure of the Chroma collection creation.

        Note: Ensure to replace placeholders like [Your code here] with actual implementation code as per the instructions above.
        """

        # Step 1: Check for processed documents
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon=":rotating_light:")
            return

        # Step 2: Split documents into text chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = []
        documents = []
        for page in self.processor.pages:
            print(f"Processing page with content: {page[:100]}...")  # Print the first 100 characters for debugging
            split_texts = text_splitter.split_text(page)
            texts.extend(split_texts)
            documents.extend([Document(page_content=chunk) for chunk in split_texts])

        if texts:
            st.success(f"Successfully split pages to {len(texts)} documents!", icon=":white_check_mark:")
            print(f"Total text chunks: {len(texts)}")
        else:
            st.error("No text chunks created!")

        # Step 3: Create the Chroma Collection
        try:
            with lock:
                self.db = Chroma.from_documents(documents, self.embed_model)
            if self.db:
                st.success("Successfully created Chroma Collection!", icon=":white_check_mark:")
            else:
                st.error("Failed to create Chroma Collection!", icon=":rotating_light:")
        except Exception as e:
            st.error(f"Error creating Chroma Collection: {e}")
            print(f"Error creating Chroma Collection: {e}")

    def query_chroma_collection(self, query) -> Document:
        """
        Queries the created Chroma collection for documents similar to the query.
        :param query: The query string to search for in the Chroma collection.

        Returns the first matching document from the collection with similarity score.
        """
        if self.db:
            try:
                docs = self.db.similarity_search_with_relevance_scores(query)
                if docs and len(docs) > 0 and len(docs[0]) > 0:
                    return docs[0][0]  # Ensure you return only the document, not the relevance score
                else:
                    st.error("No matching documents found!", icon=":rotating_light:")
            except Exception as e:
                st.error(f"Error querying Chroma Collection: {e}")
                print(f"Error querying Chroma Collection: {e}")
        else:
            st.error("Chroma Collection has not been created!", icon=":rotating_light:")