import requests
from typing import List, TypedDict

class GeoLocation(TypedDict):
    country: str
    city: str
    isp: str
    coordinates: str


def get_geo_location(ip: str) -> GeoLocation | None:
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