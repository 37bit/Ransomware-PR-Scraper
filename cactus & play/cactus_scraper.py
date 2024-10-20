from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import Workbook
from datetime import datetime
import time
import re

# CONSTANTS
DATE = "DATE"
TITLE = "TITLE"
INDUSTRY = "INDUSTRY"
CPN_DESC = "COMPANY DESCRIPTION"
WEBSITE = "WEBSITE"
REVENUE = "REVENUE"
ADDRESS = "ADDRESS"
PHONE = "PHONE NUMBER"
DATA = "DATA DESCRIPTION"

# REGEX PATTERNS
DATE_PTN = r"(\d\d\.\d\d\.\d\d\d\d)"
WEBSITE_PTN = r"Website: ([\w:\/\.]+)\n"
REVENUE_PTN = r"Revenue : \$([\d\.]+M?)\n"
ADDRESS_PTN = r"Address: ([\w ,]+)\n"
PHONE_PTN = r"Phone Number: ([\+\d\(\)\- ]+)\n"
DATA_DESC_PTN = r"DATA DESCRIPTIONS: ([\w,\\\.\n ]+)"
CPN_TXT_PTN = r"([a-zA-Z&-\. ]+)\n{2}\“(.*)\”" # Group 1 - Industry; Group 2 - Company description

EXCEL_FILENAME = "data.xlsx"
INDUSTRIES = {
    "Healthcare": [
        "medical", "hospital", "healthcare", "clinical", "pharmaceutical", "biotech", 
        "patient care", "wellness", "diagnostic", "nursing", "health services", 
        "telemedicine", "surgeon", "laboratory", "medical devices", "mental health", 
        "therapy", "biomedical", "genetics", "epidemiology", "public health"
    ],
    "Financial Services": [
        "banking", "investment", "fintech", "loans", "financial planning", "mortgages", 
        "wealth management", "insurance", "brokerage", "asset management", 
        "credit", "capital markets", "trading", "hedge fund", "private equity", 
        "investment banking", "retirement", "mutual funds", "venture capital", 
        "financial advisory"
    ],
    "Government": [
        "public sector", "municipal", "federal", "state", "regulatory", "policy", 
        "government services", "defense", "civil service", "public administration", 
        "law enforcement", "national security", "public health", "bureaucracy", 
        "taxation", "elections", "foreign affairs", "diplomacy", "public policy", 
        "governance"
    ],
    "Energy and Utilities": [
        "energy", "power", "electricity", "natural gas", "renewable", "utility", 
        "grid", "nuclear", "wind", "solar", "water management", "hydroelectric", 
        "bioenergy", "energy storage", "sustainability", "fossil fuels", "geothermal", 
        "smart grid", "energy efficiency", "offshore wind"
    ],
    "Manufacturing": [
        "production", "factory", "assembly", "machinery", "manufacture", 
        "industrial", "automation", "supply chain", "materials", "engineering", 
        "lean manufacturing", "CNC", "quality control", "industrial design", 
        "fabrication", "machining", "additive manufacturing", "3D printing", 
        "robotics", "process optimization"
    ],
    "Education": [
        "school", "university", "learning", "training", "academic", "curriculum", 
        "K-12", "higher education", "e-learning", "teaching", "scholarship", 
        "distance learning", "MOOCs", "vocational training", "educational technology", 
        "pedagogy", "tutoring", "student services", "early childhood", "STEM"
    ],
    "Retail": [
        "retail", "e-commerce", "shopping", "store", "consumer goods", "merchandising", 
        "supply chain", "fashion", "point of sale", "wholesale", "online marketplace", 
        "inventory", "discount", "omnichannel", "brick and mortar", "luxury goods", 
        "retail analytics", "customer experience", "loyalty programs", "retail management"
    ],
    "Legal": [
        "law", "legal services", "litigation", "court", "attorney", "compliance", 
        "legal counsel", "contract", "intellectual property", "dispute resolution", 
        "corporate law", "criminal law", "arbitration", "legal technology", 
        "regulatory affairs", "tax law", "employment law", "family law", 
        "mergers and acquisitions", "privacy law"
    ],
    "Transportation": [
        "logistics", "transportation", "shipping", "freight", "delivery", "transit", 
        "fleet management", "airlines", "rail", "trucking", "supply chain", 
        "cargo", "urban mobility", "public transportation", "maritime", 
        "aviation", "logistics technology", "distribution", "last mile", 
        "autonomous vehicles"
    ],
    "Hospitality": [
        "hotel", "restaurant", "tourism", "travel", "guest services", "accommodation", 
        "leisure", "catering", "hospitality management", "event planning", 
        "resorts", "cruise lines", "lodging", "airbnb", "hospitality technology", 
        "food services", "spa", "concierge", "tourism management", "event coordination"
    ],
    "Telecommunications": [
        "telecom", "internet", "wireless", "fiber optic", "broadband", "communication", 
        "networking", "mobile", "telephony", "data transmission", "5G", 
        "satellite", "VoIP", "ISP", "telecom infrastructure", "telecom services", 
        "network security", "broadband services", "telecommunications hardware", 
        "digital communication"
    ],
    "Media": [
        "broadcast", "news", "entertainment", "digital media", "publishing", "content", 
        "advertising", "journalism", "social media", "film", "television", "radio", 
        "streaming", "content creation", "influencer marketing", "video production", 
        "media technology", "advertising technology", "media analytics", "podcasting"
    ],
    "Insurance": [
        "insurance", "claims", "underwriting", "policyholder", "premium", "risk management", 
        "brokerage", "actuary", "coverage", "health insurance", "auto insurance", 
        "life insurance", "reinsurance", "disability insurance", "liability", 
        "commercial insurance", "risk assessment", "claims management", 
        "insurance technology", "policy issuance"
    ],
    "Real Estate": [
        "property", "real estate", "land", "development", "residential", "commercial", 
        "housing", "leasing", "brokerage", "realty", "mortgage", "property management", 
        "real estate investment", "REIT", "appraisal", "zoning", "urban development", 
        "home buyers", "real estate technology", "property sales"
    ],
    "IT and SaaS": [
        "software", "SaaS", "cloud", "information technology", "tech", "application", 
        "IT services", "cybersecurity", "software development", "digital transformation", 
        "API", "PaaS", "IaaS", "enterprise software", "data management", 
        "cloud computing", "artificial intelligence", "machine learning", "DevOps", 
        "infrastructure as code"
    ],
    "Construction": [
        "construction", "building", "infrastructure", "civil engineering", "contracting", 
        "architecture", "project management", "real estate development", "renovation", 
        "construction materials", "green building", "construction technology", 
        "commercial construction", "residential construction", "urban development", 
        "construction equipment", "contractors", "blueprints", "building code", 
        "construction safety"
    ],
    "Tourism": [
        "tourism", "travel", "hospitality", "leisure", "adventure", "vacation", 
        "tour guide", "cruise", "ecotourism", "travel agency", "destination management", 
        "sustainable tourism", "heritage tourism", "tour operators", "travel services", 
        "cultural tourism", "aviation", "car rental", "travel packages", "excursions"
    ],
    "Automotive": [
        "automotive", "vehicles", "cars", "trucks", "automobile", "manufacturing", 
        "repair", "electric vehicle", "dealership", "transportation", "parts", 
        "auto parts", "EV", "autonomous vehicles", "auto financing", "automotive engineering", 
        "car leasing", "auto industry", "auto insurance", "aftermarket"
    ],
    "Consultation": [
        "consulting", "advisory", "strategy", "management", "business services", 
        "professional services", "expertise", "client solutions", "consultant", 
        "management consulting", "business advisory", "strategy consulting", 
        "financial consulting", "technology consulting", "market research", 
        "change management", "human resources consulting", "operations consulting", 
        "organizational development", "business transformation"
    ],
    "Business Supplies & Equipment": [
        "supplies", "business services", "equipment", "inventory", "industrial tools", 
        "office supplies", "B2B", "logistics", "warehouse", "packaging", 
        "machinery", "industrial equipment", "commercial equipment", "office furniture", 
        "cleaning supplies", "facility management", "B2B services", "industrial safety", 
        "maintenance supplies", "tools and hardware"
    ],
    "Oil & Gas": [
        "oil", "gas", "petroleum", "drilling", "exploration", "refining", 
        "pipeline", "energy", "offshore", "upstream", "downstream", "hydrocarbon", 
        "LNG", "oilfield services", "petrochemicals", "oil exploration", "natural gas", 
        "crude oil", "fracking", "oil and gas production"
    ],
    "Agriculture": [
        "agriculture", "farming", "crop", "livestock", "agro", "agri-tech", 
        "harvest", "soil", "sustainable farming", "irrigation", "agronomy", 
        "organic farming", "precision farming", "agriculture technology", "fertilizer", 
        "seeds", "farming equipment", "crop management", "rural development", "farming techniques"
    ],
    "Consumer Goods & Services": [
        "consumer goods", "products", "services", "retail", "FMCG", "brand", 
        "customer", "marketplace", "supply chain", "e-commerce", "consumer electronics", 
        "luxury goods", "household products", "personal care", "retail services", 
        "customer experience", "consumer products", "product design", "packaging", 
        "brand management"
    ],
    "Engineering": [
        "engineering", "design", "development", "mechanical", "civil", "electrical", 
        "industrial", "innovation", "R&D", "systems", "automation", "product development", 
        "engineering services", "prototyping", "sustainability", "engineering solutions", 
        "construction engineering", "technical consulting", "industrial design", "manufacturing engineering"
    ],
    "Architecture": [
        "architecture", "design", "urban planning", "construction", "blueprint", 
        "landscape", "interior design", "building", "renovation", "infrastructure", 
        "architectural services", "sustainable design", "residential design", 
        "commercial architecture", "historic preservation", "urban development", 
        "green architecture", "drafting", "architectural engineering", "building materials"
    ],
    "Distribution": [
        "distribution", "logistics", "supply chain", "warehouse", "transportation", 
        "fulfillment", "inventory", "wholesale", "shipping", "e-commerce", 
        "distribution network", "third-party logistics", "freight forwarding", 
        "order fulfillment", "supply chain management", "last-mile delivery", 
        "retail distribution", "inventory management", "logistics technology", "distribution services"
    ],
    "Food & Beverages": [
        "food", "beverages", "restaurant", "catering", "hospitality", "grocery", 
        "retail", "consumer goods", "FMCG", "organic", "sustainable farming", 
        "restaurant management", "food production", "culinary", "packaged foods", 
        "dairy", "meat", "alcoholic beverages", "non-alcoholic beverages", "food services"
    ]
}
DATA_TYPES = {
    "Personal Identifiable Information (PII)": [
        "personal", "name", "address", "phone number", "email", "date of birth", "social security number", "passport number", 
        "driver's license", "national ID", "biometric data"
    ],
    "Financial Data": [
        "money", "financial", "accounting", "bank account", "credit card", "debit card", "transaction history", "tax information", 
        "investment records", "financial statements", "loans", "balance", "account number"
    ],
    "Intellectual Property": [
        "intellectual", "project", "patent", "corporate data", "trademark", "copyright", "trade secret", "design", "invention", "source code", 
        "proprietary algorithms", "research and development", "technical documentation"
    ],
    "Customer Data": [
        "customer", "customer data", "customer ID", "purchase history", "support tickets", "preferences", "order details", "contact information", 
        "feedback", "account activity", "billing details"
    ],
    "Employee Data": [
        "employee ID", "salary", "performance reviews", "employment history", "benefits", 
        "payroll", "attendance records", "personal contact information", "emergency contact", "training records"
    ],
    "Legal and Compliance Data": [
        "contracts", "agreements", "regulatory filings", "licenses", "audit reports", 
        "litigation documents", "corporate policies", "compliance records", "certifications"
    ],
    "Operational and Business Continuity Data": [
        "business strategy", "disaster recovery plans", "supply chain data", "vendor information", 
        "inventory", "incident response plans", "process documentation", "risk management", "maintenance schedules"
    ],
    "Health Data (PHI)": [
        "medical records", "health insurance information", "diagnoses", "treatment plans", 
        "lab results", "prescriptions", "doctor's notes", "medical history", "genetic data", "clinical trials"
    ]
}

# Function to set up the Firefox options with the Tor proxy (SOCKS5) and specify Tor Browser binary
def setup_firefox_with_tor_proxy(
    tor_binary_path,
):  # Path to Tor browser. Not the Geckodriver!
    # Set up Firefox options
    firefox_options = Options()

    # Specify the Tor Browser binary location
    firefox_options.binary_location = tor_binary_path

    # Set the proxy to Tor (SOCKS5)
    firefox_options.set_preference(
        "network.proxy.type", 1
    )  # Manual proxy configuration
    firefox_options.set_preference(
        "network.proxy.socks", "127.0.0.1"
    )  # Tor's SOCKS5 proxy address
    firefox_options.set_preference(
        "network.proxy.socks_port", 9150
    )  # Tor's SOCKS5 proxy port
    firefox_options.set_preference(
        "network.proxy.socks_remote_dns", True
    )  # Use Tor for DNS resolution

    # Optional: Run Firefox in headless mode (without GUI)
    firefox_options.add_argument("--headless")

    # Start Selenium WebDriver with GeckoDriver for Firefox and the configured options
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()), options=firefox_options
    )

    return driver

def map_to_industry(industry, cpn_desc):
    industry = industry.lower()
    cpn_desc = cpn_desc.lower()

    for ind in INDUSTRIES:
        keywords = INDUSTRIES[ind]
        for k in keywords:
            if k in industry or k in cpn_desc:
                return ind
    
    return ''

def map_to_data_type(data_desc):
    dt_dict = {}
    dt_desc = data_desc.lower().replace('\\', ' ').replace(',', ' ')

    # Map each list item to the appropriate data type
    for dt_key in DATA_TYPES:
        keywords = DATA_TYPES[dt_key]
        for k in keywords:
            if k in data_desc:
                dt_dict[dt_key] = 1
                break
        else: # If no keywords match
            dt_dict[dt_key] = 0

    return dt_dict

def parse_desc(desc):
    # try:
    # print(desc.text)

    # Get industry and company description
    cpn_text = re.search(CPN_TXT_PTN, desc)
    industry = "" if not cpn_text else cpn_text.group(1).strip('. ')
    cpn_desc = "" if not cpn_text or len(cpn_text.groups()) != 2 else cpn_text.group(2).strip()

    industry = map_to_industry(industry, cpn_desc) if industry != "" else ""
    # print('Industry: {}'.format(industry))
    # print('Company description: {}'.format(cpn_desc))

    date = re.search(DATE_PTN, desc)
    date = datetime.today().strftime(r'%d-%m-%Y') if not date else date.group(1).strip().replace('.', '-')

    website = re.search(WEBSITE_PTN, desc)
    website = "" if not website else website.group(1).strip()

    revenue = re.search(REVENUE_PTN, desc)
    revenue = "" if not revenue else revenue.group(1).strip()

    address = re.search(ADDRESS_PTN, desc)
    address = "" if not address else address.group(1).strip()

    phone = re.search(PHONE_PTN, desc)
    phone = "" if not phone else phone.group(1).strip()

    data_desc = re.search(DATA_DESC_PTN, desc)
    data_desc = "" if not data_desc else data_desc.group(1).strip()

    data_desc_dict = map_to_data_type(data_desc)
    return_dict = {
        DATE: date,
        INDUSTRY: industry,
        CPN_DESC: cpn_desc,
        WEBSITE: website,
        REVENUE: revenue,
        ADDRESS: address,
        PHONE: phone,
        DATA: data_desc
        # DATA: data_desc
    }
    return_dict.update(data_desc_dict)
    return return_dict

# except Exception:
#     print('A problem has occurred with retrieving description details')




card_num = 0
def get_card_details(driver, card):
    card_dict = {}
    global card_num
    card_num += 1
    # try:

    # Click link inside the card
    current_url = driver.current_url
    link = card.find_element(By.TAG_NAME, "a")
    link.click()

    # Wait until page changes
    WebDriverWait(driver, 10).until(EC.url_changes(current_url))

    # # Get date
    # date = driver.find_element(By.TAG_NAME, "span")
    # card_dict[DATE] = date.text

    # Get title
    title = driver.find_element(By.TAG_NAME, "h1")
    card_dict[TITLE] = title.text

    # Parse description to get more details
    desc = driver.find_elements(By.TAG_NAME, "p")
    desc_text = '\n'.join(list(map(lambda d : d.text, desc)))
    desc_parsed = parse_desc(desc_text)
    card_dict.update(desc_parsed)

    current_url = driver.current_url
    driver.back()
    WebDriverWait(driver, 10).until(EC.url_changes(current_url))
    return card_dict

    # except Exception:
    #     print('Error with obtaining card {}'.format(card_num))
    #     driver.quit()
    #     exit(1)


def output_dicts_to_excel(dicts):
    # Create the workbook
    workbook = Workbook()

    # Add the header
    sheet = workbook.active
    sheet.append(
        list(dicts[0].keys())
        # [DATE, TITLE, INDUSTRY, CPN_DESC, WEBSITE, REVENUE, PHONE, ADDRESS, DATA]
    )

    # Add the card details
    item_no = 0
    for d in dicts:
        sheet.append(list(d.values()))# [d[DATE], d[TITLE], d[INDUSTRY], d[CPN_DESC], d[WEBSITE], d[REVENUE], d[PHONE], d[ADDRESS], d[DATA]])
        item_no += 1
        print("Item {} written to excel.".format(item_no))

    workbook.save(filename=EXCEL_FILENAME)
    print("All data successfully written to excel!")


# Setup and load main page
onion_url = "https://cactusbloguuodvqjmnzlwetjlpj6aggc6iocwhuupb47laukux7ckid.onion/"
tor_browser_path = r"C:\Tor Browser\Browser\firefox.exe"
driver = setup_firefox_with_tor_proxy(tor_browser_path)
driver.get(onion_url)

# Pagination
time.sleep(3)
num_pages = int(driver.find_elements(By.TAG_NAME, "a")[-1].text)
print('There are {} pages in total.'.format(num_pages))
num_cards = len(driver.find_elements(By.TAG_NAME, "article"))

try:
    card_dicts = []
    for page in range(num_pages):
        WebDriverWait(driver, 5).until(lambda d : len(d.find_elements(By.TAG_NAME, "article")) == num_cards)
        num_cards = len(driver.find_elements(By.TAG_NAME, "article"))

        print('Now scraping page {}.'.format(page + 1))
        print('There are {} cards on page {}.'.format(num_cards, page + 1))
        
        # Iterate through cards
        for card_no in range(num_cards):

            # Wait for all cards to finish loading
            WebDriverWait(driver, 10).until(lambda d : len(d.find_elements(By.TAG_NAME, "article")) == num_cards)
            cards = driver.find_elements(By.TAG_NAME, "article")

            # Get current card in iteration
            card = cards[card_no]
            card_dict = get_card_details(driver, card)
            card_dicts.append(card_dict)

        # Go to next page
        next_page_url = onion_url + "/?page=" + str(page+1)
        driver.get(next_page_url)

except Exception:
    print('An exception has occured.')
    print('Writing to excel and exiting immediately...')
    output_dicts_to_excel(card_dicts)
    driver.quit()
    exit(1)
    

# Proceed to write to excel file
print("Finished obtaining all card details")
print("Writing to excel file...")

output_dicts_to_excel(card_dicts)
driver.quit()
