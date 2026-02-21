#!/usr/bin/env python3

import argparse
from utils.whois import whois



import json


def main():
   
    parser = argparse.ArgumentParser(description="Gather domain information from a given domain name.")
    parser.add_argument("domain", help="The domain name to query (e.g., google.com)")
    
    args = parser.parse_args()
    resultado = whois(args.domain)
    
    print(json.dumps(resultado, indent=4))

if __name__ == "__main__":
    main()