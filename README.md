# Quick Dataset Analyzer

A minimal, end-to-end data analytics project demonstrating CSV upload, data analysis, and deployment to Azure. Built with Python, Pandas, and Streamlit, it follows professional practices: testing, version control, documentation, and containerization.

---

## 🚀 Project Goal
- Upload a CSV dataset with automatic encoding detection.
- Perform validation (file size, format, encoding).
- Compute comprehensive summary statistics:
  - **Numerical columns**: mean, median, standard deviation
  - **Categorical columns**: top 5 most frequent values
  - **All columns**: null value counts and data types
- **Generate interactive data visualizations**:
  - Correlation heatmaps for variable relationships
  - Histograms and boxplots for distribution analysis
  - Per-column detailed visualizations
- Provide a user-friendly Streamlit interface for data exploration and visualization.
- Deploy to Azure cloud for easy sharing and demonstration.

---

## 📂 Project Structure

quick-dataset-analyzer/
│
├── README.md # Project overview and documentation
├── requirements.txt # Python dependencies
├── LICENSE # MIT License
├── .gitignore # Git ignore rules
├── src/ # Source code
│ ├── app.py # Streamlit web application
│ └── data_pipeline.py # Data loading, validation, and statistics
├── tests/ # Unit tests
│ └── test_pipeline.py # Comprehensive test suite
├── docs/ # Documentation
│ └── ProjectCharter.md # PRINCE2 project charter
└── data/ # Sample data directory (gitignored)

---

## ✨ Features

- **CSV Upload**: Support for CSV files with automatic encoding detection
- **Configurable File Size**: Environment-based file size limits (default 5MB)
- **Data Validation**: Format validation, encoding detection, and error handling
- **Summary Statistics**:
  - Numerical columns: mean, median, standard deviation
  - Categorical columns: top 5 value frequencies
  - All columns: null counts and data type information
- **Data Visualizations**:
  - **Correlation Heatmap**: Shows relationships between all numerical variables
  - **Interactive Histograms**: Distribution plots for individual numerical columns
  - **Boxplots**: Statistical summary plots with quartiles and outlier detection
  - **Per-Column Analysis**: Select specific columns for detailed visualization
- **Interactive UI**: Clean Streamlit interface with expandable sections and dynamic visualizations
- **Comprehensive Testing**: Unit tests covering all functionality
- **Cloud Ready**: Optimized for containerized deployment with configurable limits

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/davy-benoot/quick-dataset-analyzer.git
   cd quick-dataset-analyzer
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Configure file size limit:
   ```bash
   export MAX_FILE_SIZE_MB=10  # Set to 10MB instead of default 5MB
   ```

5. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## ☁️ Deployment

The app is containerized with Docker.

Can be deployed to Azure App Service or any container-supported cloud service.

## 📄 Documentation

/docs/ProjectCharter.md — Prince2-style project charter

/docs/Architecture.md — System design overview

/docs/Usage.md — Instructions for users

## 💡 Notes

Streamlit was chosen for rapid prototyping of a user-facing analytics dashboard.

For production-grade applications, Flask or FastAPI could be implemented.

This project demonstrates end-to-end delivery including CI/CD readiness, testing, and documentation.

## 📝 License

MIT License
