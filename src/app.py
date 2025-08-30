import streamlit as st
import pandas as pd
import chardet

st.title("Quick Dataset Analyzer")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Detect encoding
        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

        # Reset file pointer
        uploaded_file.seek(0)

        # Try to read CSV with detected encoding
        df = pd.read_csv(uploaded_file, encoding=encoding)

        st.success("File uploaded successfully!")
        st.write("Preview of the data:")
        st.dataframe(df.head())

    except UnicodeDecodeError as e:
        st.error(f"Encoding error: Unable to decode the file. Detected encoding: {encoding}. Error: {str(e)}")
    except pd.errors.ParserError as e:
        st.error(f"Parsing error: The file does not appear to be a valid CSV. Error: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Please upload a CSV file to get started.")
