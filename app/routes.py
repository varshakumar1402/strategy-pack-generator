from flask import Blueprint, render_template, request, redirect, send_file
from .utils.pdf_parser import extract_pdf_data
from .utils.scraper import scrape_planning_portal
from .utils.streetview import get_streetview_image
from .utils.flowchart import generate_flowchart
from .utils.pptx_generator import create_pptx
import tempfile
import os

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        files = request.files
        landinsight_pdf = files.get('landinsight_pdf')

        # Extract from LandInsight
        li_data = extract_pdf_data(landinsight_pdf)

        # Scrape portal links
        portal1 = scrape_planning_portal(form_data['portal_link_1'])
        portal2 = scrape_planning_portal(form_data['portal_link_2'])

        # Streetview images
        portal1['streetview'] = get_streetview_image(portal1['property_address'])
        portal2['streetview'] = get_streetview_image(portal2['property_address'])

        # Generate flowchart
        flowchart_path = generate_flowchart(form_data['planning_type'])

        # Compile all data
        full_data = {
            **form_data,
            **li_data,
            "portal_1": portal1,
            "portal_2": portal2,
            "flowchart": flowchart_path
        }

        pptx_path = create_pptx(full_data)

        return send_file(pptx_path, as_attachment=True)

    return render_template('form.html')