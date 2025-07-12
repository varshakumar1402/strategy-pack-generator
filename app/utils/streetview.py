import requests
import hashlib
import os

def get_streetview_image(address, api_key=None):
    if not api_key:
        # default key (yours)
        api_key = "AIzaSyBjyFV86_hOyWIrvRQGeGrBjVn5jlsF4r8"

    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "640x400",
        "location": address,
        "key": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception("Street View API failed")

    # Create unique filename using hash of address
    hashed = hashlib.md5(address.encode()).hexdigest()
    filename = f"/tmp/streetview_{hashed}.jpg"

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename
