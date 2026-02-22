import socket

def get_ip(domain:str) -> str:
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return "Error: No se pudo resolver el dominio."
