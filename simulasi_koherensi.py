
import threading
import time
import random

# Inisialisasi memori bersama dan variabel global
shared_memory = {'x': 0}
lock = threading.Lock()

# Statistik
mesi_messages = 0
conflicts = 0

# Status cache untuk setiap core (simulasi 2 core)
mesi_states = [{} for _ in range(2)]

# Simulasi tanpa protokol koherensi (langsung baca/tulis ke memori)
def simulate_no_coherence(core_id):
    global conflicts
    for _ in range(1000):
        val = shared_memory['x']
        time.sleep(0.001)
        if random.random() < 0.5:
            shared_memory['x'] = val + 1
        else:
            conflicts += 1

# Simulasi dengan protokol MESI
def simulate_with_mesi(core_id):
    global mesi_messages
    cache = mesi_states[core_id]
    for _ in range(1000):
        if 'x' not in cache or cache['x'] == 'I':
            # MISS - baca dari memori
            cache['x'] = 'S'
            mesi_messages += 1  # Bus read

        if random.random() < 0.5:
            # Tulis: perlu invalidasi cache lain
            cache['x'] = 'M'
            mesi_messages += 1  # Invalidate broadcast
            for i, other_cache in enumerate(mesi_states):
                if i != core_id:
                    other_cache['x'] = 'I'
            shared_memory['x'] += 1

# Fungsi utama untuk menjalankan simulasi
def run_simulation(with_mesi=True):
    global mesi_messages, conflicts, shared_memory, mesi_states
    shared_memory = {'x': 0}
    mesi_states = [{} for _ in range(2)]
    mesi_messages = 0
    conflicts = 0

    threads = []
    start = time.time()
    for i in range(2):
        t = threading.Thread(target=simulate_with_mesi if with_mesi else simulate_no_coherence, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    end = time.time()

    print(f"{'Dengan MESI' if with_mesi else 'Tanpa Koherensi'}")
    print(f"Nilai akhir x = {shared_memory['x']}")
    print(f"Waktu: {end - start:.4f} detik")
    if with_mesi:
        print(f"Pesan Koherensi (MESI): {mesi_messages}")
    else:
        print(f"Jumlah Konflik: {conflicts}")
    print("-" * 40)

# Jalankan simulasi
if __name__ == "__main__":
    run_simulation(with_mesi=False)
    run_simulation(with_mesi=True)
