import time
import requests
from urllib.parse import urlparse, parse_qs
from xssniffer.core import scan_xss

def get_website_info(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc

    try:
        response = requests.get(url, timeout=5)
        ip_address = response.raw._connection.sock.getpeername()[0]
        status = "Online"
        last_modified = response.headers.get('Last-Modified', 'Not Available')
    except requests.exceptions.RequestException:
        ip_address = 'N/A'
        status = "Offline"
        last_modified = 'N/A'

    return {
        'hostname': hostname,
        'ip_address': ip_address,
        'status': status,
        'last_modified': last_modified
    }

def start_scan(url, payload_file='payloads.txt', print_output=True):
    website_info = get_website_info(url)

    if print_output:
        print(f"Website Information for {url}:")
        print(f"Hostname: {website_info['hostname']}")
        print(f"IP Address: {website_info['ip_address']}")
        print(f"Status: {website_info['status']}")
        print(f"Last Modified: {website_info['last_modified']}")
        time.sleep(1)
        print("\nStarting XSS scan...")

    params = get_params_from_url(url)
    vulnerabilities = scan_xss(url, params, payload_file)

    if vulnerabilities and print_output:
        for vuln in vulnerabilities:
            print(f"Vulnerability found: {vuln['url']} with payload: {vuln['payload']}")
    elif not vulnerabilities and print_output:
        print("No XSS vulnerabilities found.")

    return vulnerabilities

def get_params_from_url(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return {key: val[0] for key, val in params.items()}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="XSS vulnerability scanner")
    parser.add_argument('--url', type=str, required=True, help="Target URL")
    parser.add_argument('--payloads', type=str, default='payloads.txt', help="Path to the payloads file")
    args = parser.parse_args()

    start_scan(args.url, args.payloads, print_output=True)
