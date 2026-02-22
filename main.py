#!/usr/bin/env python3

import argparse
from utils.whois import whois
from utils.get_tech import get_tech
from pwn import log
from termcolor import colored


def main():
   
    parser = argparse.ArgumentParser(description="Gather domain information from a given domain name.")
    parser.add_argument("domain", help="The domain name to query (e.g., google.com)")
    
    args = parser.parse_args()
    p1 = log.progress("")
    p1.status(colored(f"Analyzing domain: {args.domain}", "cyan"))
    basic = whois(args.domain)
    p1.status(colored("Performing technology analysis...", "cyan"))
    tech = get_tech(args.domain)
    p1.success(colored("Analysis complete!", "green"))
    
    print(colored("\n----- Whois & Registry Data -----\n", "grey", attrs=["bold"]))

    for key, value in basic.items():
        if isinstance(value, list):
            value = " | ".join(value)
        print(colored(f"{key.capitalize()}: ", "cyan",attrs=["bold"]) + colored(str(value), "yellow"))

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
    


if __name__ == "__main__":
    main()