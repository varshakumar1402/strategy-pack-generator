import pdfplumber

def extract_pdf_data(file_obj):
    with pdfplumber.open(file_obj) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Fallbacks in case not found
    address = "Not found"
    council = "Not found"
    area = "Not found"
    constraints = "Not found"

    for line in text.splitlines():
        line = line.strip()
        if "Address:" in line:
            address = line.split("Address:")[-1].strip()
        elif "Council:" in line:
            council = line.split("Council:")[-1].strip()
        elif "Area:" in line or "Built Area:" in line:
            area = line.split(":")[-1].strip()
        elif "Constraints:" in line:
            constraints = line.split("Constraints:")[-1].strip()

    return {
        "property_address": address,
        "council_name": council,
        "total_area": area,
        "constraints": constraints
    }
