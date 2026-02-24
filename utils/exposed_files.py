import requests
from termcolor import colored
import time
from typing import TypedDict, List

class ExposedFileResult(TypedDict):
    tested_path: str
    status: int | str


def check_exposed_files(domain, rate_limit: int | float | None = None) -> List[ExposedFileResult] | None:
    """
    Scans for common exposed files and returns a list of results.
    """
    paths = [
    '/.env', '/.env.local', '/.env.prod', '/.env.dev', '/.env.bak', 
    '/.aws/credentials', '/.vscode/sftp.json', '/.ssh/id_rsa',
    '/.git/config', '/.git/index', '/.gitignore', '/.svn/entries',
    '/wp-config.php.bak', '/wp-config.php.old', '/wp-config.php.save', '/wp-config.php~',
    '/wp-content/debug.log', '/wp-content/uploads/debug.log',
    '/wp-json/wp/v2/users', '/wp-links-opml.php', '/xmlrpc.php',
    '/backup.sql', '/db.sql', '/db_backup.sql', '/database.sql', '/dump.sql',
    '/db.zip', '/backup.zip', '/site.zip', '/www.zip', '/old.zip',
    '/latest.tar.gz', '/site.tar.gz', '/backup.tar.gz', '/full.sql',
    '/phpinfo.php', '/info.php', '/status', '/server-status',
    '/error_log', '/error.log', '/access.log', '/debug.log',
    '/.htaccess.bak', '/.htpasswd', '/web.config',
    '/package.json', '/composer.json', '/composer.lock', 
    '/.npmrc', '/yarn.lock', '/docker-compose.yml',
    '/backup/', '/backups/', '/css/', '/js/', '/images/', '/uploads/', 
    '/sql/', '/temp/', '/tmp/', '/old/'
]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    results = []
    
    for i,path in enumerate(paths, start=1):
        url = f"https://{domain}/{path.lstrip('/')}"
        print(colored(f"[i] checking for exposed file: {path} ({i}/{len(paths)})", "grey", attrs=["bold"]).ljust(80), end="\r", flush=True)
        if rate_limit:
            time.sleep(rate_limit)
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
