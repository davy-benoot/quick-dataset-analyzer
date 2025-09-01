import streamlit as st
import pandas as pd
from data_pipeline import (
    load_and_validate_csv,
    compute_summary_statistics,
    get_max_file_size_mb,
    get_numerical_columns,
    generate_correlation_heatmap,
    generate_histogram,
    generate_boxplot,
)

st.title("Quick Dataset Analyzer")

# Get configurable max file size
max_size_mb = get_max_file_size_mb()

uploaded_file = st.file_uploader(f"Choose a CSV file (max {max_size_mb}MB)",
                                 type="csv")

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
            st.metric("Total Null Values", sum(stats["null_counts"].values()))

        # Numerical Statistics
        if stats["numerical_stats"]:
            st.subheader("Numerical Columns Statistics")
            num_stats_df = pd.DataFrame.from_dict(
                stats["numerical_stats"], orient="index"
            )
            num_stats_df = num_stats_df.round(2)
            st.dataframe(num_stats_df)

        # Categorical Statistics
        if stats["categorical_stats"]:
            st.subheader("Categorical Columns (Top 5 Values)")
            for col, value_counts in stats["categorical_stats"].items():
                with st.expander(f"📊 {col}"):
                    cat_df = pd.DataFrame(
                        list(value_counts.items()), columns=["Value", "Count"]
                    )
                    st.dataframe(cat_df)

        # Null Values Summary
        st.subheader("Null Values Summary")
        null_df = pd.DataFrame(
            list(stats["null_counts"].items()),
            columns=["Column", "Null Count"]
        )
        null_df = null_df[null_df["Null Count"] > 0]  # Only show columns with nulls
        if not null_df.empty:
            st.dataframe(null_df)
        else:
            st.info("No null values found in the dataset")

        # Data Types
        st.subheader("Column Data Types")
        dtype_df = pd.DataFrame(
            list(stats["data_types"].items()), columns=["Column", "Data Type"]
        )
        st.dataframe(dtype_df)

        # Data Visualizations
        st.header("📊 Data Visualizations")

        # Correlation Heatmap (always visible on main screen)
        st.subheader("Correlation Heatmap")
        heatmap_fig = generate_correlation_heatmap(df)
        if heatmap_fig:
            st.pyplot(heatmap_fig)
        else:
            numerical_cols = get_numerical_columns(df)
            if len(numerical_cols) == 1:
                st.info(
                    "Need at least 2 numerical columns to generate correlation heatmap. Only found: "
                    + ", ".join(numerical_cols)
                )
            else:
                st.info("No numerical columns found for correlation analysis.")

        # Column selector for detailed visualizations
        st.subheader("Detailed Column Visualizations")
        numerical_cols = get_numerical_columns(df)

        if numerical_cols:
            selected_column = st.selectbox(
                "Select a numerical column for detailed visualization:",
                numerical_cols,
                key="column_selector",
            )

            if st.button("Generate Visualizations", key="generate_viz"):
                st.session_state.selected_column = selected_column
                st.session_state.show_visualizations = True

            # Display visualizations if button was clicked
            if st.session_state.get(
                "show_visualizations", False
            ) and st.session_state.get("selected_column"):
                col = st.session_state.selected_column

                st.markdown("---")
                st.subheader(f"📈 Visualizations for: {col}")

                # Create two columns for histogram and boxplot
                viz_col1, viz_col2 = st.columns(2)

                with viz_col1:
                    st.markdown("**Distribution Histogram**")
                    hist_fig = generate_histogram(df, col)
                    if hist_fig:
                        st.pyplot(hist_fig)
                    else:
                        st.error(f"Could not generate histogram for {col}")

                with viz_col2:
                    st.markdown("**Boxplot**")
                    box_fig = generate_boxplot(df, col)
                    if box_fig:
                        st.pyplot(box_fig)
                    else:
                        st.error(f"Could not generate boxplot for {col}")

                # Add option to select different column
                if st.button("Select Different Column", key="change_column"):
                    st.session_state.show_visualizations = False
                    st.rerun()
        else:
            st.info("No numerical columns found for visualization.")

    except UnicodeDecodeError as e:
        st.error(f"Encoding error: Unable to decode the file. Error: {str(e)}")
    except pd.errors.ParserError as e:
        st.error(
            f"Parsing error: The file does not appear to be a valid CSV. Error: {str(e)}"
        )
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Please upload a CSV file to get started.")
