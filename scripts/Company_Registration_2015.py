"""
 Company Registrations Analysis (2015)

This module:
- Reads company registration and ZIP-to-district mapping data
- Counts registrations by district for the year 2015
- Generates and saves a bar chart of top districts

Author: Your Name
"""

import csv
import re
from collections import Counter
import matplotlib.pyplot as plt


COMPANIES_FILE = 'data/company_master.csv'
ZIPCODE_FILE = 'data/zipcode.csv'
OUTPUT_PLOT_PATH = 'plots/registrations_2015_by_district.png'


REGISTRATION_DATE_FIELD = "CompanyRegistrationdate_date"
ADDRESS_FIELD = "Registered_Office_Address"

TARGET_YEAR = "2015"
TOP_DISTRICTS = 15


def calculate_registrations(company_file, zipcode_file, year=TARGET_YEAR):
    """
    Count company registrations by district for a specific year.
    Uses a ZIP-to-district mapping and processes rows in a memory-efficient way.
    """
    zip_to_district = {}

    
    with open(zipcode_file, encoding="utf-8") as zipcode_reader:
        for mapping in csv.DictReader(zipcode_reader):
            zipcode = mapping.get("ZipCode", "").replace(" ", "")
            district = mapping.get("District", "").strip()
            if zipcode and district:
                zip_to_district[zipcode] = district

    district_counter = Counter()

 
    with open(company_file, encoding="utf-8") as company_reader:
        for record in csv.DictReader(company_reader):
            registration_date = record.get(REGISTRATION_DATE_FIELD, "")
            address = record.get(ADDRESS_FIELD, "")

            
            if not registration_date.startswith(year):
                continue

            
            zip_matches = re.findall(r"\b\d{6,7}\b", address)
            for raw_zip in zip_matches:
                clean_zip = raw_zip.replace(" ", "")
                if clean_zip in zip_to_district:
                    district = zip_to_district[clean_zip]
                    district_counter[district] += 1
                    break  

    return district_counter


def plot_top_districts(district_data, top_n=TOP_DISTRICTS):
    """
    Plot and save a horizontal bar chart of top districts by registration count.
    """
    if not district_data:
        print(" No valid registrations found for the given year.")
        return

    top_items = district_data.most_common(top_n)
    districts, counts = zip(*top_items)

    plt.figure(figsize=(10, 6))
    bars = plt.barh(districts[::-1], counts[::-1],
                    color="#0561F7", edgecolor="black")
    plt.xlabel("Number of Registrations")
    plt.ylabel("District")
    plt.title(f"Top {top_n} Districts by Company Registrations ({TARGET_YEAR})")

    for bar in bars:
        count = int(bar.get_width())
        plt.text(count + 0.3, bar.get_y() + bar.get_height() / 2,
                 str(count), va="center")

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT_PATH)
    plt.show()


def execute():
    """Main function to orchestrate calculation and plotting."""
    district_counts = calculate_registrations(COMPANIES_FILE, ZIPCODE_FILE)
    print(" District Registration Counts:\n", district_counts)
    plot_top_districts(district_counts, TOP_DISTRICTS)


if __name__ == "__main__":
    execute()
