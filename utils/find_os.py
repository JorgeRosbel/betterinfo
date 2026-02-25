import subprocess
import platform
import re
from typing import Optional


def get_ttl(ip: str) -> Optional[int]:
    """
    Sends a single ICMP ping to the specified IP address
    and extracts the TTL (Time To Live) value from the response.

    Args:
        ip (str): The target IP address or hostname.

    Returns:
        Optional[int]: The TTL value if successfully extracted,
        otherwise None if the ping fails or TTL is not found.

    Notes:
        - Works on both Windows and Unix-based systems.
        - Requires the system 'ping' command to be available.
        - May fail if ICMP requests are blocked by firewall rules.
    """

    system = platform.system().lower()

    if system == "windows":
        cmd = ["ping", "-n", "1", ip]
    else:
        cmd = ["ping", "-c", "1", ip]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout

        match = re.search(r"ttl[=\s:]*?(\d+)", output, re.IGNORECASE)

        if match:
            return int(match.group(1))

    except Exception:
        pass

    return None


def find_os(ip:str)->str:

    ttl = get_ttl(ip)

    if not ttl:
        return "Not Found"

    if ttl >= 0 and ttl <= 64:
        return "Linux"
    elif ttl >= 65 and ttl <= 128:
        return "Windows"
    else:
        return "Not Found"
