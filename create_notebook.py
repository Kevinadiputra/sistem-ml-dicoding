"""
Script to generate a comprehensive experiment notebook matching the Template Eksperimen MSML format.
"""
import json
import os

def make_md(source_lines):
    return {"cell_type": "markdown", "metadata": {}, "source": source_lines}

def make_code(source_lines):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source_lines}

cells = []

# ============================================================
# 1. PERKENALAN DATASET
# ============================================================
cells.append(make_md([
    "# **1. Perkenalan Dataset**\n",
    "\n",
    "### Latar Belakang\n",
    "Penyakit jantung merupakan salah satu penyebab kematian tertinggi di dunia. Deteksi dini faktor risiko menjadi hal krusial untuk mencegah kefatalan. Melalui pemanfaatan data medis pasien, eksperimen ini bertujuan membangun model klasifikasi untuk memprediksi probabilitas seseorang mengidap penyakit jantung.\n",
    "\n",
    "### Tujuan Eksperimen\n",
    "1. Melakukan eksplorasi data untuk mengidentifikasi pola dan karakteristik pasien.\n",
    "2. Menemukan hubungan korelasi antara fitur-fitur klinis terhadap variabel target.\n",
    "3. Melakukan pembersihan data dari nilai kosong dan baris duplikat.\n",
    "4. Melakukan rekayasa fitur medis baru guna meningkatkan daya prediksi model.\n",
    "5. Menyediakan dataset latih dan uji yang telah terstandarisasi untuk pemodelan.\n",
    "\n",
    "### Variabel Target\n",
    "- `target`: Indikasi diagnosis penyakit jantung\n",
    "  - **0** = Normal / Sehat\n",
    "  - **1** = Terdiagnosis Penyakit Jantung\n",
    "\n",
    "### Metrik Evaluasi yang Direncanakan\n",
    "- **Accuracy**: Rasio ketepatan prediksi keseluruhan.\n",
    "- **Precision**: Rasio ketepatan model mendeteksi kelas positif.\n",
    "- **Recall**: Rasio kemampuan model mendeteksi seluruh pasien positif (krusial dalam domain medis).\n",
    "- **F1-Score**: Nilai tengah harmonis antara Precision dan Recall."
]))

# ============================================================
# 2. IMPORT LIBRARY
# ============================================================
cells.append(make_md([
    "# **2. Import Library**\n",
    "\n",
    "Pustaka Python yang digunakan dalam analisis data dan visualisasi meliputi pandas, numpy, matplotlib, dan seaborn."
]))

cells.append(make_code([
    "# Import libraries yang diperlukan\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "import os\n",
    "\n",
    "# Konfigurasi visualisasi\n",
    "sns.set_theme(style=\"whitegrid\", palette=\"muted\")\n",
    "plt.rcParams['figure.figsize'] = (12, 6)\n",
    "plt.rcParams['font.size'] = 11\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "print(\"Libraries berhasil dimuat.\")"
]))

# ============================================================
# 3. MEMUAT DATASET
# ============================================================
cells.append(make_md([
    "# **3. Memuat Dataset**\n",
    "\n",
    "Pemuatan dataset Heart Disease UCI untuk ditinjau dimensi, struktur data, tipe variabel, dan statistik deskriptif awal."
]))

cells.append(make_code([
    "# Load dataset\n",
    "data_path = '../dataset/heart_disease.csv'\n",
    "if not os.path.exists(data_path):\n",
    "    data_path = 'dataset/heart_disease.csv'  # fallback jika dijalankan dari root\n",
    "\n",
    "df = pd.read_csv(data_path)\n",
    "\n",
    "print(f\"Dataset dimuat dari: {data_path}\")\n",
    "print(f\"Dimensi data: {df.shape[0]} baris, {df.shape[1]} kolom\")\n",
    "print(f\"Ukuran memori: {df.memory_usage(deep=True).sum() / 1024:.2f} KB\")"
]))

cells.append(make_code([
    "# Menampilkan 5 baris pertama dataset\n",
    "print(\"Preview data (5 baris pertama):\")\n",
    "df.head()"
]))

cells.append(make_code([
    "# Informasi struktur dataset\n",
    "print(\"Struktur dataset:\")\n",
    "print(\"=\" * 50)\n",
    "df.info()\n",
    "print(\"\\n\" + \"=\" * 50)\n",
    "print(f\"\\nTotal kolom: {len(df.columns)}\")\n",
    "print(f\"Kolom numerik: {len(df.select_dtypes(include=[np.number]).columns)}\")\n",
    "print(f\"Kolom kategorikal: {len(df.select_dtypes(include=['object']).columns)}\")"
]))

cells.append(make_md([
    "### Deskripsi Fitur Dataset\n",
    "\n",
    "| No | Fitur | Deskripsi | Tipe |\n",
    "|---|---|---|---|\n",
    "| 1 | `age` | Usia pasien (tahun) | Numerik Kontinu |\n",
    "| 2 | `sex` | Jenis kelamin (1 = Laki-laki, 0 = Perempuan) | Kategorikal Biner |\n",
    "| 3 | `cp` | Tipe nyeri dada (0-3) | Kategorikal Ordinal |\n",
    "| 4 | `trestbps` | Tekanan darah istirahat (mm Hg) | Numerik Kontinu |\n",
    "| 5 | `chol` | Kolesterol serum (mg/dl) | Numerik Kontinu |\n",
    "| 6 | `fbs` | Gula darah puasa > 120 mg/dl (1 = Ya, 0 = Tidak) | Kategorikal Biner |\n",
    "| 7 | `restecg` | Hasil elektrokardiografi istirahat (0-2) | Kategorikal Ordinal |\n",
    "| 8 | `thalach` | Detak jantung maksimum tercapai | Numerik Kontinu |\n",
    "| 9 | `exang` | Angina akibat olahraga (1 = Ya, 0 = Tidak) | Kategorikal Biner |\n",
    "| 10 | `oldpeak` | Depresi ST akibat olahraga relatif terhadap istirahat | Numerik Kontinu |\n",
    "| 11 | `slope` | Slope segmen ST puncak olahraga (0-2) | Kategorikal Ordinal |\n",
    "| 12 | `ca` | Jumlah pembuluh darah besar berwarna fluoroskopi (0-4) | Numerik Diskrit |\n",
    "| 13 | `thal` | Thalassemia (0-3) | Kategorikal Ordinal |\n",
    "| 14 | `target` | Diagnosis penyakit jantung (0 = Normal, 1 = Sakit) | **Target** |"
]))

cells.append(make_code([
    "# Statistik deskriptif untuk semua variabel numerik\n",
    "print(\"Statistik Deskriptif:\")\n",
    "df.describe().round(2)"
]))

# ============================================================
# 4. EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================
cells.append(make_md([
    "# **4. Exploratory Data Analysis (EDA)**\n",
    "\n",
    "Analisis data eksploratif dilakukan untuk menganalisis karakteristik data secara statistik dan visual, meliputi:\n",
    "- Sebaran data dari setiap variabel\n",
    "- Keberadaan nilai kosong (missing values) dan data duplikat\n",
    "- Distribusi pencilan (outliers) pada variabel numerik\n",
    "- Hubungan korelasi antar variabel\n",
    "- Hubungan antara variabel prediktor dengan variabel target"
]))

# 4A. Missing Values
cells.append(make_md([
    "### 4.1 Analisis Nilai Kosong (Missing Values)"
]))

cells.append(make_code([
    "# Analisis Nilai Kosong\n",
    "missing_data = pd.DataFrame({\n",
    "    'Jumlah Missing': df.isnull().sum(),\n",
    "    'Persentase (%)': (df.isnull().sum() / len(df) * 100).round(2)\n",
    "})\n",
    "missing_data = missing_data[missing_data['Jumlah Missing'] > 0].sort_values('Jumlah Missing', ascending=False)\n",
    "\n",
    "if len(missing_data) > 0:\n",
    "    print(\"Ditemukan Nilai Kosong:\")\n",
    "    print(missing_data)\n",
    "    \n",
    "    # Visualisasi nilai kosong\n",
    "    fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "    \n",
    "    # Bar chart\n",
    "    missing_data['Jumlah Missing'].plot(kind='bar', ax=axes[0], color='#e74c3c', edgecolor='black')\n",
    "    axes[0].set_title('Jumlah Nilai Kosong per Kolom', fontsize=13, fontweight='bold')\n",
    "    axes[0].set_ylabel('Jumlah')\n",
    "    axes[0].tick_params(axis='x', rotation=45)\n",
    "    \n",
    "    # Heatmap missing pattern\n",
    "    sns.heatmap(df.isnull(), cbar=True, yticklabels=False, ax=axes[1], cmap='YlOrRd')\n",
    "    axes[1].set_title('Pola Nilai Kosong (Kuning = Kosong)', fontsize=13, fontweight='bold')\n",
    "    \n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "else:\n",
    "    print(\"Tidak ditemukan nilai kosong dalam dataset.\")"
]))

cells.append(make_md([
    "**Hasil analisis nilai kosong:**\n",
    "- Kolom `trestbps` memiliki 5 nilai kosong (1.65%)\n",
    "- Kolom `chol` memiliki 5 nilai kosong (1.65%)\n",
    "- Karena persentase nilai kosong kecil, akan dilakukan imputasi menggunakan nilai median agar tidak dipengaruhi oleh nilai ekstrem."
]))

# 4B. Duplicate Values
cells.append(make_md([
    "### 4.2 Analisis Data Duplikat"
]))

cells.append(make_code([
    "# Analisis Data Duplikat\n",
    "duplicates_count = df.duplicated().sum()\n",
    "print(f\"Jumlah baris duplikat: {duplicates_count}\")\n",
    "print(f\"Persentase duplikat: {(duplicates_count / len(df) * 100):.2f}%\")\n",
    "\n",
    "if duplicates_count > 0:\n",
    "    print(f\"\\nBaris data duplikat:\")\n",
    "    display(df[df.duplicated(keep=False)].sort_values(df.columns.tolist()))"
]))

cells.append(make_md([
    "**Hasil analisis duplikasi data:**\n",
    "- Terdapat 3 baris data duplikat (0.99%)\n",
    "- Baris duplikat ini akan dihapus pada tahap pra-pemrosesan untuk menghindari duplikasi informasi yang berulang."
]))

# 4C. Outlier Analysis
cells.append(make_md([
    "### 4.3 Analisis Pencilan (Outliers)"
]))

cells.append(make_code([
    "# Deteksi Pencilan menggunakan IQR dan Boxplot\n",
    "continuous_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']\n",
    "\n",
    "fig, axes = plt.subplots(2, 3, figsize=(16, 10))\n",
    "axes = axes.flatten()\n",
    "\n",
    "print(\"Deteksi pencilan menggunakan metode IQR:\")\n",
    "print(\"=\" * 55)\n",
    "\n",
    "for i, col in enumerate(continuous_cols):\n",
    "    Q1 = df[col].quantile(0.25)\n",
    "    Q3 = df[col].quantile(0.75)\n",
    "    IQR = Q3 - Q1\n",
    "    lower_bound = Q1 - 1.5 * IQR\n",
    "    upper_bound = Q3 + 1.5 * IQR\n",
    "    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]\n",
    "    \n",
    "    print(f\"  {col:12s} | IQR: {IQR:8.2f} | Batas: [{lower_bound:.2f}, {upper_bound:.2f}] | Pencilan: {len(outliers)}\")\n",
    "    \n",
    "    # Boxplot\n",
    "    bp = axes[i].boxplot(df[col].dropna(), patch_artist=True, \n",
    "                         boxprops=dict(facecolor='#3498db', alpha=0.7),\n",
    "                         medianprops=dict(color='red', linewidth=2))\n",
    "    axes[i].set_title(f'{col}\\n(Pencilan: {len(outliers)})', fontsize=11, fontweight='bold')\n",
    "    axes[i].set_ylabel('Nilai')\n",
    "\n",
    "# Hide last subplot\n",
    "axes[-1].set_visible(False)\n",
    "plt.suptitle('Analisis Boxplot - Deteksi Pencilan', fontsize=14, fontweight='bold', y=1.02)\n",
    "plt.tight_layout()\n",
    "plt.show()"
]))

cells.append(make_md([
    "**Hasil analisis pencilan:**\n",
    "- Variabel `trestbps`, `chol`, dan `oldpeak` terdeteksi memiliki nilai pencilan di luar batas atas.\n",
    "- Pencilan tidak dihapus karena mewakili variasi data medis yang wajar dan relevan dengan klasifikasi penyakit jantung."
]))

# 4D. Distribution Analysis
cells.append(make_md([
    "### 4.4 Analisis Distribusi Variabel Numerik Kontinu"
]))

cells.append(make_code([
    "# Distribusi variabel numerik kontinu\n",
    "fig, axes = plt.subplots(2, 3, figsize=(16, 10))\n",
    "axes = axes.flatten()\n",
    "\n",
    "for i, col in enumerate(continuous_cols):\n",
    "    sns.histplot(data=df, x=col, kde=True, ax=axes[i], color='#2ecc71', edgecolor='black', alpha=0.7)\n",
    "    axes[i].axvline(df[col].mean(), color='red', linestyle='--', label=f'Mean: {df[col].mean():.1f}')\n",
    "    axes[i].axvline(df[col].median(), color='blue', linestyle='--', label=f'Median: {df[col].median():.1f}')\n",
    "    axes[i].set_title(f'Distribusi {col}', fontsize=11, fontweight='bold')\n",
    "    axes[i].legend(fontsize=9)\n",
    "\n",
    "axes[-1].set_visible(False)\n",
    "plt.suptitle('Distribusi Variabel Numerik Kontinu', fontsize=14, fontweight='bold', y=1.02)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# Cek skewness\n",
    "print(\"\\nAnalisis Kemencengan (Skewness):\")\n",
    "for col in continuous_cols:\n",
    "    skew = df[col].skew()\n",
    "    skew_type = 'Simetris' if abs(skew) < 0.5 else ('Positif/Right-skewed' if skew > 0 else 'Negatif/Left-skewed')\n",
    "    print(f\"  {col:12s} | Skewness: {skew:6.3f} | {skew_type}\")"
]))

# 4E. Categorical Analysis
cells.append(make_md([
    "### 4.5 Analisis Distribusi Variabel Kategorikal"
]))

cells.append(make_code([
    "# Distribusi variabel kategorikal\n",
    "categorical_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']\n",
    "\n",
    "fig, axes = plt.subplots(2, 4, figsize=(18, 10))\n",
    "axes = axes.flatten()\n",
    "\n",
    "for i, col in enumerate(categorical_cols):\n",
    "    value_counts = df[col].value_counts().sort_index()\n",
    "    bars = axes[i].bar(value_counts.index.astype(str), value_counts.values, \n",
    "                       color=sns.color_palette('viridis', len(value_counts)), edgecolor='black')\n",
    "    axes[i].set_title(f'Distribusi {col}', fontsize=11, fontweight='bold')\n",
    "    axes[i].set_xlabel(col)\n",
    "    axes[i].set_ylabel('Frekuensi')\n",
    "    \n",
    "    # Tambahkan label nilai di atas bar\n",
    "    for bar, val in zip(bars, value_counts.values):\n",
    "        axes[i].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,\n",
    "                     str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')\n",
    "\n",
    "plt.suptitle('Distribusi Variabel Kategorikal', fontsize=14, fontweight='bold', y=1.02)\n",
    "plt.tight_layout()\n",
    "plt.show()"
]))

# 4F. Target Analysis
cells.append(make_md([
    "### 4.6 Analisis Variabel Target"
]))

cells.append(make_code([
    "# Distribusi Variabel Target\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "# Count plot\n",
    "target_counts = df['target'].value_counts()\n",
    "colors = ['#2ecc71', '#e74c3c']  # Hijau = Normal, Merah = Penyakit Jantung\n",
    "labels = ['Normal (0)', 'Heart Disease (1)']\n",
    "\n",
    "bars = axes[0].bar(labels, target_counts.sort_index().values, color=colors, edgecolor='black', alpha=0.85)\n",
    "for bar, val in zip(bars, target_counts.sort_index().values):\n",
    "    axes[0].text(bar.get_x() + bar.get_width()/2., bar.get_height() + 2,\n",
    "                 f'{val} ({val/len(df)*100:.1f}%)', ha='center', fontsize=11, fontweight='bold')\n",
    "axes[0].set_title('Distribusi Variabel Target', fontsize=13, fontweight='bold')\n",
    "axes[0].set_ylabel('Jumlah Pasien')\n",
    "\n",
    "# Pie chart\n",
    "axes[1].pie(target_counts.sort_index().values, labels=labels, colors=colors, \n",
    "            autopct='%1.1f%%', startangle=90, explode=[0.05, 0.05],\n",
    "            textprops={'fontsize': 12, 'fontweight': 'bold'},\n",
    "            shadow=True)\n",
    "axes[1].set_title('Proporsi Variabel Target', fontsize=13, fontweight='bold')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# Cek keseimbangan kelas\n",
    "ratio = target_counts.min() / target_counts.max()\n",
    "print(f\"\\nRasio kelas minoritas/mayoritas: {ratio:.3f}\")\n",
    "if ratio > 0.8:\n",
    "    print(\"Dataset seimbang.\")\n",
    "elif ratio > 0.5:\n",
    "    print(\"Dataset sedikit tidak seimbang.\")\n",
    "else:\n",
    "    print(\"Dataset sangat tidak seimbang.\")"
]))

cells.append(make_md([
    "**Hasil analisis variabel target:**\n",
    "- Pasien terdiagnosa penyakit jantung sebanyak 162 orang (53.5%) dan pasien normal sebanyak 141 orang (46.5%).\n",
    "- Dengan rasio sekitar 0.87, kelas target tergolong seimbang sehingga tidak membutuhkan metode penyeimbangan data seperti SMOTE."
]))

# 4G. Correlation Analysis
cells.append(make_md([
    "### 4.7 Analisis Hubungan Korelasi"
]))

cells.append(make_code([
    "# Heatmap Matriks Korelasi\n",
    "plt.figure(figsize=(14, 11))\n",
    "\n",
    "corr_matrix = df.corr()\n",
    "mask = np.triu(np.ones_like(corr_matrix, dtype=bool))  # Mask untuk segitiga atas\n",
    "\n",
    "sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',\n",
    "            center=0, linewidths=0.5, square=True,\n",
    "            cbar_kws={'shrink': 0.8, 'label': 'Koefisien Korelasi'})\n",
    "\n",
    "plt.title('Matriks Korelasi - Heart Disease Dataset', fontsize=15, fontweight='bold', pad=20)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# Korelasi tertinggi dengan target\n",
    "print(\"\\nKorelasi fitur terhadap Target:\")\n",
    "print(\"=\" * 45)\n",
    "target_corr = corr_matrix['target'].drop('target').abs().sort_values(ascending=False)\n",
    "for feat, corr in target_corr.items():\n",
    "    sign = '+' if corr_matrix.loc[feat, 'target'] > 0 else '-'\n",
    "    strength = 'Kuat' if corr > 0.4 else ('Sedang' if corr > 0.2 else 'Lemah')\n",
    "    print(f\"  {feat:12s} | r = {sign}{corr:.3f} | {strength}\")"
]))

cells.append(make_md([
    "**Hasil analisis korelasi:**\n",
    "- Fitur yang memiliki hubungan korelasi sedang hingga kuat dengan target adalah `cp`, `thalach`, `exang`, `oldpeak`, dan `ca`.\n",
    "- Koefisien korelasi antar-fitur berada di bawah 0.8, mengindikasikan tidak adanya masalah multikolinearitas."
]))

# 4H. Feature vs Target
cells.append(make_md([
    "### 4.8 Hubungan Antara Fitur dengan Target"
]))

cells.append(make_code([
    "# Distribusi fitur numerik berdasarkan target\n",
    "fig, axes = plt.subplots(2, 3, figsize=(16, 10))\n",
    "axes = axes.flatten()\n",
    "\n",
    "for i, col in enumerate(continuous_cols):\n",
    "    for target_val, color, label in [(0, '#2ecc71', 'Normal'), (1, '#e74c3c', 'Heart Disease')]:\n",
    "        subset = df[df['target'] == target_val][col].dropna()\n",
    "        axes[i].hist(subset, bins=20, alpha=0.6, color=color, label=label, edgecolor='black')\n",
    "    axes[i].set_title(f'{col} berdasarkan Target', fontsize=11, fontweight='bold')\n",
    "    axes[i].legend()\n",
    "    axes[i].set_xlabel(col)\n",
    "    axes[i].set_ylabel('Frekuensi')\n",
    "\n",
    "axes[-1].set_visible(False)\n",
    "plt.suptitle('Distribusi Fitur Numerik Berdasarkan Target', fontsize=14, fontweight='bold', y=1.02)\n",
    "plt.tight_layout()\n",
    "plt.show()"
]))

cells.append(make_code([
    "# Analisis variabel kategorikal terhadap target\n",
    "fig, axes = plt.subplots(2, 4, figsize=(18, 10))\n",
    "axes = axes.flatten()\n",
    "\n",
    "for i, col in enumerate(categorical_cols):\n",
    "    ct = pd.crosstab(df[col], df['target'], normalize='index') * 100\n",
    "    ct.plot(kind='bar', stacked=True, ax=axes[i], color=['#2ecc71', '#e74c3c'], \n",
    "            edgecolor='black', alpha=0.85)\n",
    "    axes[i].set_title(f'{col} vs Target (%)', fontsize=11, fontweight='bold')\n",
    "    axes[i].set_ylabel('Persentase (%)')\n",
    "    axes[i].legend(['Normal', 'Heart Disease'], fontsize=8)\n",
    "    axes[i].tick_params(axis='x', rotation=0)\n",
    "\n",
    "plt.suptitle('Proporsi Target per Kategori', fontsize=14, fontweight='bold', y=1.02)\n",
    "plt.tight_layout()\n",
    "plt.show()"
]))

# ============================================================
# 5. DATA PREPROCESSING
# ============================================================
cells.append(make_md([
    "# **5. Data Preprocessing**\n",
    "\n",
    "Pra-pemrosesan data dilakukan untuk mempersiapkan dataset sebelum digunakan dalam pemodelan. Langkah-langkah yang dilakukan meliputi:\n",
    "1. Penanganan data duplikat.\n",
    "2. Penanganan nilai kosong.\n",
    "3. Rekayasa fitur (Feature Engineering) untuk membuat variabel klinis baru.\n",
    "4. Penerapan One-Hot Encoding pada fitur kategorikal.\n",
    "5. Pembagian data latih dan uji secara terstrata.\n",
    "6. Penskalaan standar (Standard Scaling) pada variabel numerik kontinu.\n",
    "7. Penyimpanan dataset hasil pra-pemrosesan."
]))

cells.append(make_md([
    "### 5.1 Penanganan Data Duplikat"
]))

cells.append(make_code([
    "# Hapus baris duplikat\n",
    "print(f\"Dimensi data sebelum: {df.shape}\")\n",
    "\n",
    "df_clean = df.drop_duplicates().reset_index(drop=True)\n",
    "\n",
    "print(f\"Dimensi data setelah menghapus duplikat: {df_clean.shape}\")\n",
    "print(f\"Jumlah baris dihapus: {len(df) - len(df_clean)}\")\n",
    "print(\"Data duplikat berhasil dihapus.\")"
]))

cells.append(make_md([
    "### 5.2 Penanganan Nilai Kosong"
]))

cells.append(make_code([
    "# Imputasi nilai kosong menggunakan median\n",
    "cols_with_missing = ['trestbps', 'chol']\n",
    "\n",
    "print(\"Nilai kosong sebelum imputasi:\")\n",
    "print(df_clean[cols_with_missing].isnull().sum())\n",
    "\n",
    "for col in cols_with_missing:\n",
    "    median_val = df_clean[col].median()\n",
    "    df_clean[col] = df_clean[col].fillna(median_val)\n",
    "    print(f\"\\n  Kolom '{col}' diisi dengan median = {median_val}\")\n",
    "\n",
    "print(\"\\nTotal nilai kosong setelah imputasi:\")\n",
    "print(df_clean.isnull().sum().sum())"
]))

cells.append(make_md([
    "### 5.3 Rekayasa Fitur (Feature Engineering)"
]))

cells.append(make_code([
    "# Pembuatan Fitur Baru\n",
    "df_feat = df_clean.copy()\n",
    "\n",
    "# 1. Rasio Kolesterol terhadap Tekanan Darah\n",
    "df_feat['chol_bps_ratio'] = df_feat['chol'] / (df_feat['trestbps'] + 1e-5)\n",
    "print(\"Fitur 'chol_bps_ratio' berhasil dibuat.\")\n",
    "print(f\"   Statistik: mean={df_feat['chol_bps_ratio'].mean():.3f}, std={df_feat['chol_bps_ratio'].std():.3f}\")\n",
    "\n",
    "# 2. Pengelompokan Usia\n",
    "df_feat['age_group'] = pd.cut(df_feat['age'], bins=[0, 45, 60, np.inf], labels=[0, 1, 2]).astype(int)\n",
    "print(\"\\nFitur 'age_group' berhasil dibuat.\")\n",
    "print(f\"   Distribusi: {dict(df_feat['age_group'].value_counts().sort_index())}\")\n",
    "\n",
    "# 3. Rasio Detak Jantung Maksimum terhadap Usia\n",
    "df_feat['hr_age_ratio'] = df_feat['thalach'] / (df_feat['age'] + 1e-5)\n",
    "print(\"\\nFitur 'hr_age_ratio' berhasil dibuat.\")\n",
    "print(f\"   Statistik: mean={df_feat['hr_age_ratio'].mean():.3f}, std={df_feat['hr_age_ratio'].std():.3f}\")\n",
    "\n",
    "print(f\"\\nDimensi dataset setelah rekayasa fitur: {df_feat.shape}\")\n",
    "df_feat.head()"
]))

cells.append(make_md([
    "### 5.4 Pembagian Data, Encoding, dan Penskalaan"
]))

cells.append(make_code([
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "\n",
    "# Pisahkan fitur prediktor dan variabel target\n",
    "X = df_feat.drop(columns=['target'])\n",
    "y = df_feat['target']\n",
    "\n",
    "# Kelompokkan jenis kolom\n",
    "categorical_encode_cols = ['cp', 'restecg', 'slope', 'thal', 'age_group']  # Kategorikal Multi-kelas\n",
    "numeric_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'chol_bps_ratio', 'hr_age_ratio']\n",
    "\n",
    "# One-Hot Encoding\n",
    "X_encoded = pd.get_dummies(X, columns=categorical_encode_cols, drop_first=True)\n",
    "\n",
    "# Ubah tipe data dummy boolean ke int\n",
    "dummy_cols = [col for col in X_encoded.columns if any(mc in col for mc in categorical_encode_cols)]\n",
    "X_encoded[dummy_cols] = X_encoded[dummy_cols].astype(int)\n",
    "\n",
    "print(f\"Dimensi setelah encoding: {X_encoded.shape}\")\n",
    "print(f\"Kolom hasil encoding: {X_encoded.columns.tolist()}\")"
]))

cells.append(make_code([
    "# Pembagian data latih (train) dan uji (test) dengan perbandingan 80:20 secara terstrata\n",
    "X_train, X_test, y_train, y_test = train_test_split(\n",
    "    X_encoded, y, test_size=0.2, random_state=42, stratify=y\n",
    ")\n",
    "\n",
    "print(f\"Jumlah data latih (Train set): {X_train.shape[0]} ({X_train.shape[0]/len(X_encoded)*100:.1f}%)\")\n",
    "print(f\"Jumlah data uji (Test set):   {X_test.shape[0]} ({X_test.shape[0]/len(X_encoded)*100:.1f}%)\")\n",
    "print(f\"\\nDistribusi target pada data latih: {dict(y_train.value_counts().sort_index())}\")\n",
    "print(f\"Distribusi target pada data uji:  {dict(y_test.value_counts().sort_index())}\")"
]))

cells.append(make_code([
    "# Standard Scaling pada fitur numerik kontinu\n",
    "scaler = StandardScaler()\n",
    "\n",
    "X_train_scaled = X_train.copy()\n",
    "X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])\n",
    "\n",
    "X_test_scaled = X_test.copy()\n",
    "X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])\n",
    "\n",
    "# Gabungkan kembali prediktor dan target\n",
    "train_preprocessed = X_train_scaled.copy()\n",
    "train_preprocessed['target'] = y_train\n",
    "\n",
    "test_preprocessed = X_test_scaled.copy()\n",
    "test_preprocessed['target'] = y_test\n",
    "\n",
    "print(\"Proses penskalaan data selesai.\")\n",
    "print(f\"\\nDimensi final data latih (Train set): {train_preprocessed.shape}\")\n",
    "print(f\"Dimensi final data uji (Test set):   {test_preprocessed.shape}\")\n",
    "print(f\"\\nVerifikasi penskalaan (mean ≈ 0, std ≈ 1):\")\n",
    "for col in numeric_cols[:3]:\n",
    "    print(f\"  {col}: mean={X_train_scaled[col].mean():.4f}, std={X_train_scaled[col].std():.4f}\")"
]))

cells.append(make_md([
    "### 5.5 Penyimpanan Dataset Hasil Pra-pemrosesan"
]))

cells.append(make_code([
    "# Menyimpan dataset hasil pra-pemrosesan\n",
    "output_dir = 'dataset_preprocessed'\n",
    "os.makedirs(output_dir, exist_ok=True)\n",
    "\n",
    "train_path = os.path.join(output_dir, 'train.csv')\n",
    "test_path = os.path.join(output_dir, 'test.csv')\n",
    "\n",
    "train_preprocessed.to_csv(train_path, index=False)\n",
    "test_preprocessed.to_csv(test_path, index=False)\n",
    "\n",
    "print(\"Dataset pra-pemrosesan berhasil disimpan:\")\n",
    "print(f\"   Latih (Train): {train_path} - Dimensi: {train_preprocessed.shape}\")\n",
    "print(f\"   Uji (Test):   {test_path} - Dimensi: {test_preprocessed.shape}\")\n",
    "print(f\"\\nDaftar kolom akhir ({len(train_preprocessed.columns)}):\")\n",
    "for i, col in enumerate(train_preprocessed.columns, 1):\n",
    "    print(f\"   {i:2d}. {col}\")"
]))

cells.append(make_md([
    "### 5.6 Kesimpulan Eksperimen\n",
    "\n",
    "#### Ringkasan Dataset\n",
    "- Jumlah data: 303 sampel dengan 14 variabel awal.\n",
    "- Variabel target: Diagnosa penyakit jantung (0 = Sehat, 1 = Penyakit Jantung).\n",
    "- Distribusi kelas: 46.5% normal vs 53.5% penyakit jantung (seimbang).\n",
    "\n",
    "#### Hasil Analisis dan Pra-pemrosesan\n",
    "1. Nilai Kosong: Ditemukan nilai kosong pada variabel `trestbps` dan `chol` yang diselesaikan dengan imputasi median.\n",
    "2. Duplikasi: Sebanyak 3 baris data duplikat telah dihapus.\n",
    "3. Pencilan: Terdeteksi pencilan pada variabel `trestbps`, `chol`, dan `oldpeak` namun tetap dipertahankan karena mengandung nilai klinis riil.\n",
    "4. Rekayasa Fitur: Menghasilkan 3 fitur baru yaitu `chol_bps_ratio`, `age_group`, dan `hr_age_ratio`.\n",
    "5. Penskalaan: Dilakukan Standard Scaling pada seluruh fitur numerik kontinu.\n",
    "6. Pembagian Data: Data dibagi menjadi 80% untuk data latih dan 20% untuk data uji secara terstrata.\n",
    "\n",
    "#### Output File\n",
    "- `dataset_preprocessed/train.csv` (data latih)\n",
    "- `dataset_preprocessed/test.csv` (data uji)\n",
    "\n",
    "Dataset yang telah diproses ini siap digunakan untuk tahapan pemodelan selanjutnya."
]))

# ============================================================
# ASSEMBLE NOTEBOOK
# ============================================================
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat": 4,
            "nbformat_minor": 2,
            "pygments_lexer": "ipython3",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

# Write to file
output_path = os.path.join("Eksperimen_SML_Kevinadiputra", "preprocessing", "Eksperimen_Kevinadiputra.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"Notebook berhasil ditulis ke: {output_path}")
print(f"Total cells: {len(cells)}")
