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
- Provide a user-friendly Streamlit interface for data exploration.
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
- **Data Validation**: File size limits (5MB), format validation, and error handling
- **Summary Statistics**:
  - Numerical columns: mean, median, standard deviation
  - Categorical columns: top 5 value frequencies
  - All columns: null counts and data type information
- **Interactive UI**: Clean Streamlit interface with expandable sections
- **Comprehensive Testing**: Unit tests covering all functionality
- **Production Ready**: Containerized with Docker for easy deployment

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

4. Run the application:
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
