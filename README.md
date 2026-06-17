# 🧪 Eksperimen Data & Preprocessing Pipeline - Heart Disease Classification

[![Automated Preprocessing Pipeline](https://github.com/Kevinadiputra/sistem-ml-dicoding/actions/workflows/preprocessing.yml/badge.svg)](https://github.com/Kevinadiputra/sistem-ml-dicoding/actions/workflows/preprocessing.yml)
[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![MLOps Dicoding](https://img.shields.io/badge/MLOps-Dicoding-green.svg)](https://www.dicoding.com/)

Repositori ini didedikasikan khusus untuk **Kriteria 1 (Eksperimen Data)** dalam proyek tugas akhir Dicoding: **Membangun Sistem Machine Learning (MSML)**. Repositori ini fokus sepenuhnya pada eksplorasi dataset klinis penyakit jantung (Cleveland Heart Disease), analisis statistik, rekayasa fitur, pra-pemrosesan data terstandarisasi, serta otomatisasi alur kerja preprocessing melalui GitHub Actions.

---

## 📊 Dataset & Eksplorasi

Dataset utama yang digunakan adalah **Cleveland Heart Disease** dari UCI Machine Learning Repository. Dataset ini memuat 14 fitur klinis awal dari pasien untuk menentukan prediksi apakah pasien mengidap penyakit jantung atau tidak (fitur `target`).

Tahapan eksplorasi data secara mendalam didokumentasikan di dalam Jupyter Notebook:
* **Lokasi Notebook**: [`Eksperimen_SML_Kevin_Adiputra/preprocessing/Eksperimen_Kevin_Adiputra.ipynb`](file:///Eksperimen_SML_Kevin_Adiputra/preprocessing/Eksperimen_Kevin_Adiputra.ipynb)
* **Cakupan Analisis**:
  * Pemuatan data klinis awal.
  * Analisis statistik deskriptif dan deteksi nilai kosong (*missing values*), duplikasi baris, serta pencilan (*outliers*).
  * Visualisasi sebaran data fitur kontinu (seperti usia, tekanan darah, kolesterol) dan distribusi variabel kelas target.
  * Analisis matriks korelasi fitur kontinu untuk melihat hubungan antar variabel klinis.

---

## ⚙️ Preprocessing Pipeline

Alur pra-pemrosesan data dibangun menggunakan Python untuk mengubah data klinis mentah menjadi format siap pakai yang dioptimalkan untuk pelatihan model machine learning. Langkah-langkah pipeline mencakup:

1. **Pembersihan Data (Cleaning)**:
   * Menghapus baris data duplikat secara otomatis untuk menjaga integritas eksperimen.
   * Mendeteksi dan mengisi nilai kosong (*missing values*) pada fitur `trestbps` (tekanan darah istirahat) dan `chol` (kolesterol) menggunakan nilai **median** dari data latih untuk menghindari bias.
2. **Rekayasa Fitur (Feature Engineering)**:
   * **`chol_bps_ratio`**: Rasio kolesterol terhadap tekanan darah pasien.
   * **`age_group`**: Pengelompokan umur pasien ke dalam 3 kategori utama (Muda: `<45` tahun, Paruh Baya: `45-60` tahun, Lansia: `>60` tahun).
   * **`hr_age_ratio`**: Rasio detak jantung maksimum terhadap usia pasien.
3. **Encoding Variabel Kategorikal**:
   * Melakukan *One-Hot Encoding* (OHE) pada seluruh variabel kategorikal non-biner (`cp` - tipe nyeri dada, `restecg` - hasil EKG, `slope` - kemiringan segmen ST, `thal` - thalasemia, dan fitur baru `age_group`) dengan opsi `drop_first=True` untuk menghindari jebakan multikolinearitas.
4. **Pembagian Dataset (Train-Test Split)**:
   * Membagi dataset menjadi data latih (**80%**) dan data uji (**20%**) dengan metode *Stratified Split* untuk memastikan proporsi kelas target tetap seimbang di kedua set.
5. **Penskalaan Standar (Scaling)**:
   * Menerapkan penskalaan standar (`StandardScaler`) pada seluruh fitur kontinu untuk menstandarisasikan rata-rata = 0 dan varians = 1. Parameter penskalaan hanya dipelajari (*fit*) pada data latih dan diterapkan (*transform*) pada data uji untuk mencegah kebocoran data (*data leakage*).

---

## 🚀 Otomatisasi Pipeline (GitOps)

Alur kerja preprocessing telah diotomatisasi secara penuh menggunakan **GitHub Actions** untuk mewujudkan prinsip GitOps yang andal.

### File Konfigurasi Alur Kerja (Workflow CI)
* **Lokasi Konfigurasi**: [`.github/workflows/preprocessing.yml`](file:///.github/workflows/preprocessing.yml)
* **Aturan Trigger**: Pemicuan alur kerja otomatis terjadi setiap kali terdapat push perubahan pada:
  * File dataset mentah (`Eksperimen_SML_Kevin_Adiputra/dataset_raw/heart_disease.csv`)
  * Script otomatisasi (`Eksperimen_SML_Kevin_Adiputra/preprocessing/automate_Kevin_Adiputra.py`)
* **Langkah Eksekusi Workflow**:
  1. Melakukan checkout repositori.
  2. Menyiapkan runtime environment Python 3.10.
  3. Menginstal pustaka dependensi (pandas, numpy, scikit-learn).
  4. Mengeksekusi script otomatisasi `automate_Kevin_Adiputra.py` untuk memproses ulang data mentah.
  5. Melakukan verifikasi dan commit perubahan hasil preprocessing (`train.csv` dan `test.csv`) kembali ke repositori GitHub secara otomatis menggunakan bot GitHub Actions.

---

## 📁 Struktur Repositori

Repositori ini diatur dengan rapi agar hanya melacak aset eksperimen data dan pra-pemrosesan:

```text
sistem-ml-dicoding/
├── .github/
│   └── workflows/
│       └── preprocessing.yml              # Alur otomatisasi pipeline preprocessing (GitHub Actions)
├── .gitignore                             # Konfigurasi pengabaian berkas non-eksperimen
├── Eksperimen_SML_Kevin_Adiputra/         # Direktori utama eksperimen
│   ├── .workflow/                         # Duplikasi file konfigurasi workflow
│   ├── dataset_raw/
│   │   └── heart_disease.csv              # Dataset klinis penyakit jantung awal (mentah)
│   └── preprocessing/
│       ├── Eksperimen_Kevin_Adiputra.ipynb # Analisis data eksploratif (EDA) & preprocessing notebook
│       ├── automate_Kevin_Adiputra.py      # Script Python otomatisasi preprocessing pipeline
│       ├── dataset_preprocessed/          # Output dataset latih/uji (Format checklist utama)
│       │   ├── train.csv
│       │   └── test.csv
│       └── dataset_preprocessing/         # Output dataset latih/uji (Format spesifik reviewer)
│           ├── train.csv
│           └── test.csv
└── README.md                              # Dokumentasi repositori ini
```

---

## 🛠️ Cara Menjalankan secara Lokal

1. **Klon Repositori**:
   ```bash
   git clone https://github.com/Kevinadiputra/sistem-ml-dicoding.git
   cd sistem-ml-dicoding
   ```
2. **Instal Dependensi**:
   Pastikan Anda menggunakan Python 3.10+. Jalankan perintah instalasi berikut:
   ```bash
   pip install pandas numpy scikit-learn jupyter
   ```
3. **Jalankan Pipeline Preprocessing**:
   Eksekusi script otomatisasi secara langsung dari root direktori proyek:
   ```bash
   python Eksperimen_SML_Kevin_Adiputra/preprocessing/automate_Kevin_Adiputra.py
   ```
   *Script ini akan memproses dataset mentah dan menghasilkan berkas data klinis terstandardisasi `train.csv` dan `test.csv` di dalam folder output.*
