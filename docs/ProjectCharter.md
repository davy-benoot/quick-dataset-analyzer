# Project Charter (Prince2 Light Version)

## 1. Project Definition
**Project Name:**  
End-to-End Data Analytics Demonstration (CSV → Azure Deployment)

**Background:**  
The project aims to demonstrate the ability to deliver a professional, end-to-end data analytics solution. It will include data ingestion, analysis, testing, documentation, and deployment to Azure. The objective is to showcase professional delivery capabilities to potential collaborators or clients.  

**Objectives:**  
- Build a minimal but complete analytics pipeline from CSV upload to statistics dashboard.  
- Apply professional practices: testing, CI/CD, documentation, deployment.  
- Deliver a working demo accessible via Azure cloud.  
- Provide clear documentation so that others can build on it.  

**Scope (In):**  
- Upload CSV dataset.  
- Basic validation and preprocessing.  
- Compute summary statistics & simple visualizations.  
- Deploy to Azure App Service.  
- Documentation & unit tests.  

**Scope (Out):**  
- Advanced ML models.  
- Complex dashboards.  
- Multi-user management.  

---

## 2. Project Organization
**Project Board (roles):**  
- Executive: *You (project sponsor)*  
- Senior User: *Potential collaborators / demo users*  
- Senior Supplier: *You (developer/engineer)*  

**Project Manager:** You  
**Team Manager(s):** N/A (solo project, could be extended later)  

---

## 3. Business Case
**Why:**  
Demonstrating professional delivery of a small analytics project increases credibility and shows readiness to manage larger AI/analytics initiatives.  

**Expected Benefits:**  
- A visible live demo for portfolio.  
- Improved skills in CI/CD, testing, and deployment.  
- Reusable template for future projects.  

**Risks:**  
- Time constraints (weekend delivery).  
- Deployment issues with Azure configuration.  
- Over-engineering (scope creep).  

---

## 4. Project Approach
- Agile, time-boxed approach (weekend delivery).  
- Use **Python, Pandas, and Streamlit** for rapid prototyping of a user-facing interface.  
- Containerization with Docker.  
- Deployment on Azure App Service.  

**Note on Design Choice:**  
Streamlit was chosen instead of Flask/FastAPI because it enables rapid creation of a working analytics dashboard with minimal front-end overhead. This aligns with the project’s limited scope and timebox while still allowing professional practices (Dockerization, version control, testing). For production systems, a Flask/FastAPI approach could be considered.  

---

## 5. Project Controls
- Daily checkpoint reviews (self-reflection at end of day).  
- Timebox: 3 days (Friday evening to Sunday).  
- Deliverables checked against success criteria.  
- Version control via GitHub.  

---

## 6. Project Plan (High Level)
- **Day 1:** Planning, environment setup, repo, basic data handling.  
- **Day 2:** Data analysis functions, testing, Streamlit interface.  
- **Day 3:** Deployment, documentation, UAT, polish.  

---

## 7. Project Tolerances
- **Time:** +/- half a day.  
- **Scope:** Must deliver MVP; enhancements optional.  
- **Cost:** No external cost beyond Azure trial/credits.  

---

## 8. Initial Risks / Issues
- **Technical:** Deployment on Azure may require troubleshooting.  
- **Resource:** Solo project → no backup if blocked.  
- **Quality:** Limited time may constrain documentation depth.  
