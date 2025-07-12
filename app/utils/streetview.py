import requests

def get_streetview_image(address):
    api_key = "AIzaSyBjyFV86_hOyWIrvRQGeGrBjVn5jlsF4r8"
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        'size': '600x400',
        'location': address,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    filename = f"/tmp/{address.replace(' ', '_')}_gsv.jpg"
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename