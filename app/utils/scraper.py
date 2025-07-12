import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_planning_portal(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch URL: {url}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract property address
    try:
        address_section = soup.find('span', {'id': 'ctl00_MainContent_lblSiteAddress'})
        address = address_section.text.strip() if address_section else "Not found"
    except:
        address = "Not found"

    # Extract validated and approved dates
    validated_date = None
    approved_date = None

    for row in soup.select('table tr'):
        cells = row.find_all('td')
        if len(cells) == 2:
            label = cells[0].text.strip()
            value = cells[1].text.strip()

            if "Validated" in label:
                validated_date = value
            if "Decision Issued" in label or "Decision Date" in label:
                approved_date = value

    # Parse timeline
    timeline_weeks = 0
    try:
        if validated_date and approved_date:
            d1 = datetime.strptime(validated_date, "%d/%m/%Y")
            d2 = datetime.strptime(approved_date, "%d/%m/%Y")
            timeline_weeks = (d2 - d1).days // 7
    except:
        pass

    # Extract document links
    documents = []
    for link in soup.find_all("a", href=True):
        if ".pdf" in link["href"]:
            documents.append({
                "name": link.text.strip(),
                "url": link["href"]
            })

    return {
        "property_address": address,
        "validated_date": validated_date,
        "approved_date": approved_date,
        "timeline_weeks": timeline_weeks,
        "documents": documents
    }
