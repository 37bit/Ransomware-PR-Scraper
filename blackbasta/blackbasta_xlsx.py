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
    cards = soup.find_all('div', class_='vuepress-markdown-body')

    # Loop through each card and extract the relevant information
    for card in cards:
            
            # Extract the site name (from the <a> tag inside <div class="title">)
            site_name_tag = card.find('p', {'data-v-md-line': '5'})
            if site_name_tag is None or 'SITE' not in site_name_tag.get_text():
                site_name_tag = card.find('p', {'data-v-md-line': '6'})
            if site_name_tag is None:
                 site_name_tag = card.find('p', {'data-v-md-line': '10'})
            print(site_name_tag)
            site_url = site_name_tag.get_text(strip=True) if site_name_tag else 'N/A'
                

            # Extract the description (inside <p> tags with data-v-md-line attributes)
            description_tag = card.find('p', {'data-v-md-line': '3'})
            description = description_tag.get_text(strip=True) if description_tag else 'N/A'

            # Extract the address (inside the <p> tag with data-v-md-line="7")
            address_tag = card.find('p', {'data-v-md-line': '7'})
            address = address_tag.get_text(strip=True) if address_tag else 'N/A'

            # Extract the data size and all related data types as a single cell value
            data_size_block = card.find('p', {'data-v-md-line': '12'})
            data_size_combined = ' '.join(data_size_block.stripped_strings) if data_size_block else 'N/A'

            # Append the extracted information to the data list
            data.append([site_url, description, address, data_size_combined])

        # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data, columns=['Site URL', 'Description', 'Address', 'Data Size & Types'])

        # Save the DataFrame to an Excel file
    df.to_excel(output_excel_file, index=False)

    print(f"Data successfully saved to {output_excel_file}")

# Example usage
if __name__ == '__main__':
    html_file = './output/scraped_pages.html'  # Path to the input HTML file
    output_excel_file = './output/organized_data.xlsx'  # Path to the output Excel file

    # Convert the HTML content into an Excel file
    html_to_excel(html_file, output_excel_file)
 