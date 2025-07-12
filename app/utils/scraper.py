import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_planning_portal(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    validated_date = None
    approved_date = None
    property_address = None
    documents = []

    # Simple heuristics
    for row in soup.find_all('tr'):
        text = row.get_text()
        if 'Valid' in text and 'Date' in text:
            validated_date = row.find_all('td')[-1].get_text(strip=True)
        if 'Approved' in text:
            approved_date = row.find_all('td')[-1].get_text(strip=True)
        if 'Address' in text:
            property_address = row.find_all('td')[-1].get_text(strip=True)

    # Parse dates and calculate timeline
    try:
        d1 = datetime.strptime(validated_date, "%d/%m/%Y")
        d2 = datetime.strptime(approved_date, "%d/%m/%Y")
        delta = (d2 - d1).days // 7
    except:
        delta = 0

    # Document links
    for link in soup.find_all('a', href=True):
        if '.pdf' in link['href'].lower():
            documents.append({
                'name': link.get_text(strip=True),
                'url': link['href']
            })

    return {
        "validated_date": validated_date or "N/A",
        "approved_date": approved_date or "N/A",
        "timeline_weeks": delta,
        "property_address": property_address or "N/A",
        "documents": documents
    }