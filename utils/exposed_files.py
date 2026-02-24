import requests
from termcolor import colored

def check_exposed_files(domain):
    """
    Scans for common exposed files and returns a list of results.
    """
    paths = [
        '/.env', '/.env.local', '/.git/config', '/web.config',
        '/config.php.bak', '/wp-config.php.bak', '/wp-config.php.old',
        '/backup.sql', '/db.sql', '/dump.sql', '/backup.zip', 
        '/phpinfo.php', '/info.php', '/error_log', '/debug.log', 
        '/wp-content/debug.log', '/wp-json/wp/v2/users', '/.htaccess.bak'
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    results = []
    
    for path in paths:
        url = f"https://{domain}/{path.lstrip('/')}"
        print(colored(f"[i] checking for exposed file: {path}", "grey", attrs=["bold"]).ljust(80), end="\r", flush=True)
        try:
            response = requests.get(url, headers=headers, timeout=4, allow_redirects=False)
            status = response.status_code
        except requests.exceptions.RequestException:
            status = "Error"
            
        results.append({
            "tested_path": url,
            "status": status
        })
    print(" " * 100, end="\r", flush=True) 
    return results
