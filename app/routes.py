from flask import Blueprint, render_template, request, send_file
from .utils.pdf_parser import extract_pdf_data
from .utils.scraper import scrape_planning_portal
from .utils.streetview import get_streetview_image
from .utils.flowchart import generate_flowchart
from .utils.pptx_generator import create_pptx
import json

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("🚀 POST / triggered")

        form = request.form
        files = request.files

        try:
            # Collect form data
            client_name = form.get("client_name")
            scope = form.get("scope_of_work")
            existing_use = form.get("existing_use")
            planning_type = form.get("planning_type")
            portal_link_1 = form.get("portal_link_1")
            portal_link_2 = form.get("portal_link_2")
            building_reg = "Yes" if form.get("building_reg_required") else "No"

            # Extract LandInsight PDF data
            land_pdf = files.get("landinsight_pdf")
            li_data = extract_pdf_data(land_pdf)
            print("✅ PDF parsed:", li_data)

            # Scrape planning portals
            portal_1 = scrape_planning_portal(portal_link_1)
            portal_2 = scrape_planning_portal(portal_link_2)
            print("✅ Portal 1:", portal_1.get("property_address"))
            print("✅ Portal 2:", portal_2.get("property_address"))

            # Get street view images
            gsv_main = get_streetview_image(li_data.get("property_address", ""))
            gsv1 = get_streetview_image(portal_1.get("property_address", ""))
            gsv2 = get_streetview_image(portal_2.get("property_address", ""))

            # Generate flowchart image
            flowchart_path = generate_flowchart(planning_type)

            # Ensure documents list is not None
            portal_1["documents"] = portal_1.get("documents", [])
            portal_2["documents"] = portal_2.get("documents", [])

            # Prepare data for preview page
            ppt_data = {
                "client name": client_name,
                "scope of work": scope,
                "existing use": existing_use,
                "planning_type": planning_type,
                "building reg required": building_reg,
                "property address": li_data.get("property_address"),
                "local council name": li_data.get("council_name"),
                "total area": li_data.get("total_area"),
                "constraints": li_data.get("constraints"),
                "Link 1": portal_link_1,
                "Link 2": portal_link_2,
                "timeline 1": portal_1.get("timeline_weeks", ""),
                "timeline 2": portal_2.get("timeline_weeks", ""),
                "property address - sample 1": portal_1.get("property_address", ""),
                "property address - sample 2": portal_2.get("property_address", ""),
                "flowchart": flowchart_path,
                "streetview": gsv_main,
                "sample1_streetview": gsv1,
                "sample2_streetview": gsv2,
                "portal_1": portal_1,
                "portal_2": portal_2
            }

            print("🔍 Preview data ready. Rendering preview.html")
            return render_template("preview.html", data=ppt_data)

        except Exception as e:
            print("❌ Error in / POST route:", str(e))
            return "An error occurred while processing your submission. Please try again.", 500

    return render_template("form.html")


@main.route('/generate', methods=['POST'])
def generate():
    print("⚙️  /generate triggered")
    try:
        data = json.loads(request.form['serialized'])

        # Add user-selected floor plans and elevations
        data["Sim app Floor plan 1"] = request.form.get("floorplan1")
        data["Sim app Floor plan 2"] = request.form.get("floorplan2")
        data["Sim app elevation 1"] = request.form.get("elevation1")
        data["Sim app elevation 2"] = request.form.get("elevation2")

        print("🧩 Data received for PPTX generation")
        pptx_path = create_pptx(data)
        return send_file(pptx_path, as_attachment=True)

    except Exception as e:
        print("❌ Error in /generate:", str(e))
        return "Failed to generate PowerPoint. Please try again.", 500
