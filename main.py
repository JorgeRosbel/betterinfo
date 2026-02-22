#!/usr/bin/env python3

import argparse
from utils.whois import whois
from utils.get_tech import get_tech
from utils.find_subdomains import sublist3r_style_search
from pwn import log
from termcolor import colored


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

   
    p1 = log.progress("")
    p1.status(colored(f"Analyzing domain: {args.domain}", "cyan"))
    basic = whois(args.domain)
    if is_active:
        p1.status(colored("Performing technology analysis...", "cyan"))
        tech = get_tech(args.domain)
    p1.status(colored("Finding subdomains...", "cyan"))
    subdomains = sublist3r_style_search(args.domain)
    p1.success(colored("Analysis complete!", "green"))

    
    print(colored("\n----- Whois & Registry Data -----\n", "grey", attrs=["bold"]))

    for key, value in basic.items():
        if isinstance(value, list):
            value = " | ".join(value)
        print(colored(f"{key.capitalize()}: ", "cyan",attrs=["bold"]) + colored(str(value), "yellow"))

    if is_active and tech:
        print(colored("\n----- Technology Analysis -----\n", "grey",attrs=["bold"]))
        if isinstance(tech, str):
            print(colored(tech, "red"))
        else:
            print(colored("Detected: ", "cyan",attrs=["bold"]) + colored(", ".join(tech["technologies"]), "yellow"))

        print(colored("\n----- HTTP Headers -----\n", "grey",attrs=["bold"]))
        if isinstance(tech, str):
            print(colored(tech, "red"))
        else:
            for key, value in tech["headers"].items():
                print(colored(f"{key}: ", "cyan",attrs=["bold"]) + colored(value, "yellow"))

    print(colored("\n----- Subdomains Found -----\n", "grey",attrs=["bold"]))
    
    if not subdomains:
        print(colored("\nNo subdomains found.", "red"))
    else:
        for i, sub in enumerate(subdomains, start=1):
            print(colored(f"{i}. ", "cyan",attrs=["bold"]) + colored(sub, "yellow"))
    


if __name__ == "__main__":
    main()