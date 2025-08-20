## Ransomware PR Analysis

This project automates the scraping and analysis of press release (PR) pages maintained by ransomware gangs, accessible only on the Dark Web.
Selenium & BeautifulSoup are primarily used for the scraping process.
The project also includes a formal report and dataset of aggregated and cleaned raw data from the various PR pages.


### 📂 Project Structure
---

```
├── blackbasta/          # Scraping & raw data for BlackBasta ransomware gang
├── cactus & play/       # Scraping & raw data for Cactus and Play ransomware gangs
├── ra-ransomware/       # Scraping & raw data for RA ransomware gang
├── ransomhub/           # Scraping & raw data for RansomHub
├── Cleaned data.csv     # Consolidated & cleaned dataset from all sources
├── Charts.twb           # Tableau workbook for data visualization
├── Report.docx          # Written report with findings
├── requirements.txt     # Python dependencies
└── .gitignore
```


### 🚀 Features

---

- Automated scraping of ransomware PR sites using Selenium & BeautifulSoup
- Cleaning and normalization of scraped data into a CSV dataset
- Exploratory analysis and visualization via Tableau (Charts.twb)
- Full written report (Report.docx) summarizing findings


### 🔧 Installation

---

1. Clone this repository:

```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```
(or simply download the repository as a zip above)

2. Create a virtual environment (optional but recommended):

```
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```


### ⚠️ Disclaimer

---

This project is for educational and research purposes only. It does not promote or support malicious activity. The scraped data originates from publicly accessible ransomware PR sites.
