#!/usr/bin/env python3

import argparse
from utils.whois import whois
from utils.find_tech import find_tech
from utils.find_subdomains import sublist3r_style_search
from utils.find_ip import get_ip
from pwn import log
from termcolor import colored
from utils.find_location import get_geo_location
from utils.find_mail_servers import find_mail_server, find_txt_records
from utils.sitemaps_robots import find_sitemaps, find_robots

def main():
   
    parser = argparse.ArgumentParser(description="Gather domain information from a given domain name.")
    parser.add_argument("domain", help="The domain name to query (e.g., google.com)")
    parser.add_argument(
        "-a", "--active",
        dest="active",
        action="store_true",
        help="Modo de escaneo: pasivo (consultas a APIs) o activo (interacción directa)"
    )

    args = parser.parse_args()

    is_active = args.active 
    tech = None
    ip_address = None
    sitemaps = None
    robots = None

   
    p1 = log.progress("")
    p1.status(colored(f"Analyzing domain: {args.domain}", "cyan"))
    basic = whois(args.domain)
    if is_active:
        p1.status(colored("Performing technology analysis...", "cyan"))
        tech = find_tech(args.domain)
        ip_address = get_ip(args.domain)
    p1.status(colored("Finding subdomains...", "cyan"))
    subdomains = sublist3r_style_search(args.domain)

    if is_active:
        p1.status(colored("Searching for sitemaps and robots.txt...", "cyan"))
        sitemaps = find_sitemaps(args.domain)
        robots = find_robots(args.domain)
    p1.success(colored("Analysis complete!", "green"))

    
    print(colored("\n----- Whois & Registry Data -----\n", "grey", attrs=["bold"]))

    for key, value in basic.items():
        if isinstance(value, list):
            value = " | ".join(value)
        print(colored(f"{key.capitalize()}: ", "cyan",attrs=["bold"]) + colored(str(value), "yellow"))
    
    if ip_address:
        print(colored(f"Edge IP Address: ", "cyan",attrs=["bold"]) + colored(ip_address, "yellow"))

    if is_active and tech and not isinstance(tech, str):
        print(colored("\n----- Technology Analysis -----\n", "grey",attrs=["bold"]))
        
        for i, tech_name in enumerate(tech["technologies"], start=1):
            print(colored(f"{i}. ", "cyan",attrs=["bold"]) + colored(tech_name, "yellow"))

    

        print(colored("\n----- HTTP Response Headers -----\n", "grey",attrs=["bold"]))
        if isinstance(tech, str):
            print(colored(tech, "red"))
        else:
            for key, value in tech["headers"].items():
                if value == "Not Found":
                    print(colored(f"{key}: ", "cyan",attrs=["bold"]) + colored(value, "red"))
                else:                    
                    print(colored(f"{key}: ", "cyan",attrs=["bold"]) + colored(value, "yellow"))
            

    print(colored("\n----- Subdomains Found -----\n", "grey",attrs=["bold"]))
    
    if not subdomains:
        print(colored("\n[!] No subdomains found.", "red", attrs=["bold"]))
        print(colored(
            "    Note: This could be due to API rate limits or the domain having no public records.\n"
            "    Suggestions:\n"
            "    - Try again in a few minutes.\n",
            "yellow"
        ))
    else:
        for i, sub in enumerate(subdomains, start=1):
            print(colored(f"{i}. ", "cyan",attrs=["bold"]) + colored(sub, "yellow"))


    location = get_geo_location(ip_address) if ip_address else None
    if location:
        print(colored("\n----- Geolocation Data -----\n", "grey",attrs=["bold"]))
        print(colored(f"Country: ", "cyan",attrs=["bold"]) + colored(location['country'], "yellow"))
        print(colored(f"City: ", "cyan",attrs=["bold"]) + colored(location['city'], "yellow"))
        print(colored(f"Internet Service Provider: ", "cyan",attrs=["bold"]) + colored(location['isp'], "yellow"))
        print(colored(f"Coordinates: ", "cyan",attrs=["bold"]) + colored(location['coordinates'], "yellow"))

    mail_servers = find_mail_server(args.domain)
    if mail_servers:
        print(colored("\n----- Mail Servers (MX Records) -----\n", "grey",attrs=["bold"]))
        for mx in mail_servers:
            print(f"{colored('Preference:', 'cyan', attrs=['bold'])} {colored(mx['preference'], 'yellow')}, {colored('Server:', 'cyan', attrs=['bold'])} {colored(mx['mail_server'], 'yellow')}")


    txt_records = find_txt_records(args.domain)
    if txt_records:
        print(colored("\n----- TXT Records -----\n", "grey",attrs=["bold"]))
        for record in txt_records:
            if "v=spf1" in record:
                print(f"[*] {colored('SPF (Email Security):', 'yellow')} {record}")
                if "~all" in record:
                    print(colored("    [!] Warning: Policy is set to SoftFail (~all).", "red"))
            else:
                print(f"[-] {record}")

    if is_active:
        print(colored("\n----- Internal URLs Found -----\n", "grey",attrs=["bold"]))
        if sitemaps:
            for i, sitemap in enumerate(sitemaps, start=1):
                print(colored(f"{i}. ", "cyan",attrs=["bold"]) + colored(sitemap, "yellow"))
        else:
            print(colored("\n[!] No sitemaps found or accessible.", "red", attrs=["bold"]))

        print(colored("\n----- robots.txt Content -----\n", "grey",attrs=["bold"]))
        if robots:
            print(colored(robots, "yellow"))
        else:
            print(colored("\n[!] No robots.txt found or accessible.", "red", attrs=["bold"]))

        print(colored("\n-----END OF ANALYSIS-----", "grey"))
    


if __name__ == "__main__":
    main()