from bs4 import BeautifulSoup
import pandas as pd

# Function to extract data from the provided HTML file and save it to an Excel file
def html_to_excel(html_file, output_excel_file):
    # Read the HTML content from the file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a list to store the extracted data
    data = []
    # Extract relevant data
    # Find all <div> tags and extract the text content for each section
    cards = soup.find_all('div', class_='col-md-12 col-sm-12 col-black-bg portfolio-item')

    # Loop through each card and extract the relevant information
    for card in cards:
            
            # Extract the site url (from the <a> tag beside the <div class="Official Website">)
            url_tag = card.find('h5', text=lambda x: x and 'Official Website:' in x)
            url_tag = url_tag.find_next_sibling('div')
            site_url = url_tag.get_text(strip=True) if url_tag else 'N/A'

            # Extract the site date (from the <a> tag beside the <div class="Schedule for Document Public Release">)
            date_tag = card.find('h5', text=lambda x: x and 'Schedule for Document Public Release:' in x)
            date_tag = date_tag.find_next_sibling('div')
            site_date = date_tag.get_text(strip=True) if date_tag else 'N/A'

            # Extract the site size (from the <a> tag beside the <div class="SIZE">)
            size_tag = card.find('h5', text=lambda x: x and 'SIZE:' in x)
            size_tag = size_tag.find_next_sibling('div')
            site_size = size_tag.get_text(strip=True)  if size_tag else 'N/A'

            # Extract the site content (from the <a> tag beside the <div class="Content">)
            content_tag = card.find('h5', text=lambda x: x and 'Content:' in x)
            content_tag = content_tag.find_next_sibling('div')
            site_content = content_tag.get_text(strip=True)  if content_tag else 'N/A'

            # Create a Variable to store data not found
            nlm = 'N/A'

            # Append the extracted information to the data list with the agreed variables
            data.append([site_url, site_date, nlm, nlm, nlm, nlm, site_content, site_size, nlm, nlm, nlm, nlm, nlm, nlm, nlm, nlm ])

        # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data, columns=['Site URL', 'Date of Attack', 'Description', 'Address', 'Country', 'Industry', 'Content', 'Size', 'Personal identifiable Information(PII)', 'Financial Data', 'Intellectual Property', 'Customer Data', 'Employee Data', 'Legal and Compliance Data', 'Operational and Business Continuity Data', 'Health Data(PHI)'])

        # Save the DataFrame to an Excel file
    df.to_excel(output_excel_file, index=False)

    print(f"Data successfully saved to {output_excel_file}")

# Example usage
if __name__ == '__main__':
    html_file = './output/scraped_pages4.html'  # Path to the input HTML file
    output_excel_file = './output/organized_data.xlsx'  # Path to the output Excel file

    # Convert the HTML content into an Excel file
    html_to_excel(html_file, output_excel_file)