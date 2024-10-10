from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
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

# Function to download and save the entire HTML content from the Tor-based site
def download_full_html_tor(url, output_file):
    # Path to the Tor Browser's Firefox binary
    tor_browser_path = r'C:\Tor Browser\Browser\firefox.exe'  # Replace with your actual path <>

    # Get Firefox options configured with the Tor proxy and Tor binary path
    firefox_options = setup_firefox_with_tor_proxy(tor_browser_path)

    # Start Selenium WebDriver with GeckoDriver for Firefox and the configured options
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    try:
        # Navigate to the .onion URL
        driver.get(url)

        # Wait for the page to fully load (adjust the sleep time as necessary)
        time.sleep(10)  # Adjust based on how long the page takes to load

        # Get the full page source after rendering
        page_source = driver.page_source

        # Save the HTML content to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"Successfully downloaded and saved the HTML content to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

# Example usage
if __name__ == '__main__':
    onion_url = 'http://stniiomyjliimcgkvdszvgen3eaaoz55hreqqx6o77yvmpwt7gklffqd.onion/'  # Replace with the actual .onion URL <>
    output_filename = 'scraped_page.html'  # File to save the HTML content

    # Download the full HTML content from the site
    download_full_html_tor(onion_url, output_filename)
