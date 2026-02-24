import requests

def find_subdomains_passive(domain :str) -> list[str]:
    """
    Performs passive subdomain enumeration by querying Certificate Transparency (CT) logs via crt.sh.

    Args:
        domain (str): The target domain name to search for.

    Returns:
        list[str]: A unique list of discovered subdomains.
    """

    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    subdomains = set()
    
    try:
        response = requests.get(url, timeout=25)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                name_value = entry['name_value'].lower()
                for sub in name_value.split('\n'):
                    clean_sub = sub.replace('*.', '')
                    if clean_sub.endswith(domain) and clean_sub != domain:
                        subdomains.add(clean_sub)
    except:
        pass
        
    return list(subdomains)

def sublist3r_style_search(domain :str) -> list[str]:
    """
    Aggregates subdomains from multiple passive OSINT sources (CRT.sh, HackerTarget, and AlienVault).

    Args:
        domain (str): The target domain name.

    Returns:
        list[str]: A sorted list of unique subdomains found across all sources.
    """
    
    all_subdomains = set()
    
    
    all_subdomains.update(find_subdomains_passive(domain))
    
    
    try:
        res = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        for line in res.text.split('\n'):
            if ',' in line:
                host = line.split(',')[0].lower()
                if host.endswith(domain) and host != domain:
                    all_subdomains.add(host)
    except:
        pass


    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        res = requests.get(url, timeout=15).json()
        for record in res.get('passive_dns', []):
            hostname = record.get('hostname', '').lower()
            if hostname.endswith(domain) and hostname != domain:
                all_subdomains.add(hostname)
    except:
        pass

    return sorted(list(all_subdomains))