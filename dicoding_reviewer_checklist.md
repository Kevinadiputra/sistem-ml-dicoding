# Dicoding Submission Checklist & Screenshot Guide (Advanced 4/4)

Dokumen ini berisi panduan screenshot wajib untuk dilampirkan dalam README proyek Anda dan checklist evaluasi agar mendapatkan nilai **Advanced (4/4)** dari reviewer.

---

## 1. Daftar Screenshot Wajib untuk Reviewer

Karena reviewer tidak selalu bisa menjalankan Docker container atau Prometheus secara langsung di environment mereka, **melampirkan screenshot berikut sangat krusial** untuk mempermudah reviewer memverifikasi sistem Anda:

### Kriteria 1: Preprocessing & GitHub Actions
1. **GitHub Actions Preprocessing Run**: Screenshot halaman run workflow GitHub Actions yang menunjukkan workflow `preprocessing.yml` sukses dijalankan pada event push.
2. **Git Commit History**: Screenshot history commit di repository GitHub yang membuktikan bot github-actions berhasil menambahkan/meng-update file `dataset_preprocessed/train.csv` dan `test.csv`.

### Kriteria 2: Model Experimentation & DagsHub MLflow
3. **MLflow Local Dashboard**: Screenshot dashboard MLflow local (`mlflow ui`) setelah menjalankan `modelling.py` dengan autologging, menunjukkan parameters, metrics, dan model logged.
4. **DagsHub MLflow Experiments**: Screenshot dashboard MLflow di platform DagsHub Anda setelah menjalankan `modelling_tuning.py`, yang menunjukkan parameters hasil tuning GridSearchCV, metrics, dan list artifacts (`confusion_matrix.png`, `feature_importance.png`, `learning_curve.png`, dll.) tersimpan di remote registry.

### Kriteria 3: Workflow CI (Second Repository)
5. **GitHub Actions Workflow CI Run**: Halaman run workflow `ci-training.yml` di repository kedua (`Workflow-CI`) sukses dari tahap checkout sampai build & push Docker image.
6. **Docker Hub Image Repository**: Halaman Docker Hub account Anda yang menampilkan image model serving baru saja di-push dengan tag `:latest`.

### Kriteria 4: Monitoring & Alerting
7. **FastAPI inference API & /metrics**:
   * API Docs Swagger (`http://localhost:8000/docs`) menunjukkan endpoint `/predict` dan `/metrics`.
   * Screenshot browser saat membuka endpoint `/metrics` yang menampilkan value dari 10 metrics Prometheus.
8. **Prometheus Targets Active**: Halaman **Status -> Targets** di Prometheus (`http://localhost:9090`) menunjukkan status target endpoint model serving dalam keadaan **UP**.
9. **Grafana Dashboard**: Dashboard Grafana yang dinamai dengan **Username Dicoding Anda** menampilkan visualisasi dari 10 metrics secara live setelah Anda melakukan request menggunakan `inference.py`.
10. **Grafana Alerting Rules**: Halaman **Alerting -> Alert rules** di Grafana yang menampilkan status rule alert (High Latency, High CPU, Error Rate) aktif.

---

## 2. Checklist Detail Penilaian Advanced (4/4)

Pastikan semua poin di bawah ini tercentang sebelum Anda mengunggah berkas zip submission:

### Kriteria 1: Experimentation (Advanced)
* [ ] **Notebook Eksperimen**: File `Eksperimen_HeartDisease.ipynb` ada di root project.
* [ ] **Eksperimen Lengkap**: Notebook berisi loading data, EDA lengkap (missing values, duplicates, outliers, distribution, correlation, target), preprocessing (handling missing/duplicates, feature engineering, encoding, scaling, train-test split).
* [ ] **Output Preprocessed**: Data hasil preprocessing disimpan ke dalam folder `dataset_preprocessed/`.
* [ ] **Script Otomatisasi**: File `automate_HeartDisease.py` memiliki fungsi: `load_data()`, `clean_data()`, `feature_engineering()`, `preprocess()`, `save_dataset()`, dan `main()`.
* [ ] **Preprocessing CI**: File `.github/workflows/preprocessing.yml` terkonfigurasi dengan benar untuk mendeteksi push, menjalankan python preprocessing, dan meng-commit hasilnya secara otomatis.

### Kriteria 2: Model Building (Advanced)
* [ ] **Membangun Model**: Terdapat folder `Membangun_model/` berisi `modelling.py` and `modelling_tuning.py`.
* [ ] **Automatic Logging**: Script `modelling.py` menggunakan `mlflow.autolog()` untuk merekam metrics dan models secara otomatis.
* [ ] **Hyperparameter Tuning**: Script `modelling_tuning.py` menggunakan `GridSearchCV` atau `RandomizedSearchCV` tanpa autolog (menggunakan manual logging).
* [ ] **Manual Logs**: Menyimpan parameter tuning, metrics (accuracy, precision, recall, f1), dan minimal 5 artifacts (`confusion_matrix.png`, `feature_importance.png`, `classification_report.txt`, `learning_curve.png`, `prediction_distribution.png`).
* [ ] **Remote Tracking (DagsHub)**: Terintegrasi dengan `dagshub.init()` untuk mengarahkan tracking MLflow ke dashboard DagsHub Anda.
* [ ] **Dependencies**: File `requirements.txt` ter-generate lengkap dan diletakkan di root project.

### Kriteria 3: Workflow CI (Advanced)
* [ ] **Repositori CI**: File project diletakkan di folder/repositori kedua `Workflow-CI` yang terpisah.
* [ ] **MLProject File**: File `MLproject` mendefinisikan environment `conda.yaml` dan perintah running `python modelling.py`.
* [ ] **Conda Environment**: File `conda.yaml` mendefinisikan dependencies Python dan CLI library yang dibutuhkan untuk project.
* [ ] **Workflow CI-Training**: File `.github/workflows/ci-training.yml` memproses checkout, install dependencies, run MLflow project, compress/upload artifacts, login Docker Hub, serta build dan push Docker image ke Docker Hub.
* [ ] **Dockerfile**: Terdapat `Dockerfile` di folder `Workflow-CI` untuk model serving.

### Kriteria 4: Monitoring (Advanced)
* [ ] **FastAPI Serving & Metrics**: File `prometheus_exporter.py` menggabungkan FastAPI model serving dan pengeksporan metrics dalam 1 script.
* [ ] **Inference Client**: File `inference.py` dapat mengirimkan JSON request ke model dan mencetak respon output.
* [ ] **Minimal 10 Metrics**: Pengeksporan metrics mencakup minimal 10 metric wajib (prediction count, latency, request count, error count, cpu, memory, disk, accuracy, throughput, response time).
* [ ] **Prometheus Config**: File `prometheus/prometheus.yml` terkonfigurasi untuk men-scrape metrics dari target server.
* [ ] **Grafana Dashboard JSON**: File `grafana_dashboard.json` ada di root project, siap di-import, dan menampilkan visualisasi kesepuluh metric.
* [ ] **Alerting Rules**: Menyetel 3 rule alert di Grafana (High Latency > 2s, High CPU > 80%, Error Rate > 5%) dengan petunjuk setup lengkap di dokumentasi.
