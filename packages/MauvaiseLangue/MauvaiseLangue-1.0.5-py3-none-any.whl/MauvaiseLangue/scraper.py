import requests
from bs4 import BeautifulSoup
import os
import json

CACHE_FILE = 'insultes_cache.json'

def load_cached_insultes():
    """
    Loads cached insults from a local JSON file, if it exists.
    
    Returns:
    - list of str: A list of cached insults, or an empty list if the cache is missing or invalid.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            try:
                cached_data = json.load(f)
                return cached_data
            except json.JSONDecodeError:
                return []
    return []

def save_insultes_to_cache(insultes):
    """
    Saves the insults to a local JSON file.
    
    Args:
    - insultes (list of str): The list of insults to be cached.
    """
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(insultes, f, ensure_ascii=False, indent=4)

def scrape_insultes():
    """
    Scrapes French insults from the fixed Wiktionary category URL or loads from cache if the site is unavailable.

    Returns:
    - list of str: A list containing insult titles, excluding specific category titles.
    """
    base_url = 'https://fr.wiktionary.org'
    url = '/wiki/Cat%C3%A9gorie:Insultes_en_fran%C3%A7ais'
    all_insultes = []

    try:
        while url:
            # Send a GET request to the page
            response = requests.get(base_url + url, timeout=10)  # Add a timeout for better reliability

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the specific section of insults on the page
                insultes_section = soup.find('div', {'id': 'mw-pages'})  # e.g., a div containing insults

                if insultes_section:
                    # Find all <a> links in this section
                    insultes_links = insultes_section.find_all('a', href=True, title=True)

                    # Extract insult titles, excluding specific category titles
                    insultes = [
                        link.get('title') for link in insultes_links 
                        if "title" in link.attrs and link.get('title') != 'Catégorie:Insultes en français'
                    ]
                    all_insultes.extend(insultes)

                # Check if there is a "page suivante" link and update the url
                next_page_link = insultes_section.find('a', string='page suivante')
                if next_page_link:
                    url = next_page_link['href']
                else:
                    url = None
            else:
                print(f"Request failed with status: {response.status_code}")
                break
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

    # Save the scraped insults to cache
    save_insultes_to_cache(all_insultes)

    return all_insultes if all_insultes else load_cached_insultes()  # Load from cache if no insults found

