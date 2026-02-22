#!/usr/bin/env python3

import argparse
from utils.whois import whois
from utils.get_tech import get_tech



import json


def main():
   
    parser = argparse.ArgumentParser(description="Gather domain information from a given domain name.")
    parser.add_argument("domain", help="The domain name to query (e.g., google.com)")
    
    args = parser.parse_args()
    basic = whois(args.domain)
    tech = get_tech(args.domain)
    
    print(json.dumps(basic, indent=4))
    print(json.dumps(tech, indent=4))



if __name__ == "__main__":
    main()