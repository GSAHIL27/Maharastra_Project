"""
Optimized script to calculate and plot the total number of company registrations
per year as a bar chart. Uses minimal memory and no `os` module.
"""

import csv
import matplotlib.pyplot as plt

DATE_OF_REGISTRATION = 'CompanyRegistrationdate_date'
COMPANY_NAME = 'CompanyName'


def load_companies(company_master_file):
    """
    Reads the company CSV and returns a list of rows as dictionaries.
    Only necessary columns are processed.
    """
    companies = []
    with open(company_master_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append({
                DATE_OF_REGISTRATION: row[DATE_OF_REGISTRATION],
                COMPANY_NAME: row[COMPANY_NAME]
            })
    return companies


def calculate_registrations_per_year(companies):
    """Calculate the total number of unique company registrations per year."""
    registrations_per_year = {}
    seen_companies_per_year = {}

    for company in companies:
        year = int(company[DATE_OF_REGISTRATION].split('-')[0])
        name = company[COMPANY_NAME]

        if year not in registrations_per_year:
            registrations_per_year[year] = 0
            seen_companies_per_year[year] = set()

        if name not in seen_companies_per_year[year]:
            registrations_per_year[year] += 1
            seen_companies_per_year[year].add(name)

    return registrations_per_year


def plot_registrations_per_year(registrations):
    """Plot a bar chart showing total company registrations per year."""
    years = sorted(registrations.keys())
    counts = [registrations[y] for y in years]

    plt.figure(figsize=(14, 6))  
    plt.bar(years, counts, color='#0561F7', edgecolor='black')
    plt.title('Total Company Registrations Per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Companies')

    if len(years) > 20:
        step = max(1, len(years) // 10)  
    else:
        step = 1
    plt.xticks(years[::step], rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('../plots/company_registrations_per_year.png')
    plt.show()


def execute(companies_file):
    """Execute the data processing and plotting pipeline."""
    companies = load_companies(companies_file)
    registrations = calculate_registrations_per_year(companies)
    plot_registrations_per_year(registrations)


if __name__ == "__main__":
    COMPANIES_PATH = 'data/company_master.csv'
    execute(COMPANIES_PATH)
