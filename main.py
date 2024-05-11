from scrape import fetch_links, scrape_content
from db import create_db, fetch_leipzig_reports

import os
import re
from collections import Counter

def get_population():
    area_population = {}
    with open("data/people_2023.txt") as f:
        for line in f:
            match = re.match(r"(.+?)\s+(\w+)\s+(\d+)$", line.strip())
            if match:
                area = match.group(1).strip()
                population = int(match.group(3))
                area_population[area] = population
    return area_population

def extract_area_from_ort(ort):
    match = re.search(r'\((.*?)\)', ort)
    if match:
        return match.group(1) 
    return None

def analyze_reports(reports):
    return Counter(extract_area_from_ort(report[1]) for report in reports if extract_area_from_ort(report[1]))

if __name__ == "__main__":
    db_path = 'polizei_reports_2023.db'
    if not os.path.exists(db_path):
        print(f"Database does not exist. Creating {db_path}...")
        file_path = "links_2023.txt"
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file.readlines()]

        create_db(db_path)
        for url in urls:
            links = fetch_links(url)
            for link in links:
                scrape_content(link)
    
    res = fetch_leipzig_reports(db_path)
    ort_counts = analyze_reports(res)
    ort_population = get_population()

    freq_per_capita = {}
    print("Frequency of each 'Ort' in Leipzig reports:")
    for ort, count in ort_counts.items():
        if ort in ort_population:
            print(f"{ort}: {count / ort_population[ort]} times per capita")
            print(f"{ort}: {count} times")
            freq_per_capita[ort] = count / ort_population[ort]

    print("Sorted frequency of each 'Ort' in Leipzig reports:")
    sorted_areas = sorted(freq_per_capita.items(), key=lambda item: item[1], reverse=True)
    for area, frequency in sorted_areas:
        print(f"{area}: {frequency * 1000:.8f} crimes per 1000")
