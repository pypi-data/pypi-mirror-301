import requests

def scan_xss(url, params, payload_file):
    vulnerabilities = []
    
    with open(payload_file, 'r') as f:
        payloads = [payload.strip() for payload in f.readlines()]

    for payload in payloads:
        for param in params:
            test_url = f"{url}?{param}={payload}"
            try:
                response = requests.get(test_url, timeout=5)
                
                if payload in response.text:
                    vulnerabilities.append({
                        'url': test_url,
                        'payload': payload,
                        'response': response.text[:100]
                    })
            except requests.exceptions.RequestException as e:
                print(f"")
    
    return vulnerabilities
