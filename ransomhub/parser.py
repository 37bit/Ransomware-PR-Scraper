import pandas as pd
from bs4 import BeautifulSoup
from bs4 import Comment  # Import Comment to handle HTML comments

# Function to check if a line is likely part of the company description
def is_company_description(line):
    # Exclude lines with keywords related to data size or stolen information
    exclude_keywords = ['GB', 'MB', 'data', 'confidential', 'information', 'records', 'documents', 'names', 'phone', 'financial']
    return not any(keyword.lower() in line.lower() for keyword in exclude_keywords)

# Function to check if a line contains stolen data information
def is_stolen_data(line):
    # Include lines with keywords related to data size or stolen information
    include_keywords = ['GB', 'MB', 'confidential', 'data', 'records', 'documents', 'names', 'phone', 'financial', 'employee']
    return any(keyword.lower() in line.lower() for keyword in include_keywords)

# Function to parse and extract data
def parse_html_to_data(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    data = []

    # Parse the main page to get site URL and date of attack
    main_page_boxes = soup.find_all('div', class_='col-12 col-md-6 col-lg-4')
    
    for box in main_page_boxes:
        # Extract the company URL (site URL) from the <strong> tag
        company_url = box.find('strong').text if box.find('strong') else 'N/A'
        
        # Extract the date of attack from the footer, adding better error handling
        date_of_attack = 'N/A'  # Default value
        footer = box.find('div', class_='card-footer')
        if footer:
            date_of_attack = footer.text.strip() if footer.text.strip() else 'N/A'
        
        # Extract the link to the company's detailed page
        link_url = box.find('a')['href'] if box.find('a') else 'N/A'
        
        # Go to the linked page's HTML (next block in combined HTML)
        linked_page_comment = soup.find(string=lambda text: isinstance(text, Comment) and link_url in text)
        linked_page_html = linked_page_comment.find_next() if linked_page_comment else None
        linked_soup = BeautifulSoup(str(linked_page_html), 'html.parser') if linked_page_html else None

        # Extract and clean company description and stolen data
        description_lines = []
        stolen_data_lines = []
        if linked_soup:
            content_div = linked_soup.find('div', class_='post-content')
            if content_div:
                all_content = content_div.get_text(separator='\n').strip().split('\n')
                
                # Iterate through each line and classify as description or stolen data
                for line in all_content:
                    if is_company_description(line):
                        description_lines.append(line.strip())
                    elif is_stolen_data(line):
                        stolen_data_lines.append(line.strip())

        # Handle missing descriptions
        description = ' '.join(description_lines) if description_lines else 'N/A'
        stolen_data = '\n'.join(stolen_data_lines) if stolen_data_lines else 'N/A'
        
        # Add the extracted information to the data list
        data.append({
            'Company URL': company_url,
            'Date of Attack': date_of_attack,
            'Description': description,
            'Stolen Data Info': stolen_data
        })

    return data

# Function to convert the parsed data into an Excel file
def export_to_excel(data, excel_file):
    df = pd.DataFrame(data)
    df.to_excel(excel_file, index=False)
    print(f"Data successfully saved to {excel_file}")

# Main function to parse the HTML and export to Excel
def main():
    html_file = './output/scraped_pages.html'  # The HTML file you previously saved
    excel_file = 'organized_data.xlsx'  # The Excel file where the output will be saved

    # Parse the HTML and extract data from both main and linked pages
    data = parse_html_to_data(html_file)

    # Export the data to Excel
    export_to_excel(data, excel_file)

if __name__ == '__main__':
    main()
