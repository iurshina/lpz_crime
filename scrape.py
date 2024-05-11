import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from db import save_to_db

def fetch_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = "https://www.polizei.sachsen.de/de/"  # Base URL for relative links
    links = []

    divs = soup.find_all('div', style="width: 306px;")
    for div in divs:
        link = div.find('a', href=True)
        full_url = urljoin(base_url, link['href'])
        links.append(full_url)
    
    return links

def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    sections = soup.find_all('h3')
    for section in sections:
        # Initial variable to hold the location and time
        ort = zeit = None
        content = []

        # Find the first <p> right after the <h3>
        first_p = section.find_next_sibling('p')
        if first_p:
            ort_zeit_text = first_p.get_text(strip=True)
            if 'Ort:' in ort_zeit_text and 'Zeit:' in ort_zeit_text:
                ort = ort_zeit_text.split('Zeit:')[0].replace('Ort:', '').strip()
                zeit = ort_zeit_text.split('Zeit:')[1].strip()
        
        # Continue only if both Ort and Zeit have been found
        if ort and zeit:
            next_node = first_p.find_next_sibling()
            while next_node and next_node.name != 'h3':
                if next_node.name == 'p':
                    content.append(next_node.get_text(strip=True))
                next_node = next_node.find_next_sibling()

            # Now save to the database
            print(f"{ort} {zeit} {section.get_text(strip=True)} {' '.join(content)}")
            save_to_db(ort, zeit, section.get_text(strip=True), ' '.join(content))