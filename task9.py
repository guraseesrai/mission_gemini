import streamlit as st
import os
import sys
import json
import logging

sys.path.append(os.path.abspath('../../'))
from task3 import DocumentProcessor
from task4 import EmbeddingClient
from task5 import ChromaCollectionCreator
from task8 import QuizGenerator

logging.basicConfig(level=logging.INFO)

class QuizManager:
    ##########################################################
    def __init__(self, questions: list):
        self.questions = questions
        self.total_questions = len(questions)
    ##########################################################

    def get_question_at_index(self, index: int):
        valid_index = index % self.total_questions
        return self.questions[valid_index]
    
    ##########################################################
    def next_question_index(self, direction=1):
        current_index = st.session_state["question_index"]
        new_index = (current_index + direction) % self.total_questions
        st.session_state["question_index"] = new_index
    ##########################################################

def main():
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "sample-mission",
        "location": "us-central1"
    }
    
    screen = st.empty()
    with screen.container():
        st.header("Quiz Builder")
        processor = DocumentProcessor()
        
        try:
            processor.ingest_documents()
        except Exception as e:
            st.error(f"Error ingesting documents: {e}")
            logging.error(f"Error ingesting documents: {e}")
            return
    
        embed_client = EmbeddingClient(**embed_config)
        chroma_creator = ChromaCollectionCreator(processor, embed_client)
    
        question = None
        question_bank = None
    
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                try:
                    chroma_creator.create_chroma_collection()
                except Exception as e:
                    st.error(f"Error creating Chroma collection: {e}")
                    logging.error(f"Error creating Chroma collection: {e}")
                    return
                
                st.write(topic_input)
                
                generator = QuizGenerator(topic_input, questions, chroma_creator)
                try:
                    question_bank = generator.generate_quiz()
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")
                    logging.error(f"Error generating quiz: {e}")
                    return

    if question_bank:
        screen.empty()
        with st.container():
            st.header("Generated Quiz Question: ")
            
            quiz_manager = QuizManager(question_bank)
            with st.form("Multiple Choice Question"):
                
                index_question = quiz_manager.get_question_at_index(0)
                choices = []
                for choice in index_question['choices']:
                    key = choice['key']
                    value = choice['value']
                    choices.append(f"{key}) {value}")
                
                st.write(f"{index_question['question']}")
                
                answer = st.radio(
                    'Choose the correct answer',
                    choices
                )
                submitted = st.form_submit_button("Submit")
                
                if submitted:
                    correct_answer_key = index_question['answer']
                    if answer.startswith(correct_answer_key):
                        st.success("Correct!")
                    else:
                        st.error("Incorrect!")

if __name__ == "__main__":
    main()
