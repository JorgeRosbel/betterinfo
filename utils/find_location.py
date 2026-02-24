import requests
from typing import TypedDict

class GeoLocation(TypedDict):
    country: str
    city: str
    isp: str
    coordinates: str


def get_geo_location(ip: str) -> GeoLocation | None:
    """
    Retrieves geographical and ISP data for a given IP address using the ip-api service.

    Args:
        ip (str): The target IP address.

    Returns:
        dict | None: A dictionary containing country, city, isp, and coordinates, 
                     or None if the lookup fails.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as")
        data = response.json()
        
        if data['status'] == 'success':
            return {
                "country": data.get('country'),
                "city": data.get('city'),
                "isp": data.get('isp'),
                "coordinates": f"{data.get('lat')}, {data.get('lon')}"
            }
    except:
        pass
    return None