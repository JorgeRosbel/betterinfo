#!/usr/bin/env python3

import re
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
from utils.exposed_files import check_exposed_files
from utils.find_os import find_os

def validate_domain(domain):
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain)

def main():
   
    parser = argparse.ArgumentParser(description="Gather domain information from a given domain name.")
    parser.add_argument("domain", help="The domain name to query (e.g., domain.com)")
    parser.add_argument(
        "-r", "--rate-limit",
        dest="rate_limit",
        help="Set a custom rate limit (in seconds) between API requests to avoid hitting rate limits. Default is none (no delay).", 
    )
    parser.add_argument(
        "-a", "--active",
        dest="active",
        action="store_true",
        help="Active Scan: Direct interaction with the target"
    )
    parser.add_argument(
        "-oN", "--output-name",
        dest="output_name",
        help="Set a custom output file name (default is domain_report.txt).", 
    )
   
    

    args = parser.parse_args()

    if not validate_domain(args.domain):
        print(colored("Error: Invalid domain format. Please provide a valid domain (e.g., domain.com).", "red"))
        return

    is_active = args.active 
    tech = None
    ip_address = None
    sitemaps = None
    robots = None
    exposed_files = None
    o_system = None

   
    p1 = log.progress("")
    p1.status(colored(f"Analyzing domain: {args.domain}", "cyan"))
    basic = whois(args.domain)
    if is_active:
        p1.status(colored("Performing technology analysis...", "cyan"))
        tech = find_tech(args.domain)
        ip_address = get_ip(args.domain)
        o_system = find_os(ip_address)

    p1.status(colored("Finding subdomains...", "cyan"))
    subdomains = sublist3r_style_search(args.domain)

    if is_active:
        rate = f"(rate_limit:{args.rate_limit}s)" if args.rate_limit else "(no rate limit)"
        rate_limit=float(args.rate_limit) if args.rate_limit else None
        p1.status(colored(f"Searching for sitemaps and robots.txt... {rate}", "cyan"))
        sitemaps = find_sitemaps(args.domain, rate_limit=rate_limit)
        robots = find_robots(args.domain)
        p1.status(colored(f"Checking for exposed files... {rate}", "cyan"))
        exposed_files = check_exposed_files(args.domain, rate_limit=rate_limit)
    p1.success(colored("Analysis complete!", "green"))


    print(colored("\n----- Website Metadata -----\n", "grey", attrs=["bold"]))
    if tech and isinstance(tech, dict) and "metadata" in tech:
        metadata = tech["metadata"]
        for key, value in metadata.items():
            print(colored(f"{key.capitalize()}: ", "cyan",attrs=["bold"]) + colored(str(value), "yellow"))

    if is_active and o_system:
        print(colored("\n----- Operative System -----\n", "grey", attrs=["bold"]))
        print(colored(f"{o_system}", "yellow" ))


    
    print(colored("\n----- Whois & Registry Data -----\n", "grey", attrs=["bold"]))

    for key, value in basic.items():
        if isinstance(value, list):
            value = " | ".join(value)
        print(colored(f"{key.capitalize()}: ", "cyan",attrs=["bold"]) + colored(str(value), "yellow"))
    
    if ip_address:
        print(colored(f"Edge IP Address: ", "cyan",attrs=["bold"]) + colored(ip_address, "yellow"))

    if is_active and tech and isinstance(tech, dict):
        print(colored("\n----- Technology Analysis -----\n", "grey",attrs=["bold"]))
        for i, tech_name in enumerate(tech["technologies"], start=1):
            print(colored(f"{i}. ", "cyan",attrs=["bold"]) + colored(tech_name, "yellow"))
        
        if len(tech["plugins"]) > 0:
            print(colored("\n----- WordPress Plugins Found -----\n", "grey",attrs=["bold"]))
            for i, plugin in enumerate(tech["plugins"], start=1):
                print(colored(f"Plugin {i}: ", "cyan",attrs=["bold"]) + colored(f"{plugin['name']} (Version: {plugin['version']})", "yellow"))

        print(colored("\n----- HTTP Response Headers -----\n", "grey",attrs=["bold"]))
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
        lat, long = location["coordinates"].split(",")
        print(colored("Google Maps URL: ", "cyan", attrs=["bold"]) + colored(f"https://www.google.com/maps/@{lat.replace(" ", "")},{long.replace(" ", "")},15z", "yellow") )

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

        print(colored("\n----- Exposed Files Check -----\n", "grey",attrs=["bold"]))
        if exposed_files:
            for entry in exposed_files:
                if entry["status"] == 200:
                    status_color = colored(entry["status"], "green")
                    text_info = colored(" [Potentially Exposed]", "red")
                    path_info = colored(f"{entry['tested_path']}: ", "cyan",attrs=["bold"])
                elif entry["status"] in [401, 403]:
                    status_color = colored(entry["status"], "yellow") 
                    text_info = colored(" [Access Restricted]", "yellow")
                    path_info = colored(f"{entry['tested_path']}: ", "cyan",attrs=["bold"])
                else:
                    status_color = colored(entry["status"], "grey")
                    text_info = colored(" [Not Found]", "grey", attrs=["bold"])
                    path_info = colored(f"{entry['tested_path']}: ", "grey",attrs=["bold"])
            
                print(path_info + status_color + text_info)


            print(colored("\nSummary: ", "cyan",attrs=["bold"]) + colored(f"{sum(1 for e in exposed_files if e['status'] == 200)} potentially exposed files found.", "yellow"))
        else:
            print(colored("\n[!] No exposed files found or accessible.", "red", attrs=["bold"]))

    print(colored("\n-----END OF ANALYSIS-----", "grey"))

    file_name = args.output_name if args.output_name else None

    if not file_name:
        return
    
    full_text = f"""
----- Website Metadata -----
Title: {tech['metadata']['title'] if tech and isinstance(tech, dict) and 'metadata' in tech else 'N/A'}
Description: {tech['metadata']['description'] if tech and isinstance(tech, dict) and 'metadata' in tech else 'N/A'}

----- Operative System -----
{o_system}

----- Whois & Registry Data -----
{chr(10).join([f"{key.capitalize()}: {value if not isinstance(value, list) else ' | '.join(value)}" for key, value in basic.items()])}
Edge IP Address: {ip_address if ip_address else 'N/A'}

----- Technology Analysis -----
{chr(10).join([f"{i}. {tech_name}" for i, tech_name in enumerate(tech['technologies'], start=1)]) if tech and isinstance(tech, dict) and 'technologies' in tech else 'N/A'}

--- WordPress Plugins Found ---
{chr(10).join([f"Plugin {i}: {plugin['name']} (Version: {plugin['version']})" for i, plugin in enumerate(tech['plugins'], start=1)]) if tech and isinstance(tech, dict) and 'plugins' in tech and len(tech['plugins']) > 0 else 'N/A'}

----- Subdomains Found -----
{chr(10).join([f"{i}. {sub}" for i, sub in enumerate(subdomains, start=1)]) if subdomains else 'N/A'}

----- Geolocation Data -----
Country: {location['country'] if location else 'N/A'}
City: {location['city'] if location else 'N/A'}
Internet Service Provider: {location['isp'] if location else 'N/A'}
Coordinates: {location['coordinates'] if location else 'N/A'}

----- Mail Servers (MX Records) -----
{chr(10).join([f"Preference: {mx['preference']}, Server: {mx['mail_server']}" for mx in mail_servers]) if mail_servers else 'N/A'}

----- TXT Records -----
{chr(10).join([f"{record}" for record in txt_records]) if txt_records else 'N/A'}

----- Internal URLs Found -----
{chr(10).join([f"{i}. {sitemap}" for i, sitemap in enumerate(sitemaps, start=1)]) if sitemaps else 'N/A'}

----- robots.txt Content -----
{robots if robots else 'N/A'}

----- Exposed Files Check -----
{chr(10).join([
    f"{entry['tested_path']}: {entry['status']} {'[Potentially Exposed]' if entry['status'] == 200 else '[Access Restricted]'}" 
    for entry in exposed_files 
    if entry['status'] in [200, 401, 403]
]) if exposed_files else 'N/A'}
Summary: {sum(1 for e in exposed_files if e['status'] == 200) if exposed_files else 0} potentially exposed files found.
-----END OF ANALYSIS-----   
        """
    
   
    
    with open(file_name, "w") as f:
        f.write(full_text)
        print(colored(f"\nReport saved to {file_name}", "green", attrs=["bold"]))

    



if __name__ == "__main__":
    main()