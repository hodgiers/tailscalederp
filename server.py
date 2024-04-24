import requests
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import schedule
import time
import logging
from logging.handlers import TimedRotatingFileHandler

def fetch_and_save_ips():
    url = "https://login.tailscale.com/derpmap/default"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = json.loads(response.text)

        ips = []
        def extract_ips(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if 'IPv4' == key:
                        ips.append(value)
                    else:
                        extract_ips(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_ips(item)

        extract_ips(data)

        with open('data.txt', 'w') as file:
            for ip in ips:
                file.write(f"{ip}/32\n")

        # Log success
        logger.info("IPs fetched and saved successfully.")
    except Exception as e:
        # Log failure
        logger.error(f"Failed to fetch and save IPs. Error: {str(e)}")

def run_http_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Serving at port 8000")
    httpd.serve_forever()

def main():
    # Set up logging
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Rotate log file every week
    handler = TimedRotatingFileHandler('fetcher.log', when='W0', backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Fetch and save IPs initially
    fetch_and_save_ips()

    # Run the HTTP server
    run_http_server()

    # Schedule the job to run every hour
    schedule.every().hour.do(fetch_and_save_ips)

    # Run the scheduler in a loop
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
