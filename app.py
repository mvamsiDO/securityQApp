import streamlit as st
import pandas as pd
import time
import json
from chatbot import ask_question  # Import the function from chatbot.py

def process_security_questions(uploaded_file):
    """
    Process security questions from an Excel file and get answers using the chatbot.
    
    Args:
        uploaded_file: The uploaded Excel file
    
    Returns:
        DataFrame with questions and answers
    """
    try:
        df = pd.read_excel(uploaded_file)
        
        # Find the questions column
        question_col_index = None
        for i, col in enumerate(df.columns):
            if 'question' in str(col).lower():
                question_col_index = i
                break
        
        if question_col_index is None:
            st.error("Could not find a column containing 'question' in its name")
            return None
        
        answers = []
        progress_bar = st.progress(0)
        num_rows = len(df)
        
        for i in range(num_rows):
            question = str(df.iloc[i, question_col_index])
            st.write(f"Processing question {i+1}: {question}")
            response = ask_question(question)
            try:
                # Parse the JSON response from the agent
                content = response["choices"][0]["message"]["content"]
                print("content", content)
                answer_data = json.loads(content)
            except Exception as e:
                answer_data = {
                    "answer": "Not Sure",
                    "reasoning": "Failed to get a proper response",
                }
            answers.append(answer_data)
            progress_bar.progress((i + 1) / num_rows)
            time.sleep(1)  # Delay to avoid overwhelming the endpoint
        
        # Add the results to the DataFrame as new columns
        df["Answer"] = [a.get("answer", "") for a in answers]
        df["Reasoning"] = [a.get("reasoning", "") for a in answers]
        
        return df
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# Main Streamlit app
st.title("Security Policy Q&A Agent")

st.markdown("Upload an Excel file (.xlsx) containing your security questions.")
uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

if uploaded_file is not None:
    if st.button("Process Questions"):
        processed_df = process_security_questions(uploaded_file)
        
        if processed_df is not None:
            st.write("Processed Data:", processed_df)

            # Create a CSV file for download
            csv = processed_df.to_csv(index=False)
            
            # Offer the CSV for download
            st.download_button(
                "Download Processed CSV",
                csv,
                "Processed_Questions.csv",
                "text/csv",
                key='download-csv'
            )