"""
Optimized script to calculate and plot the distribution of company authorized capital
as a bar chart. Uses minimal memory and no `os` module.
"""

import csv
import matplotlib.pyplot as plt

AUTHORIZED_CAPITAL = 'AuthorizedCapital'


def load_and_categorize_capitals(companies_file):
    """
    Reads the CSV file line by line and categorizes each company's authorized capital.
    Returns a dictionary with counts per category.
    """
    categories = {
        "<= 1L": 0,
        "1L - 10L": 0,
        "10L - 1Cr": 0,
        "1Cr - 10Cr": 0,
        "> 10Cr": 0
    }

    with open(companies_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for company in reader:
            try:
                cap = float(company[AUTHORIZED_CAPITAL])
            except (ValueError, TypeError):
                continue 

            if cap <= 1_00_000:
                categories["<= 1L"] += 1
            elif cap <= 10_00_000:
                categories["1L - 10L"] += 1
            elif cap <= 1_00_00_000:
                categories["10L - 1Cr"] += 1
            elif cap <= 10_00_00_000:
                categories["1Cr - 10Cr"] += 1
            else:
                categories["> 10Cr"] += 1

    return categories


def plot_capital_distribution(categories):
    """Plot a bar chart showing number of companies per authorized capital range."""
    labels = list(categories.keys())
    counts = [categories[label] for label in labels]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, counts, color='#0561F7', edgecolor='black')
    plt.title('Histogram of Authorized Capital')
    plt.xlabel('Authorized Capital Range')
    plt.ylabel('Number of Companies')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('../plots/authorized_capital_histogram.png')
    plt.show()


def execute(companies_file):
    """Execute the data processing and plotting pipeline."""
    categories = load_and_categorize_capitals(companies_file)
    plot_capital_distribution(categories)


if __name__ == "__main__":
    COMPANIES_PATH = 'data/company_master.csv'
    execute(COMPANIES_PATH)
