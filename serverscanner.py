import requests
import http.client
from urllib.parse import urlparse
from colorama import Fore, Style, init
import re

# Initialize colorama
init()

# Define known web server and API patterns
web_server_patterns = {
    "Apache": r"Apache(?:/\d+\.\d+\.\d+)?",
    "Nginx": r"nginx(?:/\d+\.\d+\.\d+)?",
    "IIS": r"Microsoft-IIS(?:/\d+\.\d+)?",
    "Lighttpd": r"lighttpd(?:/\d+\.\d+\.\d+)?",
}

api_patterns = {
    "Apache Portable Runtime": r"APR(?:/\d+\.\d+)?",
    "Nginx C API": r"Nginx(?: API| C API)",
    "HTTP API": r"HTTP(?: API)?",
    "IIS Metabase": r"IIS Metabase",
    "ASP.NET": r"ASP\.NET(?: Core)?",
    "FastCGI": r"FastCGI",
    "SCGI": r"SCGI",
    "WSGI": r"WSGI",
    "AJP": r"AJP(?:/\d+\.\d+)?",
    "Modularity API": r"Modularity API",
}

def scan_website(target_url):
    try:
        # Validate and parse URL
        parsed_url = urlparse(target_url)
        if not parsed_url.scheme:
            target_url = "http://" + target_url
            parsed_url = urlparse(target_url)

        print(f"{Fore.YELLOW}[*] Scanning target: {target_url}{Style.RESET_ALL}")

        # Fetch headers
        response = requests.head(target_url, timeout=5)
        headers = response.headers

        # Extract web server information
        server_header = headers.get("Server", "Unknown")
        print(f"{Fore.GREEN}[+] Server Header: {server_header}{Style.RESET_ALL}")

        # Detect web server type
        detected_server = "Unknown"
        for server, pattern in web_server_patterns.items():
            if re.search(pattern, server_header, re.IGNORECASE):
                detected_server = server
                break
        print(f"{Fore.CYAN}[+] Detected Web Server: {detected_server}{Style.RESET_ALL}")

        # Detect API type from headers
        detected_api = "Unknown"
        for api_name, pattern in api_patterns.items():
            for key, value in headers.items():
                if re.search(pattern, f"{key}: {value}", re.IGNORECASE):
                    detected_api = api_name
                    break
            if detected_api != "Unknown":
                break
        print(f"{Fore.CYAN}[+] Detected API: {detected_api}{Style.RESET_ALL}")

        # Analyze deeper with HTTP OPTIONS method
        conn = http.client.HTTPConnection(parsed_url.netloc, timeout=5)
        conn.request("OPTIONS", "/")
        options_response = conn.getresponse()
        allow_header = options_response.getheader("Allow")

        if allow_header:
            print(f"{Fore.CYAN}[+] HTTP Methods Allowed: {allow_header}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] No HTTP Allow Header Found{Style.RESET_ALL}")

        conn.close()

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] Error accessing target: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Unexpected error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.BLUE}Optimized Web Server and API Scanner{Style.RESET_ALL}")
    target = input(f"{Fore.YELLOW}Enter the target URL: {Style.RESET_ALL}")
    scan_website(target)
