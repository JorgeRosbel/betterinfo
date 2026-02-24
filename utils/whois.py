import requests
from typing import TypedDict, List
from datetime import datetime

class DomainInfo(TypedDict):
    nameservers: List[str]
    registrar: str
    creation_date: str
    expiration_date: str
    status: str
    domain_name: str
    remaining_time_in_days: int | str

class ErrorInfo(TypedDict):
    error: str


def whois(domain: str) -> DomainInfo | ErrorInfo:
    """
    Retrieves domain registration data using the RDAP protocol.

    Args:
        domain (str): The domain name to query (e.g., 'example.com').

    Returns:
        dict: A dictionary containing domain details like nameservers, registrar, 
              creation/expiration dates, and remaining days, or an error message.
    """
    
    url = f"https://rdap.verisign.com/com/v1/domain/{domain}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            raw_creation = data.get("events", [{}])[0].get("eventDate", "N/A")
            raw_expiration = data.get("events", [{}])[1].get("eventDate", "N/A")
            
            remaining_days = "N/A"
            creation_human = "N/A"
            expiration_human = "N/A"
            
            if raw_expiration != "N/A":
                dt_exp = datetime.strptime(raw_expiration[:10], "%Y-%m-%d")
                remaining_days = (dt_exp - datetime.now()).days
                expiration_human = dt_exp.strftime("%d/%m/%y")
                
            if raw_creation != "N/A":
                dt_crea = datetime.strptime(raw_creation[:10], "%Y-%m-%d")
                creation_human = dt_crea.strftime("%d/%m/%y")

            return {
                "domain_name": data.get("ldhName", "N/A").lower(),
                "nameservers": [ns["ldhName"].lower() for ns in data["nameservers"]],
                "registrar": [entities["href"] for entities in data["entities"][0]["links"] ][0],
                "creation_date": creation_human,
                "expiration_date": expiration_human,
                "remaining_time_in_days": remaining_days,
                "status": data.get("status", [])[0] if data.get("status") else "N/A",
    
            }
        elif response.status_code == 404:
            return {"error": f"The domain '{domain}' was not found."}
        else:
            return {"error": f"Error retrieving data. Status code: {response.status_code}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {e}"}


