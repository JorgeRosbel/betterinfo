import dns.resolver
from typing import List, TypedDict

class MailServerInfo(TypedDict):
    preference: int
    mail_server: str

def find_mail_server(domain :str) -> List[MailServerInfo]:
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
    

def find_txt_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        return [str(txt_data).strip('"') for txt_data in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, Exception):
        return []