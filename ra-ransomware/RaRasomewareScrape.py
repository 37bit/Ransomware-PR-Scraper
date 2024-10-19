import random
import time
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO)

def setup_firefox_with_tor_proxy(tor_binary_path):
    firefox_options = Options()
    firefox_options.binary_location = tor_binary_path
    # Utilise numerous other headers
    firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # setting up proxy 
    firefox_options.set_preference("network.proxy.type", 1)
    firefox_options.set_preference("network.proxy.socks", "127.0.0.1")
    firefox_options.set_preference("network.proxy.socks_port", 9150)
    firefox_options.set_preference("network.proxy.socks_remote_dns", True)
    firefox_options.add_argument("--headless")
    return firefox_options

def download_html_from_links(url, output_file, max_entries):
    # include own tor browser path
    tor_browser_path = r"C:\Users\bryan\Desktop\Tor Browser\Browser\firefox.exe" 
    firefox_options = setup_firefox_with_tor_proxy(tor_browser_path)

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    try:
        driver.get(url)

        # First 2 entries are not relevant for this duration
        for i in range(2,max_entries):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Try clicking a link
            for attempt in range(5):
                try:

                    # find buttons linked with a[href]
                    links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
                    if not links:
                        logging.warning("No available links found. Ending loop.")
                        break

                    # Click the link based on the current index of the loop, wrap around if i exceeds the number of links
                    link = links[i % len(links)]  
                    link.click()
                    logging.info(f"Clicked on link {i + 1}: {link.get_attribute('href')}")

                    # Exit if click is successful
                    break  

                except Exception as e:
                    logging.warning(f"Could not find or click any link. Error: {e}")
                    break

            # Scrape full page content after clicking the link
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                content_html = driver.page_source

                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n<!-- Entry {i + 1} -->\n\n")
                    f.write(content_html)

                logging.info(f"Entry {i + 1} content downloaded and saved.")
            except Exception as e:
                logging.warning(f"Could not scrape content on page {i + 1}. Error: {e}")
                logging.debug(traceback.format_exc())
                break

            # Go back to the main page
            try:
                home_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Home"))
                )
                home_link.click()
                logging.info("Navigated to the Home page.")
            except Exception as e:
                logging.warning(f"Could not find or click the Home link on page {i + 1}. Ending loop.")
                break
            
            # to reduce tax on server traffic
            time.sleep(random.uniform(2, 5))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.debug(traceback.format_exc())
    finally:
        driver.quit()

if __name__ == '__main__':
    onion_url = 'http://raworldw32b2qxevn3gp63pvibgixr4v75z62etlptg3u3pmajwra4ad.onion/index.html'
    output_filename = './output/scraped_pages4.html'
    max_entries_to_scrape = 25

    download_html_from_links(onion_url, output_filename, max_entries_to_scrape)