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
def download_html_multiple_pages(url, output_file):
    # Path to the Tor Browser's Firefox binary
    tor_browser_path = r'/Applications/Tor Browser.app/Contents/MacOS/firefox'  # Replace with your actual path

    # Get Firefox options configured with the Tor proxy and Tor binary path
    firefox_options = setup_firefox_with_tor_proxy(tor_browser_path)

    # Start Selenium WebDriver with GeckoDriver for Firefox and the configured options
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    try:
        # Navigate to the initial URL (main page)
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Get HTML of the main page
        main_page_html = driver.page_source

        # Save the main page HTML first (using 'w' to write initially)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"<!-- Main Page HTML -->\n{main_page_html}\n\n<!-- Linked Pages HTML -->\n")

        # Find all the boxes (divs with class 'col-12 col-md-6 col-lg-4')
        boxes = driver.find_elements(By.CSS_SELECTOR, "div.col-12.col-md-6.col-lg-4")

        # Iterate through each box to find the 'a' tag and click the link
        for index, box in enumerate(boxes):
            try:
                link = box.find_element(By.TAG_NAME, "a")
                link_url = link.get_attribute("href")

                # Scroll the link into view using JavaScript
                driver.execute_script("arguments[0].scrollIntoView(true);", link)
                time.sleep(1)  # Give it some time after scrolling

                # Click the link using JavaScript instead of Selenium's click
                driver.execute_script("arguments[0].click();", link)
                time.sleep(5)  # Wait for the linked page to load

                # Get the HTML of the linked page
                linked_page_html = driver.page_source
                linked_page_html_comment = f"<!-- Linked Page HTML ({index + 1}): {link_url} -->\n{linked_page_html}\n\n"

                # Append linked page HTML to the file
                with open(output_file, 'a', encoding='utf-8') as file:
                    file.write(linked_page_html_comment)

                # Go back to the main page to continue processing other links
                driver.back()
                time.sleep(5)  # Wait for the main page to load again

            except Exception as e:
                print(f"Error processing link {index + 1}: {e}")
                continue

        print(f"HTML of main and linked pages saved to '{output_file}'")

    finally:
        # Quit the browser when done
        driver.quit()

# Example usage
if __name__ == '__main__':
    onion_url = 'http://ransomxifxwc5eteopdobynonjctkxxvap77yqifu2emfbecgbqdw6qd.onion/'  # Replace with the actual .onion URL
    output_filename = './output/scraped_pages.html'  # File to save the HTML content for all pages

    # Download the HTML content from multiple pages
    download_html_multiple_pages(onion_url, output_filename)
