from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl import Workbook
import time

# CONSTANTS
ORG_NAME = "ORGANIZATION NAME"
CTY = "COUNTRY"
ORG_URL = "ORGANIZATION WEBSITE URL"
VIEWS = "NUMBER OF VIEWS"
ADDED = "ADDED DATE"
PUB = "PUBLICATION DATE"
AMT_DATA = "AMOUNT OF DATA"
INFO_DATA = "INFORMATION"
CAT = "INDUSTRY"
COMMENT_DATA = "COMMENT"
DOWNLOAD_LINKS = "DOWNLOAD LINKS"
DOWNLOAD_PASS = "DOWNLOAD PASSWORD"

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



card_no = 0
def get_card_details(cards):
    global card_no
    card_details = []

    # Express each card as a dictionary of attributes
    for c in cards:
        card_no += 1
        c_text = c.text.splitlines()
        # Add the attributes visible on main page
        dict = {
            ORG_NAME: c_text[0],
            CTY: c_text[1],
            ORG_URL: c_text[2],
            VIEWS: c_text[3],
            ADDED: c_text[4],
            PUB: c_text[5],
        }

        # Get topic (new page). Doing this because c.click() doesn't seem to work
        topic_id = c.get_attribute("onclick").split("'")[1]
        topic_url = onion_url + "topic.php?id=" + topic_id
        driver.get(topic_url)

        # Get divs on page
        t_rows = driver.find_elements(By.TAG_NAME, "tr")
        divs = t_rows[0].find_elements(By.TAG_NAME, "div")

        # Extract amt, info and comment data
        amt_data = divs[4].text.splitlines()[0]
        info_data = divs[7].text.splitlines()[0]
        cat = determine_industry(dict[ORG_NAME], info_data)
        comment_data = divs[8].text.splitlines()[0]
        download_links = ""

        # Get download links if exists
        try:
            download_links = divs[9].text
        except Exception:
            pass
            # print('No download links available for card {}.'.format(card_no))

        dict[AMT_DATA] = amt_data
        dict[INFO_DATA] = info_data
        dict[CAT] = cat
        dict[COMMENT_DATA] = comment_data
        dict[DOWNLOAD_LINKS] = download_links
        

        # Add dict object to list
        print("Obtained card {} info.".format(card_no))
        card_details.append(dict)

        # # Parse download links
        # download_links = normalize(download_links).splitlines()
        # for link in download_links:
        #     search_download_files(link)

        # Go back to main page
        driver.back()

    return card_details

# def search_download_files(download_link):
#     print('Searching {} for files...'.format(download_link))
#     driver.get(download_link)

def normalize(data):
    return data.split(":")[-1]

def determine_industry(company_name, company_info):
    company_info = normalize(company_info)
    # print('Determining industry for {}...'.format(company_name))
    
    
    # info_set = company_info.strip().replace("!", "").replace(",", "").replace(".", "").replace(":", "").replace("?", "").split(" ")
    # info_set = set(map(lambda word : word.lower(), info_set))

    # for cat in INDUSTRIES:
    #     keyword_set = set(INDUSTRIES[cat])
    #     if len(info_set.intersection(keyword_set)) > 0:
    #         return cat
    
    # return ""

    company_info = company_info.lower()
    for cat in INDUSTRIES:
        for keyword in INDUSTRIES[cat]:
            if keyword in company_info:
                return cat
    return ""



def output_dicts_to_excel(dicts):
    # Create the workbook
    workbook = Workbook()

    # Add the header
    sheet = workbook.active
    sheet.append(
        [ORG_NAME, CTY, ORG_URL, VIEWS, ADDED, PUB, AMT_DATA, INFO_DATA, CAT, DOWNLOAD_LINKS] # COMMENT_DATA taken out
    )

    # Add the card details
    item_no = 0
    for d in dicts:
        views_normalized = normalize(d[VIEWS])
        added_normalized = normalize(d[ADDED])
        pub_normalized = normalize(d[PUB])
        amt_normalized = normalize(d[AMT_DATA])
        info_normalized = normalize(d[INFO_DATA])
        comment_normalized = normalize(d[COMMENT_DATA])
        download_normalized = normalize(d[DOWNLOAD_LINKS])
        download_normalized = "Yes" if len(download_normalized) > 0 else "No"
        sheet.append(
            [
                d[ORG_NAME],
                d[CTY],
                d[ORG_URL],
                views_normalized,
                added_normalized,
                pub_normalized,
                amt_normalized,
                info_normalized,
                d[CAT],
                #comment_normalized,
                download_normalized
            ]
        )
        item_no += 1
        print("Item {} written to excel.".format(item_no))

    workbook.save(filename=EXCEL_FILENAME)
    print("All data successfully written to excel!")


# Setup and load main page
output_file = "page_source.html"
onion_url = "http://mbrlkbtq5jonaqkurjwmxftytyn2ethqvbxfu4rgjbkkknndqwae6byd.onion/"
tor_browser_path = r"C:\Tor Browser\Browser\firefox.exe"
driver = setup_firefox_with_tor_proxy(tor_browser_path)
driver.get(onion_url)


# Get max pages
max_pages = 30 #int(driver.find_elements(By.CLASS_NAME, 'Page')[-1].text)
print('There are a total of {} pages.'.format(max_pages))

card_details = []
# Pagination 
try:
    for i in range(12, max_pages):
        # Formulate new page url
        page_url = onion_url + "index.php?page=" + str(i+1)
        driver.get(page_url)
        print('Now scraping page {} ({}).'.format(i+1, driver.current_url))

        # Get the cards for first page
        cards = driver.find_elements(By.CLASS_NAME, "News")
        card_details += get_card_details(cards)
except Exception:
    print('An exception has occurred. Outputting to excel and aborting...')
    output_dicts_to_excel(card_details)
    driver.quit()
    exit(1)

# Output to excel
output_dicts_to_excel(card_details)

driver.quit()