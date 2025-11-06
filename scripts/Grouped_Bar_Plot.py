"""
Optimized script to calculate and plot a grouped bar plot of company registrations
by Principal Business Activity for the last 10 years. Uses minimal memory.
"""

import csv
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import random  # Added for color generation

DATE_OF_REGISTRATION = 'CompanyRegistrationdate_date'
PRINCIPAL_ACTIVITY = 'CompanyIndustrialClassification'


def load_activity_counts(companies_file):
    """Read CSV and count registrations per (year, activity)."""
    counts = defaultdict(int)
    max_year = 0

    with open(companies_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for company in reader:
            try:
                year = int(company[DATE_OF_REGISTRATION].split('-')[0])
                activity = company[PRINCIPAL_ACTIVITY].strip()
            except (ValueError, KeyError):
                continue

            counts[(year, activity)] += 1
            max_year = max(max_year, year)

    return counts, max_year


def aggregate_top_activities(counts, max_year, top_n=5, last_years=10):
    """Aggregate counts for top N activities in the last M years."""
    start_year = max_year - last_years + 1
    activity_totals = Counter()

    for (year, activity), count in counts.items():
        if start_year <= year <= max_year:
            activity_totals[activity] += count

    top_activities = [act for act, _ in activity_totals.most_common(top_n)]
    years = list(range(start_year, max_year + 1))
    data_matrix = [[counts.get((year, activity), 0) for year in years]
                   for activity in top_activities]

    return years, top_activities, data_matrix


def plot_grouped_bar(years, activities, data_matrix):
    """Plot a grouped bar chart for top activities over the last 10 years."""
    num_activities = len(activities)
    width = 0.15
    x_positions = list(range(len(years)))

    
    colors = [(random.random(), random.random(), random.random()) for _ in range(num_activities)]

    plt.figure(figsize=(14, 7))

    for i, activity_data in enumerate(data_matrix):
        shifted_positions = [x + i * width for x in x_positions]
        plt.bar(shifted_positions, activity_data, width=width, color=colors[i], label=activities[i])

    middle_positions = [x + width * (num_activities - 1) / 2 for x in x_positions]
    plt.xticks(middle_positions, years, rotation=45)
    plt.xlabel('Year')
    plt.ylabel('Number of Companies')
    plt.title('Company Registrations by Principal Business Activity\n(Last 10 Years)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('../plots/Top_5_Principal_Business_Activity.png')
    plt.show()


def execute(companies_file):
    """Execute the data processing and plotting pipeline."""
    counts, max_year = load_activity_counts(companies_file)
    years, activities, data_matrix = aggregate_top_activities(counts, max_year)
    plot_grouped_bar(years, activities, data_matrix)


if __name__ == "__main__":
    COMPANIES_PATH = '../data/company_master.csv'
    execute(COMPANIES_PATH)
