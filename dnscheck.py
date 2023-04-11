#!/usr/bin/env python3

import os
import re
import sys
import subprocess

def run_dnsrecon(domain):
    print(f"Running dnsrecon command for {domain}. This may take a few minutes...")

    command = f"python3 dnsrecon.py -d {domain} -D subdomains-top1mil-20000.txt -t brt > out.txt"
    subprocess.run(command, shell=True, check=True)


def read_ips_from_file(file_path):
    with open(file_path, "r") as file:
        ips = [ip.strip() for ip in file.readlines()]
    return ips


def extract_domains_and_ips_from_data(data_file_path):
    with open(data_file_path, "r") as f:
        lines = f.readlines()

    domains_and_ips = []
    for line in lines:
        if "A" in line:
            domain_match = re.findall(r'\S+', line)
            ip_match = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)

            if domain_match and ip_match:
                domain_name = domain_match[-2]
                domains_and_ips.append((domain_name, ip_match[0]))

    return domains_and_ips


def check_ips_against_list(data_file_path, ip_list_file_path):
    ip_list = read_ips_from_file(ip_list_file_path)
    domains_and_ips = extract_domains_and_ips_from_data(data_file_path)

    matched_domains_and_ips = [(domain, ip) for domain, ip in domains_and_ips if ip in ip_list]

    return matched_domains_and_ips


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dnscheck.py <domain> <ip_file>")
        sys.exit(1)

    domain = sys.argv[1]
    ip_file = sys.argv[2]

    run_dnsrecon(domain)

    matched_domains_and_ips = check_ips_against_list("out.txt", ip_file)

    if matched_domains_and_ips:
        print("Matched Domains and IPs:")
        for domain, ip in matched_domains_and_ips:
            print(f"Domain: {domain}, IP: {ip}")
    else:
        print("No matched domains and IPs found.")
