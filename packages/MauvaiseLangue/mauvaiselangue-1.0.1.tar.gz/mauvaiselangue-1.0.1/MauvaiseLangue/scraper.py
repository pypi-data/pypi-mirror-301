import requests
from bs4 import BeautifulSoup

def scrape_insultes():
    """
    Scrapes French insults from the fixed Wiktionary category URL.

    Returns:
    - list of strings: A list containing the names of insults.
    """
    url = 'https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Insultes_en_fran%C3%A7ais'

    try:
        # Send a GET request to the page
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the specific section of insults on the page
            insultes_section = soup.find('div', {'id': 'mw-pages'})

            if insultes_section:
                # Find all <a> links in this section
                insultes_links = insultes_section.find_all('a', href=True, title=True)

                # Extract only the names of the insults
                insultes = [link.get('title') for link in insultes_links if "title" in link.attrs]
                return insultes
            else:
                print("Section des insultes non trouvée.")
                return []
        else:
            print(f"Request failed with status: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []
