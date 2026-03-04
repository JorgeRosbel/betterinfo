import dns.resolver
import requests
from termcolor import colored

def check_email_security(domain):
    # Initialize the report dictionary
    report = {
        "domain": domain,
        "dmarc": {"status": "Missing", "record": None, "policy": None, "risk": "High"},
        "dkim": {"status": "Not Found", "selectors_tested": [], "active_selector": None},
        "reputation": {"score": None, "status": "Unknown", "warning": False}
    }
    
    # 1. Verify DMARC
    try:
        dmarc_target = f"_dmarc.{domain}"
        records = dns.resolver.resolve(dmarc_target, 'TXT')
        for record in records:
            rec_str = str(record).lower()
            report["dmarc"]["status"] = "Found"
            report["dmarc"]["record"] = rec_str
            if "p=reject" in rec_str:
                report["dmarc"]["policy"] = "reject"
                report["dmarc"]["risk"] = "Critical (Silent Delete)"
            elif "p=quarantine" in rec_str:
                report["dmarc"]["policy"] = "quarantine"
                report["dmarc"]["risk"] = "Medium (Goes to Spam)"
            else:
                report["dmarc"]["policy"] = "none"
                report["dmarc"]["risk"] = "High (No enforcement)"
    except Exception:
        pass

    # 2. Verify DKIM
    selectors = ['default', 'google', 'hostinger', 's1', 'mail']
    report["dkim"]["selectors_tested"] = selectors
    for s in selectors:
        try:
            target = f"{s}._domainkey.{domain}"
            dns.resolver.resolve(target, 'TXT')
            report["dkim"]["status"] = "Found"
            report["dkim"]["active_selector"] = s
            break
        except Exception:
            continue

    # 3. Reputation Check
    try:
        response = requests.get(f"https://api.mailaudit.io/tools/reputation?domain={domain}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            score = data.get('score', 0)
            report["reputation"]["score"] = score
            report["reputation"]["status"] = "Poor" if int(score) < 70 else "Good"
            report["reputation"]["warning"] = True if int(score) < 70 else False
    except Exception:
        pass

    return report

