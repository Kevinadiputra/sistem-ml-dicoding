# Panduan Evaluasi Mandiri dan Screenshot Penyerahan Berkas

Dokumen ini memuat daftar kebutuhan screenshot wajib untuk dilampirkan dalam dokumentasi proyek serta checklist evaluasi kelayakan sistem sesuai standar kriteria tugas akhir.

---

## 1. Daftar Screenshot Wajib

Dokumentasi visual berikut diperlukan untuk memverifikasi fungsionalitas sistem yang tidak dapat diuji secara langsung oleh penilai:

### Kriteria 1: Preprocessing & GitHub Actions
1. **GitHub Actions Preprocessing Run**: Screenshot halaman eksekusi workflow GitHub Actions yang menunjukkan file workflow `preprocessing.yml` berhasil berjalan saat terjadi event push.
2. **Git Commit History**: Screenshot riwayat commit pada repositori GitHub yang membuktikan bot github-actions berhasil menambahkan atau memperbarui file data latih `train.csv` dan data uji `test.csv` di direktori `dataset_preprocessed/`.

### Kriteria 2: Model Experimentation & DagsHub MLflow
3. **MLflow Local Dashboard**: Screenshot halaman dashboard MLflow lokal (`mlflow ui`) setelah pengeksekusian script `modelling.py` dengan fitur autologging aktif.
4. **DagsHub MLflow Experiments**: Screenshot dashboard MLflow pada platform DagsHub setelah pengeksekusian script `modelling_tuning.py` yang menampilkan parameter hasil pencarian GridSearchCV, metrik performa, dan daftar artefak visualisasi (Confusion Matrix, Feature Importance, Learning Curve) di server registri DagsHub.

### Kriteria 3: Workflow CI (Repositori Kedua)
5. **GitHub Actions Workflow CI Run**: Screenshot halaman eksekusi workflow `ci-training.yml` pada repositori kedua (`Workflow-CI`) yang berhasil berjalan dari langkah checkout hingga kompilasi dan pengunggahan Docker image.
6. **Docker Hub Image Repository**: Halaman akun Docker Hub yang menampilkan image model serving berhasil diunggah dengan tag `:latest`.

### Kriteria 4: Monitoring & Alerting
7. **FastAPI inference API & /metrics**:
   - Dokumentasi antarmuka Swagger FastAPI (`http://localhost:8000/docs`) yang memuat endpoint `/predict` dan `/metrics`.
   - Tampilan respon browser pada endpoint `/metrics` yang menyajikan deretan nilai metrik Prometheus.
8. **Prometheus Targets Active**: Halaman **Status -> Targets** pada server Prometheus (`http://localhost:9090`) yang menampilkan status target endpoint model serving dalam keadaan **UP**.
9. **Grafana Dashboard**: Dashboard Grafana yang dinamai dengan identitas Anda, memvisualisasikan nilai metrik secara live setelah pengujian inferensi.
10. **Grafana Alerting Rules**: Halaman **Alerting -> Alert rules** pada Grafana yang menampilkan status aturan peringatan (High Latency, High CPU, Error Rate) dalam kondisi aktif.

---

## 2. Checklist Evaluasi Kelayakan Sistem

Berikut poin-poin verifikasi sistem sebelum berkas proyek diserahkan:

### Kriteria 1: Eksperimen Data
- [ ] Berkas notebook eksperimen `Eksperimen_Kevinadiputra.ipynb` berada di direktori `preprocessing/`.
- [ ] Notebook memuat tahap pemuatan data, analisis deskriptif lengkap (nilai kosong, duplikasi, pencilan, sebaran data, hubungan korelasi, variabel target), serta pra-pemrosesan data (penanganan nilai kosong/duplikat, rekayasa fitur, encoding, penskalaan, dan pembagian data).
- [ ] File hasil pra-pemrosesan data tersimpan di folder `dataset_preprocessed/`.
- [ ] Script otomatisasi `automate_Kevinadiputra.py` memuat fungsi utama: `load_data()`, `clean_data()`, `feature_engineering()`, `preprocess()`, `save_dataset()`, dan `main()`.
- [ ] File alur kerja GitHub Actions `.github/workflows/preprocessing.yml` terkonfigurasi dengan benar untuk mendeteksi event push, memicu script otomatisasi pra-pemrosesan, dan melakukan commit hasil pemrosesan secara otomatis.

### Kriteria 2: Pembuatan Model
- [ ] Folder `Membangun_model/` memuat berkas `modelling.py` dan `modelling_tuning.py`.
- [ ] Script `modelling.py` menerapkan fitur `mlflow.autolog()` untuk mencatat metrik dan parameter model secara otomatis.
- [ ] Script `modelling_tuning.py` menerapkan optimasi hyperparameter menggunakan `GridSearchCV` dengan pencatatan metrik secara manual (manual logging).
- [ ] Pencatatan manual menyimpan parameter model terbaik, metrik performa (Accuracy, Precision, Recall, F1-Score), serta minimal 5 artefak visualisasi evaluasi model.
- [ ] Integrasi DagsHub MLflow menggunakan library `dagshub` terkonfigurasi untuk mengunggah pelacakan eksperimen pemodelan secara jarak jauh (remote registry).
- [ ] File daftar pustaka dependensi `requirements.txt` diletakkan di root project.

### Kriteria 3: Alur Integrasi Berkelanjutan (CI)
- [ ] Berkas alur kerja dipisahkan ke repositori kedua bernama `Workflow-CI`.
- [ ] File `MLproject` mendefinisikan environment `conda.yaml` dan perintah pengeksekusian script training model.
- [ ] File `conda.yaml` memuat daftar dependensi pustaka Python yang dibutuhkan dalam training model.
- [ ] File workflow `.github/workflows/ci-training.yml` memuat urutan langkah penyiapan conda environment, pengeksekusian MLflow project, pengarsipan artefak hasil run, otentikasi akun Docker Hub, serta pembangunan dan pengunggahan Docker image ke Docker Hub.
- [ ] File instruksi build `Dockerfile` tersedia di direktori `Workflow-CI`.

### Kriteria 4: Pemantauan & Deployment
- [ ] Berkas `prometheus_exporter.py` menggabungkan model serving (FastAPI) dan pengeksporan metrik ke dalam satu script.
- [ ] Berkas client `inference.py` dikonfigurasi untuk mengirimkan payload data pengujian format JSON ke endpoint prediksi dan mencetak respon output.
- [ ] Pengeksporan metrik menyediakan minimal 10 metrik sistem dan pemodelan yang relevan.
- [ ] File konfigurasi Prometheus `prometheus/prometheus.yml` terkonfigurasi dengan target server penarikan metrik.
- [ ] File konfigurasi dashboard `grafana_dashboard.json` tersedia di root project dan siap untuk diimpor ke aplikasi Grafana.
- [ ] Pengaturan aturan peringatan (alert rules) pada Grafana mencakup 3 alert wajib (High Latency, High CPU, Error Rate) beserta petunjuk implementasi lengkap pada dokumentasi.
