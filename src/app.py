import streamlit as st
import pandas as pd
import chardet
from data_pipeline import load_and_validate_csv, compute_summary_statistics

st.title("Quick Dataset Analyzer")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load and validate CSV
        df = load_and_validate_csv(uploaded_file)

        st.success("File uploaded successfully!")
        st.write("Preview of the data:")
        st.dataframe(df.head())

        # Compute and display summary statistics
        st.header("Summary Statistics")

        stats = compute_summary_statistics(df)

        # Data Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Total Null Values", sum(stats['null_counts'].values()))

        # Numerical Statistics
        if stats['numerical_stats']:
            st.subheader("Numerical Columns Statistics")
            num_stats_df = pd.DataFrame.from_dict(stats['numerical_stats'], orient='index')
            num_stats_df = num_stats_df.round(2)
            st.dataframe(num_stats_df)

        # Categorical Statistics
        if stats['categorical_stats']:
            st.subheader("Categorical Columns (Top 5 Values)")
            for col, value_counts in stats['categorical_stats'].items():
                with st.expander(f"📊 {col}"):
                    cat_df = pd.DataFrame(list(value_counts.items()), columns=['Value', 'Count'])
                    st.dataframe(cat_df)

        # Null Values Summary
        st.subheader("Null Values Summary")
        null_df = pd.DataFrame(list(stats['null_counts'].items()), columns=['Column', 'Null Count'])
        null_df = null_df[null_df['Null Count'] > 0]  # Only show columns with nulls
        if not null_df.empty:
            st.dataframe(null_df)
        else:
            st.info("No null values found in the dataset")

        # Data Types
        st.subheader("Column Data Types")
        dtype_df = pd.DataFrame(list(stats['data_types'].items()), columns=['Column', 'Data Type'])
        st.dataframe(dtype_df)

    except UnicodeDecodeError as e:
        st.error(f"Encoding error: Unable to decode the file. Error: {str(e)}")
    except pd.errors.ParserError as e:
        st.error(f"Parsing error: The file does not appear to be a valid CSV. Error: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Please upload a CSV file to get started.")
