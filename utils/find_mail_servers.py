import dns.resolver
from typing import List, TypedDict

class MailServerInfo(TypedDict):
    preference: int
    mail_server: str

def find_mail_server(domain :str) -> List[MailServerInfo]:
    """
    Retrieves MX (Mail Exchange) records for a given domain to identify mail servers.

    Args:
        domain (str): The target domain name.

    Returns:
        List[dict]: A list of dictionaries containing 'preference' and 'mail_server',
                    or an empty list if no records are found.
    """
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [
            {
                "preference": rdata.preference, 
                "mail_server": str(rdata.exchange).rstrip('.')
            } 
            for rdata in answers
        ]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, Exception):
        return []
    

def find_txt_records(domain :str) -> List[str]:
    """
    Fetches all TXT records for a domain, often used for SPF, DKIM, or site verification.

    Args:
        domain (str): The target domain name.

    Returns:
        List[str]: A list of strings containing the TXT record data, 
                   or an empty list if no records are found.
    """
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        return [str(txt_data).strip('"') for txt_data in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, Exception):
        return []