import streamlit as st
import pandas as pd
import time
import json
from io import BytesIO
from chatbot import ask_question  # Import the function from chatbot.py

st.title("Security Policy Q&A Agent")

st.markdown("Upload an Excel file (.xlsx) containing your security questions (first column).")
uploaded_file = st.file_uploader("Upload Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    

    if st.button("Process Questions"):
        answers = []
        progress_bar = st.progress(0)
        num_rows = len(df)
        
        for i in range(num_rows):
            question = str(df.iloc[i, 0])
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
                    "source": ""
                }
            answers.append(answer_data)
            progress_bar.progress((i + 1) / num_rows)
            time.sleep(1)  # Delay to avoid overwhelming the endpoint
        
        # Add the results to the DataFrame as new columns
        df["Answer"] = [a.get("answer", "") for a in answers]
        df["Reasoning"] = [a.get("reasoning", "") for a in answers]
        df["Evidence"] = [a.get("source", "") for a in answers]
        
        st.write("Processed Data:", df)

        # Create an Excel file for download
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Results")
        processed_excel = output.getvalue()

        st.download_button("Download Processed Excel", processed_excel, "Processed_Questions.xlsx")