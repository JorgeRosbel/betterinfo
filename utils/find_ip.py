import socket

def get_ip(domain: str) -> str:
    """
    Resolves a domain name to its corresponding IPv4 address.

    Args:
        domain (str): The domain name to resolve (e.g., 'example.com').

    Returns:
        str: The resolved IP address or an error message if the domain cannot be resolved.
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return "Error: Could not resolve domain."