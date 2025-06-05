# 🔍 Naukri Job Scraper & Real-Time Insights Dashboard

This project uses **Selenium** to scrape real-time **Data Analyst job listings** from [Naukri.com](https://naukri.com) and visualizes them using an interactive **Streamlit Dashboard**. It enables users to explore the latest job trends, download job data, and gain quick insights into job market demands.

---

## 📦 Features

- ✅ Real-time scraping of job listings from Naukri.com  
- ✅ Saves data with timestamped `.csv` files  
- ✅ Clean Streamlit dashboard for filtering, visualizing & downloading jobs  
- ✅ Charts and summaries: Most common skills, locations, companies, etc.  
- ✅ One-click export to Excel  

---## 🛠️ Technologies Used

- 🐍 Python
- 🌐 Selenium (web scraping)
- 📊 Pandas (data handling)
- 📈 Streamlit (dashboard)
- 🧠 Matplotlib / Plotly / Altair (charts)
- 📁 CSV (data storage)

---

## 🚀 How to Run
### 🔧 1. Clone this repo
```bash
git clone https://github.com/somranal2799/naukri-job-scraper-dashboard.git
cd naukri-job-scraper-dashboard
🐍 2. Set up environment
Install dependencies:

pip install -r requirements.txt
🧹 3. Scrape jobs (optional, already included)

python scraper.py
🖥️ 4. Launch the dashboard

streamlit run dashboard.py
📂 Project Structure
📦 naukri-job-scraper-dashboard/
├── scraper.py             # Scrapes job data from Naukri
├── app.py           # Streamlit dashboard app
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── data/                  # CSV job data files

📈 Sample Insights
📌 Top hiring companies

📍 Common job locations

🛠️ Most in-demand skills

📅 Recently posted jobs

📥 Output Example
CSV file: naukri_jobs_2025-06-05_22-34-15.csv
Includes columns:
Title, Company, Location, Experience, Description, Skills, Posted, Job URL

✨ Future Ideas
Add ML to cluster jobs by seniority

Resume matching for job fit

Email alerts for fresh jobs

Thanks for reading , Feel free to comment.