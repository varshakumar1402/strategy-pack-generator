import pdfplumber

def extract_pdf_data(file_obj):
    with pdfplumber.open(file_obj) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    lines = full_text.splitlines()
    address, council, area, constraints = "Not found", "Not found", "Not found", "Not found"

    for line in lines:
        l = line.lower()
        if "address" in l and address == "Not found":
            address = line.strip()
        elif "council" in l and council == "Not found":
            council = line.strip()
        elif ("area" in l or "sqm" in l) and area == "Not found":
            area = line.strip()
        elif "constraint" in l and constraints == "Not found":
            constraints = line.strip()

    return {
        "property_address": address,
        "council_name": council,
        "total_area": area,
        "constraints": constraints
    }
