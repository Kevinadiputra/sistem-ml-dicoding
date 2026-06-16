# Klasifikasi Penyakit Jantung Menggunakan Sistem Machine Learning End-to-End

Repository ini berisi implementasi sistem klasifikasi penyakit jantung berbasis machine learning secara end-to-end. Proyek ini mencakup seluruh siklus pengembangan mulai dari pra-pemrosesan data, pelacakan eksperimen pemodelan, integrasi sirkuit integrasi berkelanjutan (CI/CD), hingga penyajian model (serving) dan pemantauan (monitoring).

## Dataset
Dataset yang digunakan dalam proyek ini adalah Cleveland Heart Disease dari UCI Machine Learning Repository yang berisi informasi klinis pasien seperti usia, jenis kelamin, tipe nyeri dada, tekanan darah, kadar kolesterol, dan detak jantung maksimum.

## Alur Pengerjaan

1. **Pra-pemrosesan Data (Kriteria 1)**
   - Menghapus baris data duplikat.
   - Mengisi nilai kosong pada variabel `trestbps` dan `chol` dengan nilai median.
   - Rekayasa fitur: membuat variabel baru `chol_bps_ratio`, `age_group`, dan `hr_age_ratio`.
   - Melakukan One-Hot Encoding pada fitur kategorikal non-biner.
   - Membagi dataset menjadi data latih (80%) dan data uji (20%) secara terstrata.
   - Penskalaan standar menggunakan StandardScaler pada variabel kontinu.

2. **Pemodelan & Pelacakan Eksperimen (Kriteria 2)**
   - Melatih model klasifikasi menggunakan Random Forest Classifier.
   - Melakukan pelacakan otomatis (autologging) parameter dan metrik evaluasi model dengan MLflow secara lokal.
   - Melakukan penalaan hyperparameter (hyperparameter tuning) dengan GridSearchCV dan merekam parameter terbaik, metrik evaluasi (Accuracy, Precision, Recall, F1-Score), serta artefak visualisasi ke registri MLflow di DagsHub secara manual.

3. **Workflow CI (Kriteria 3)**
   - Mengintegrasikan kode pemodelan ke dalam folder terpisah sebagai proyek MLflow (`Workflow-CI`).
   - Menyusun alur integrasi berkelanjutan (GitHub Actions) untuk memicu proses training secara otomatis, menguji performa model, dan membangun serta mengunggah Docker image berisi model serving ke Docker Hub.

4. **Serving & Pemantauan (Kriteria 4)**
   - Membuka model serving menggunakan FastAPI dengan endpoint `/predict`.
   - Mengintegrasikan Prometheus Client untuk mengekspor metrik sistem dan performa model lewat endpoint `/metrics`.
   - Menghubungkan Prometheus server untuk mengambil metrik dari aplikasi FastAPI.
   - Menyusun dashboard visualisasi di Grafana untuk memantau metrik secara real-time.
   - Menyiapkan aturan peringatan (alert rules) pada Grafana jika terjadi lonjakan latensi, tingginya beban CPU, atau tingginya tingkat error pada server.

## Struktur Direktori

```text
├── dataset/
│   └── heart_disease.csv                  # Dataset mentah (Cleveland Heart Disease)
├── .github/
│   └── workflows/
│       └── preprocessing.yml              # Alur kerja otomatis pra-pemrosesan data
├── Membangun_model/
│   ├── dataset_preprocessed/              # Salinan data hasil pra-pemrosesan untuk pemodelan
│   │   ├── train.csv
│   │   └── test.csv
│   ├── modelling.py                       # Script pelatihan model dengan MLflow autologging
│   └── modelling_tuning.py                # Script hyperparameter tuning dengan DagsHub MLflow
├── preprocessing/
│   ├── dataset_preprocessed/              # Output dataset hasil pra-pemrosesan
│   │   ├── train.csv
│   │   └── test.csv
│   ├── Eksperimen_Kevinadiputra.ipynb     # Dokumentasi eksperimen dan analisis data (Jupyter)
│   └── automate_Kevinadiputra.py           # Script otomatisasi pra-pemrosesan data
├── Workflow-CI/                           # Repositori terpisah untuk pipeline CI
│   ├── .github/workflows/
│   │   └── ci-training.yml                # Alur kerja CI training dan build/push Docker
│   ├── dataset/
│   │   └── heart_disease_preprocessed.csv # Salinan data pra-pemrosesan untuk CI
│   ├── MLproject                          # Spesifikasi proyek MLflow
│   ├── conda.yaml                         # Spesifikasi environment conda
│   ├── modelling.py                       # Script pelatihan model untuk proyek MLflow
│   ├── Dockerfile                         # Spesifikasi kontainer Docker untuk deployment
│   ├── requirements.txt                   # Dependensi instalasi kontainer
│   └── prometheus_exporter.py             # Script model serving dengan metrics exporter
├── prometheus/
│   └── prometheus.yml                     # Konfigurasi pengumpulan metrik Prometheus
├── requirements.txt                       # Daftar dependensi utama proyek
├── inference.py                           # Script simulasi pengiriman data ke server serving
├── prometheus_exporter.py                 # Script model serving lokal FastAPI & Prometheus
├── grafana_dashboard.json                 # Konfigurasi dashboard visualisasi Grafana
└── README.md                              # Dokumentasi proyek
```

## Cara Menjalankan Proyek secara Lokal

### 1. Instalasi Dependensi
Pastikan Python 3.10 ke atas telah terinstal. Instal seluruh pustaka dependensi yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 2. Pra-pemrosesan Data
Jalankan script otomatisasi berikut untuk menghasilkan data hasil pra-pemrosesan:
```bash
python run_pipeline.py
```
Script ini akan memproses dataset mentah dan menghasilkan file `train.csv` serta `test.csv` di direktori `dataset_preprocessed/`, sekaligus memperbarui salinan data di dalam folder `Workflow-CI/dataset/`.

### 3. Pemodelan dan Pelacakan
- **Autologging Lokal**:
  ```bash
  python Membangun_model/modelling.py
  ```
  Visualisasikan hasil eksperimen pemodelan lokal melalui dashboard MLflow:
  ```bash
  mlflow ui
  ```
- **Hyperparameter Tuning (DagsHub)**:
  Atur kredensial akun DagsHub terlebih dahulu menggunakan environment variables:
  ```bash
  $env:DAGSHUB_USERNAME="Username_DagsHub"
  $env:DAGSHUB_REPO="Nama_Repository"
  ```
  Kemudian jalankan proses penalaan parameter:
  ```bash
  python Membangun_model/modelling_tuning.py
  ```
  Metrik evaluasi beserta grafik visualisasi (Confusion Matrix, Feature Importance, Learning Curve) akan diunggah ke server registri MLflow DagsHub.

### 4. Serving dan Pemantauan
- **Menjalankan Server Serving**:
  ```bash
  uvicorn prometheus_exporter:app --host 127.0.0.1 --port 8000
  ```
- **Melakukan Uji Coba Prediksi**:
  Jalankan script berikut di terminal terpisah untuk mensimulasikan permintaan prediksi ke API server:
  ```bash
  python inference.py
  ```
- **Mengaktifkan Prometheus dan Grafana**:
  Panduan konfigurasi Prometheus, pembuatan dashboard di Grafana, serta aktivasi rules alerting dapat dilihat pada file [monitoring_setup_guide.md](./monitoring_setup_guide.md).
