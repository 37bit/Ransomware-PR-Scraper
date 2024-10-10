from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time

# Function to set up the Firefox options with the Tor proxy (SOCKS5) and specify Tor Browser binary
def setup_firefox_with_tor_proxy(tor_binary_path):
    # Set up Firefox options
    firefox_options = Options()
    
    # Specify the Tor Browser binary location
    firefox_options.binary_location = tor_binary_path

    # Set the proxy to Tor (SOCKS5)
    firefox_options.set_preference("network.proxy.type", 1)  # Manual proxy configuration
    firefox_options.set_preference("network.proxy.socks", "127.0.0.1")  # Tor's SOCKS5 proxy address
    firefox_options.set_preference("network.proxy.socks_port", 9150)  # Tor's SOCKS5 proxy port
    firefox_options.set_preference("network.proxy.socks_remote_dns", True)  # Use Tor for DNS resolution
    
    # Optional: Run Firefox in headless mode (without GUI)
    firefox_options.add_argument("--headless")

    return firefox_options

# Function to download and save the HTML content for multiple pages
def download_html_multiple_pages(url, output_file, max_pages):
    # Path to the Tor Browser's Firefox binary
    tor_browser_path = r'C:\Tor Browser\Browser\firefox.exe'  # Replace with your actual path <>

    # Get Firefox options configured with the Tor proxy and Tor binary path
    firefox_options = setup_firefox_with_tor_proxy(tor_browser_path)

    # Start Selenium WebDriver with GeckoDriver for Firefox and the configured options
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    try:
        # Navigate to the .onion URL
        driver.get(url)

        # Loop through n pages
        for i in range(max_pages):
            # Wait for the page to fully load (adjust the sleep time as necessary)
            time.sleep(5)  # Adjust based on how long the page takes to load

            # Get the full page source after rendering
            page_source = driver.page_source

            # Save the HTML content to a file (appending the page source to the same file for simplicity)
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"\n\n<!-- Page {i+1} -->\n\n")  # Add a page separator for clarity
                f.write(page_source)
            
            print(f"Page {i+1} content downloaded and saved.")

            # Try to click the "Next" button (replace the selector if needed)
            try:
                next_button = driver.find_element(By.CLASS_NAME, 'next-page-btn')
                next_button.click()
                print(f"Navigated to page {i+2}")
            except Exception as e:
                print(f"Could not find or click the next button on page {i+1}. Ending loop.")
                break  # If there is no next button or we encounter an error, stop the loop

            # Wait for the next page to load
            time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

# Example usage
if __name__ == '__main__':
    onion_url = 'http://stniiomyjliimcgkvdszvgen3eaaoz55hreqqx6o77yvmpwt7gklffqd.onion/'  # Replace with the actual .onion URL <>
<<<<<<< HEAD
    output_filename = 'scraped_page.html'  # File to save the HTML content
=======
    output_filename = './output/scraped_pages.html'  # File to save the HTML content for all pages
    max_pages_to_scrape = 13  # Number of pages you want to scrape
>>>>>>> 26f7b59b2432b8761c9490aa96b8c8ba209e24b3

    # Download the HTML content from multiple pages
    download_html_multiple_pages(onion_url, output_filename, max_pages_to_scrape)
