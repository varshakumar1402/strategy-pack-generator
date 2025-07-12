import fitz  # PyMuPDF

def extract_pdf_data(file):
    doc = fitz.open(stream=file.read(), filetype='pdf')
    text = ''
    for page in doc:
        text += page.get_text()

    # Basic extraction logic
    address = ""
    council = ""
    area = ""
    constraints = ""

    for line in text.split('\n'):
        if 'Address:' in line:
            address = line.split('Address:')[-1].strip()
        if 'Council:' in line:
            council = line.split('Council:')[-1].strip()
        if 'Area:' in line:
            area = line.split('Area:')[-1].strip()
        if 'Constraints:' in line:
            constraints = line.split('Constraints:')[-1].strip()

    return {
        "property_address": address or "Not found",
        "council_name": council or "Not found",
        "total_area": area or "Not found",
        "constraints": constraints or "Not found"
    }