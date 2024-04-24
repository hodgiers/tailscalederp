import requests
import json

def fetch_and_save_ips():
    url = "https://login.tailscale.com/derpmap/default"
    response = requests.get(url)
    data = json.loads(response.text)

    ips = []
    def extract_ips(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if 'IPv4' == key or 'IPv6' == key:
                    ips.append(value)
                else:
                    extract_ips(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_ips(item)

    extract_ips(data)
    print("Extracted IPs:", ips)

    with open('datadebug.txt', 'w') as file:
        for ip in ips:
            file.write(f"{ip}\n")

if __name__ == "__main__":
    fetch_and_save_ips()
