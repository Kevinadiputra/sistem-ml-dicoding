# Panduan Konfigurasi Monitoring & Alerting (Kriteria 4)

Dokumen ini berisi langkah-step instalasi, konfigurasi, dan pengujian untuk sistem monitoring berbasis **FastAPI + Prometheus + Grafana** beserta konfigurasi **Alerting**.

---

## 1. Menjalankan Model Serving (FastAPI App)

Aplikasi FastAPI di `prometheus_exporter.py` menggabungkan inference API (`/predict`) dengan pengeksporan metrics (`/metrics`).

Jalankan server locally dengan Uvicorn:
```bash
uvicorn prometheus_exporter:app --host 0.0.0.0 --port 8000 --reload
```
Aplikasi akan running di `http://localhost:8000`. 
- **Endpoint API**: `http://localhost:8000/predict` (POST)
- **Endpoint Metrics**: `http://localhost:8000/metrics` (GET)

---

## 2. Menjalankan Prometheus

Prometheus akan mengumpulkan (scrape) data metric dari `/metrics` setiap 5 detik.

### Langkah Setup:
1. Download Prometheus dari official site.
2. Gunakan file konfigurasi `prometheus.yml` yang telah kita generate:
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
3. Jalankan Prometheus server:
   * **Windows/CLI**: `prometheus.exe --config.file=prometheus.yml`
   * **Docker (Alternatif)**:
     ```bash
     docker run -d -p 9090:9090 -v D:\KULIAH\ID CAMP\MEMBANGUN SISTEM MACHINE LEARNING\prometheus\prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
     ```
4. Buka dashboard Prometheus di `http://localhost:9090` and verifikasi bahwa status target Up di menu **Status -> Targets**.

---

## 3. Menjalankan Grafana & Import Dashboard

Grafana digunakan untuk memvisualisasikan data dari Prometheus.

### Langkah Setup:
1. Jalankan Grafana server:
   * **Docker**:
     ```bash
     docker run -d -p 3000:3000 grafana/grafana
     ```
2. Buka Grafana di `http://localhost:3000` (Default login: `admin` / `admin`).
3. Tambahkan **Prometheus** sebagai **Data Source**:
   * Masuk ke **Connections -> Data sources -> Add data source**.
   * Pilih **Prometheus**.
   * Set URL ke `http://localhost:9090` (atau `http://host.docker.internal:9090` jika running di Docker).
   * Klik **Save & test**.
4. Import Dashboard:
   * Klik menu **Dashboards -> New -> Import**.
   * Upload file `grafana_dashboard.json` yang ada di root project, atau salin isinya.
   * Ganti judul dashboard dengan nama **Username Dicoding Anda** di kolom *Dashboard Name*.
   * Pilih data source Prometheus yang baru dibuat.
   * Klik **Import**.

---

## 4. Konfigurasi Grafana Alerting (3 Alerts)

Berdasarkan ketentuan kriteria Advanced, berikut adalah langkah konfigurasi untuk 3 alert wajib:

### Alert 1: High Latency (> 2 Second)
Alert ini terpicu jika rata-rata durasi response API model serving lebih dari 2 detik.
1. Di Grafana, buka **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama alert: `High Latency Alert`.
3. Di bagian query, masukkan query berikut (PromQL):
   ```promql
   api_response_time_seconds_sum / (api_response_time_seconds_count + 1e-5)
   ```
4. Di bagian **Condition**, set evaluasi setiap `10s` selama `30s` (for `30s`).
5. Set threshold condition: **IS ABOVE** `2`.
6. Tentukan folder dan evaluation group (buat baru jika belum ada, misal folder `MLOps Alerts` dengan evaluasi group `every-10s`).
7. Klik **Save and exit**.

### Alert 2: High CPU (> 80%)
Alert ini terpicu jika penggunaan CPU host container serving melebihi 80%.
1. Masuk ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama alert: `High CPU Alert`.
3. Di bagian query, masukkan query berikut:
   ```promql
   cpu_usage_percent
   ```
4. Di bagian **Condition**, set evaluasi setiap `10s` selama `30s`.
5. Set threshold condition: **IS ABOVE** `80`.
6. Pilih folder `MLOps Alerts` dan group `every-10s`.
7. Klik **Save and exit**.

### Alert 3: Error Rate (> 5%)
Alert ini terpicu jika rasio kegagalan/error API melebihi 5% dari total requests.
1. Masuk ke **Alerting -> Alert rules -> Create rule**.
2. Masukkan nama alert: `High Error Rate Alert`.
3. Di bagian query, masukkan query berikut untuk mendeteksi persentase rate error terhadap total request:
   ```promql
   (rate(error_count_total[1m]) / (rate(request_count_total[1m]) + 1e-5)) * 100
   ```
4. Di bagian **Condition**, set evaluasi setiap `10s` selama `30s`.
5. Set threshold condition: **IS ABOVE** `5` (merepresentasikan 5%).
6. Pilih folder `MLOps Alerts` dan group `every-10s`.
7. Klik **Save and exit**.

---

## 5. Cara Pengujian Sistem (Simulation)

Untuk memicu data metrics dan memverifikasi visualisasi Grafana:
1. Jalankan API: `uvicorn prometheus_exporter:app`.
2. Jalankan script client untuk mengirim batch inference:
   ```bash
   python inference.py
   ```
3. Buka dashboard Grafana untuk memantau perubahan metric secara real-time.
