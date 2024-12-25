import requests
import concurrent.futures
import time

# Daftar endpoint umum ASP.NET
COMMON_ENDPOINTS = [
    "/", "/home", "/about", "/contact", "/login", "/logout", "/api/values",
    "/products", "/services", "/admin", "/dashboard"
]

# Fungsi untuk memindai endpoint valid dengan metode GET
def scan_endpoint(host, endpoint):
    try:
        url = f"{host}{endpoint}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"[VALID] {url} - {response.status_code}")
            return endpoint
    except requests.RequestException:
        pass
    return None

# Fungsi untuk stres tes endpoint dengan metode GET atau POST
def stress_test(host, endpoint, duration, method="GET", payload=None):
    url = f"{host}{endpoint}"
    start_time = time.time()
    print(f"Starting stress test on {url} with method {method} for {duration} seconds...")
    while time.time() - start_time < duration:
        try:
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                response = requests.post(url, json=payload, timeout=5)
            print(f"[{response.status_code}] {url}")
        except requests.RequestException as e:
            print(f"[ERROR] {url} - {e}")

# Fungsi utama
def main():
    host = input("Masukkan URL server (contoh: https://your-aspnet-server.com): ").strip()
    duration = int(input("Masukkan durasi stres tes (detik): "))
    method = input("Pilih metode HTTP (GET/POST): ").strip().upper()

    # Jika metode POST, minta payload JSON
    payload = None
    if method == "POST":
        payload = input("Masukkan payload JSON untuk POST (contoh: {\"key\": \"value\"}): ").strip()
        try:
            payload = eval(payload)  # Konversi string ke dict
        except Exception as e:
            print(f"[ERROR] Payload tidak valid: {e}")
            return

    print("\n[INFO] Memindai endpoint valid...")
    valid_endpoints = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_endpoint = {executor.submit(scan_endpoint, host, ep): ep for ep in COMMON_ENDPOINTS}
        for future in concurrent.futures.as_completed(future_to_endpoint):
            result = future.result()
            if result:
                valid_endpoints.append(result)

    if not valid_endpoints:
        print("\n[TIDAK DITEMUKAN] Tidak ada endpoint valid yang ditemukan.")
        return

    print("\n[VALID] Endpoint valid ditemukan:")
    for endpoint in valid_endpoints:
        print(f" - {endpoint}")

    print("\n[INFO] Memulai stres tes...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        for endpoint in valid_endpoints:
            executor.submit(stress_test, host, endpoint, duration, method, payload)

if __name__ == "__main__":
    main()
