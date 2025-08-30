# Quick Dataset Analyzer

A minimal, end-to-end data analytics project demonstrating CSV upload, data analysis, and deployment to Azure. Built with Python, Pandas, and Streamlit, it follows professional practices: testing, version control, documentation, and containerization.

---

## 🚀 Project Goal
- Upload a CSV dataset.
- Perform basic validation and preprocessing.
- Compute summary statistics and simple visualizations.
- Provide a user-friendly interface for interactive exploration.
- Deploy to Azure cloud for easy sharing and demonstration.

---

## 📂 Project Structure

quick-dataset-analyzer/
│
├── README.md # Project overview
├── requirements.txt # Python dependencies
├── Dockerfile # Containerization for Azure
├── src/ # Source code
│ ├── app.py # Streamlit main app
│ ├── data_pipeline.py # CSV loading & preprocessing
│ ├── analysis.py # Statistics & visualizations
│ └── utils.py # Helper functions
├── tests/ # Unit and integration tests
├── docs/ # Documentation (Project Charter, Architecture, Usage)
└── data/ # Sample CSV files (gitignored)

---

## ⚙️ Installation

1. Clone the repo:
git clone https://github.com/davy-benoot/quick-dataset-analyzer.git

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