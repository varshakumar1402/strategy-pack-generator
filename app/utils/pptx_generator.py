from pptx import Presentation
from pptx.util import Inches

def create_pptx(data):
    prs = Presentation("template.pptx")

    # Example: replace text placeholder
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        run.text = run.text.replace("{{client name}}", data.get("client_name", ""))
                        run.text = run.text.replace("{{property address}}", data.get("property_address", ""))
                        run.text = run.text.replace("{{scope of work}}", data.get("scope_of_work", ""))

    # Save to file
    output_path = "/tmp/generated_strategy_pack.pptx"
    prs.save(output_path)
    return output_path