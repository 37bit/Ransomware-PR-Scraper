import whois
import pandas as pd

# Function to get country from domain using whois
def get_country_from_domain(domain):
    try:
        # Perform whois lookup
        w = whois.whois(domain)
        if w and 'country' in w:
            return w['country']
        else:
            return 'Country not found'
    except Exception as e:
        return f"Error: {str(e)}"

# Load company domains from a CSV file (replace with your file)
domains_file = 'company_domains.csv'
df = pd.read_csv(domains_file)

# Assuming the CSV file has a column 'Domain' with the company domains
df['Country'] = df['Domain'].apply(get_country_from_domain)

# Save the results to a new Excel file
output_file = 'company_domains_with_countries.xlsx'
df.to_excel(output_file, index=False)

print(f"Results saved to {output_file}")
