# Panduan Konfigurasi Pemantauan dan Peringatan (Monitoring & Alerting)

Dokumen ini berisi panduan langkah-langkah instalasi, konfigurasi, pengujian sistem pemantauan (FastAPI + Prometheus + Grafana), dan pengaturan sistem peringatan (Alerting).

---

## 1. Menjalankan Model Serving (Aplikasi FastAPI)

Aplikasi FastAPI pada `prometheus_exporter.py` menggabungkan API inferensi (`/predict`) dan pengeksporan metrik (`/metrics`).

Jalankan server secara lokal menggunakan Uvicorn:
```bash
uvicorn prometheus_exporter:app --host 0.0.0.0 --port 8000 --reload
```
Aplikasi akan berjalan di `http://localhost:8000`.
- **Endpoint API**: `http://localhost:8000/predict` (POST)
- **Endpoint Metrik**: `http://localhost:8000/metrics` (GET)

---

## 2. Menjalankan Prometheus

Prometheus mengambil (scrape) metrik dari `/metrics` setiap 5 detik.

### Langkah Setup:
1. Unduh Prometheus dari situs resmi.
2. Gunakan konfigurasi pada file `prometheus.yml`:
   ```yaml
   global:
     scrape_interval: 5s
     evaluation_interval: 5s

   scrape_configs:
     - job_name: 'heart-disease-api-monitoring'
       metrics_path: '/metrics'
       static_configs:
         - targets: ['localhost:8000']
   ```
3. Jalankan server Prometheus:
   * **Windows/CLI**: `prometheus.exe --config.file=prometheus.yml`
   * **Docker**:
     ```bash
     docker run -d -p 9090:9090 -v D:\KULIAH\ID CAMP\MEMBANGUN SISTEM MACHINE LEARNING\prometheus\prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
     ```
4. Verifikasi status target pada menu **Status -> Targets** di `http://localhost:9090` hingga berstatus **UP**.

---

## 3. Menjalankan Grafana dan Impor Dashboard

Grafana digunakan untuk visualisasi metrik yang diperoleh dari Prometheus.

### Langkah Setup:
1. Jalankan server Grafana:
   * **Docker**:
     ```bash
     docker run -d -p 3000:3000 grafana/grafana
     ```
2. Akses Grafana melalui `http://localhost:3000` (kredensial default: `admin` / `admin`).
3. Tambahkan **Prometheus** sebagai **Data Source**:
   * Navigasi ke **Connections -> Data sources -> Add data source**.
   * Pilih **Prometheus**.
   * Masukkan URL server Prometheus `http://localhost:9090` (atau `http://host.docker.internal:9090` jika menggunakan Docker).
   * Klik **Save & test**.
4. Impor Dashboard:
   * Navigasi ke **Dashboards -> New -> Import**.
   * Unggah file `grafana_dashboard.json` dari repositori proyek.
   * Ganti nama dashboard pada kolom *Dashboard Name* sesuai dengan nama identitas Anda.
   * Pilih data source Prometheus yang sesuai.
   * Klik **Import**.

---

## 4. Konfigurasi Sistem Peringatan Grafana (Grafana Alerting)

Berikut konfigurasi untuk 6 jenis peringatan (alerts) yang diterapkan pada sistem:

### Alert 1: High Latency (> 2 Second)
Mendeteksi jika rata-rata waktu respon API model serving melebihi 2 detik.
1. Navigasi ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama aturan: `High Latency Alert`.
3. Masukkan query PromQL:
   ```promql
   api_response_time_seconds_sum / (api_response_time_seconds_count + 1e-5)
   ```
4. Pada bagian **Condition**, atur evaluasi setiap `10s` dengan durasi evaluasi `30s`.
5. Atur batas ambang (threshold): **IS ABOVE** `2`.
6. Tentukan folder penyimpanan aturan (misalnya folder `MLOps Alerts` dengan grup evaluasi `every-10s`).
7. Simpan aturan.

### Alert 2: High CPU (> 80%)
Mendeteksi jika penggunaan CPU pada container serving melebihi 80%.
1. Navigasi ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama aturan: `High CPU Alert`.
3. Masukkan query:
   ```promql
   cpu_usage_percent
   ```
4. Atur evaluasi setiap `10s` dengan durasi `30s`.
5. Atur batas ambang: **IS ABOVE** `80`.
6. Simpan aturan ke folder `MLOps Alerts` grup `every-10s`.

### Alert 3: Error Rate (> 5%)
Mendeteksi jika persentase kegagalan permintaan API serving melebihi 5% dari total permintaan.
1. Navigasi ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama aturan: `High Error Rate Alert`.
3. Masukkan query:
   ```promql
   (rate(error_count_total[1m]) / (rate(request_count_total[1m]) + 1e-5)) * 100
   ```
4. Atur evaluasi setiap `10s` dengan durasi `30s`.
5. Atur batas ambang: **IS ABOVE** `5` (merepresentasikan 5%).
6. Simpan aturan ke folder `MLOps Alerts` grup `every-10s`.

### Alert 4: High Memory Usage (> 85%)
Mendeteksi risiko kegagalan sistem akibat kebocoran memori (memory leak) di atas 85%.
1. Navigasi ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama aturan: `High Memory Alert`.
3. Masukkan query:
   ```promql
   memory_usage_percent
   ```
4. Atur evaluasi setiap `10s` dengan durasi `1m`.
5. Atur batas ambang: **IS ABOVE** `85`.
6. Simpan aturan ke folder `MLOps Alerts` grup `every-10s`.

### Alert 5: High Disk Space Usage (> 90%)
Mendeteksi jika kapasitas penyimpanan container hampir penuh (melebihi 90%).
1. Navigasi ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama aturan: `High Disk Usage Alert`.
3. Masukkan query:
   ```promql
   disk_usage_percent
   ```
4. Atur evaluasi setiap `10s` dengan durasi `1m`.
5. Atur batas ambang: **IS ABOVE** `90`.
6. Simpan aturan ke folder `MLOps Alerts` grup `every-10s`.

### Alert 6: API Error Spike (Absolute Errors > 5 dalam 1 Menit)
Mendeteksi jika terjadi lonjakan error absolut sebanyak lebih dari 5 kali dalam periode 1 menit.
1. Navigasi ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama aturan: `API Error Spike Alert`.
3. Masukkan query:
   ```promql
   increase(error_count_total[1m])
   ```
4. Atur evaluasi setiap `10s` dengan durasi `1m`.
5. Atur batas ambang: **IS ABOVE** `5`.
6. Simpan aturan ke folder `MLOps Alerts` grup `every-10s`.

---

## 5. Simulasi Pengujian Sistem

Untuk memverifikasi visualisasi dashboard Grafana dan pengiriman metrik:
1. Jalankan API model serving lokal: `uvicorn prometheus_exporter:app`.
2. Jalankan script simulasi pengirim inferensi:
   ```bash
   python inference.py
   ```
3. Pantau perubahan nilai pada visualisasi dashboard Grafana untuk memastikan metrik terupdate secara real-time.
