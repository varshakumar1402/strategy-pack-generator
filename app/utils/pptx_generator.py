from pptx import Presentation
from pptx.util import Inches
import os

def replace_text_placeholders(slide, data):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    for key, value in data.items():
                        placeholder = f"{{{{{key}}}}}"
                        if placeholder in run.text:
                            run.text = run.text.replace(placeholder, str(value))

def insert_image(slide, placeholder, image_path, width=Inches(4)):
    if not os.path.exists(image_path):
        return
    for shape in slide.shapes:
        if shape.has_text_frame and placeholder in shape.text:
            left, top = shape.left, shape.top
            slide.shapes._spTree.remove(shape._element)
            slide.shapes.add_picture(image_path, left, top, width=width)
            break

def create_pptx(data, template_path="template.pptx"):
    prs = Presentation(template_path)

    for slide in prs.slides:
        replace_text_placeholders(slide, data)

        # Insert known image placeholders
        insert_image(slide, "{{flowchart image}}", data.get("flowchart", ""))
        insert_image(slide, "{{streetview_image}}", data.get("streetview", ""))
        insert_image(slide, "{{property - sample 1 - screenshot}}", data.get("sample1_streetview", ""))
        insert_image(slide, "{{property - sample 2 - screenshot}}", data.get("sample2_streetview", ""))

    output_path = "/tmp/generated_strategy_pack.pptx"
    prs.save(output_path)
    return output_path
