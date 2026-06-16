# End-to-End Machine Learning System: Heart Disease Classification

Repository ini dibuat untuk memenuhi kriteria kelulusan **Submission Akhir** kelas **"Membangun Sistem Machine Learning"** di Dicoding. Proyek ini diimplementasikan menggunakan praktik terbaik industri MLOps untuk mencapai nilai **Advanced (4/4 pts)**.

---

## 📁 Struktur Proyek

```text
├── dataset/
│   └── heart_disease.csv                # Raw Dataset (Cleveland Heart Disease)
├── dataset_preprocessed/
│   ├── train.csv                        # Preprocessed Train Set
│   └── test.csv                         # Preprocessed Test Set
├── .github/
│   └── workflows/
│       └── preprocessing.yml            # Preprocessing CI (Kriteria 1)
├── Membangun_model/
│   ├── modelling.py                     # MLflow Autologging Training (Kriteria 2)
│   └── modelling_tuning.py              # Hyperparameter Tuning + Manual Logging (Kriteria 2)
├── Workflow-CI/                         # Repositori/Folder Kedua (Kriteria 3)
│   ├── .github/workflows/
│   │   └── ci-training.yml              # CI/CD Training & Docker Build/Push
│   ├── dataset/
│   │   └── heart_disease_preprocessed.csv # Dataset Preprocessed
│   ├── MLproject                        # MLflow Project Specification
│   ├── conda.yaml                       # Conda Environment Spec
│   ├── modelling.py                     # Training script for MLproject
│   ├── Dockerfile                       # Dockerfile for serving container
│   ├── requirements.txt                 # Dependencies for Docker build
│   └── prometheus_exporter.py           # Model serving script inside container
├── prometheus/
│   └── prometheus.yml                   # Prometheus Scraping Config (Kriteria 4)
├── requirements.txt                     # Global dependencies
├── Eksperimen_HeartDisease.ipynb       # Jupyter Notebook Eksperimen (Kriteria 1)
├── automate_HeartDisease.py             # Automated Preprocessing Script (Kriteria 1)
├── inference.py                         # Test client for model serving API (Kriteria 4)
├── prometheus_exporter.py               # Model Serving FastAPI & Prometheus Exporter (Kriteria 4)
├── grafana_dashboard.json               # Grafana Dashboard configuration (Kriteria 4)
└── README.md                            # Dokumentasi utama proyek
```

---

## 🛠️ Cara Menjalankan Proyek secara Lokal

### 1. Prasyarat & Instalasi
Pastikan Python 3.10+ telah terinstal. Instal semua dependencies global:
```bash
pip install -r requirements.txt
```

### 2. Jalankan Preprocessing Pipeline (Kriteria 1)
Script `run_pipeline.py` akan membuat dataset raw secara otomatis, menjalankan preprocessing, dan mendistribusikan data:
```bash
python run_pipeline.py
```
Ini akan menghasilkan folder `dataset_preprocessed/` berisi `train.csv` & `test.csv` serta menduplikasi preprocessed data ke folder `Workflow-CI/dataset/`.

### 3. Model Building & Experiment Tracking (Kriteria 2)
* **Training dengan Autologging**:
  ```bash
  python Membangun_model/modelling.py
  ```
  Ini akan merekam metrik secara otomatis menggunakan MLflow. Buka dashboard local MLflow dengan:
  ```bash
  mlflow ui
  ```
* **Hyperparameter Tuning & Manual Logging (DagsHub)**:
  Sebelum menjalankan, pastikan Anda memasukkan username DagsHub dan nama project Anda pada file `Membangun_model/modelling_tuning.py`, atau set melalui environment variables:
  ```bash
  $env:DAGSHUB_USERNAME="USERNAME_DAGSHUB"
  $env:DAGSHUB_REPO="NAMA_REPO_DAGSHUB"
  ```
  Lalu jalankan tuning:
  ```bash
  python Membangun_model/modelling_tuning.py
  ```
  Tuning akan merekam metrik manual dan meng-upload file artifact (`confusion_matrix.png`, `feature_importance.png`, `learning_curve.png`, dll.) ke server DagsHub.

### 4. Serving & Monitoring (Kriteria 4)
* **Jalankan API Server & Exporter**:
  ```bash
  uvicorn prometheus_exporter:app --host 127.0.0.1 --port 8000
  ```
* **Kirim Request Uji Coba**:
  Buka terminal baru dan jalankan:
  ```bash
  python inference.py
  ```
  Script akan mengirimkan payload ke API dan mengembalikan hasil prediksi class target (Normal / Heart Disease).
* **Setup Prometheus & Grafana**:
  Baca panduan lengkap konfigurasi dan alerting pada file [monitoring_setup_guide.md](./monitoring_setup_guide.md).

---

## 📝 Panduan Penilaian Advanced & Reviewer Checklist

Untuk memastikan berkas submission Anda mendapatkan nilai **Advanced (4/4)**, silakan buka file checklist dan panduan screenshot penyerahan berkas berikut:
- [Checklist Nilai Advanced & Screenshot Guide](./dicoding_reviewer_checklist.md)
