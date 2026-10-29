# Proyek Analisis Data: E-Commerce Public Dataset

Proyek ini menganalisis data transaksi e-commerce dan menyajikan hasilnya dalam dashboard interaktif berbasis **Streamlit**.

## Pertanyaan Bisnis

1. Bagaimana tren bulanan jumlah pesanan dan nilai penjualan pada Januari 2017 sampai Agustus 2018, serta bulan apa yang memiliki nilai penjualan tertinggi dan terendah?
2. Berapa rata-rata durasi pengiriman dan persentase pesanan yang terlambat dibandingkan estimasi pada Januari sampai Agustus 2018?
3. Bagaimana distribusi pelanggan berdasarkan segmen RFM (Recency, Frequency, Monetary) selama keseluruhan periode transaksi?

## Struktur Folder

```
Submission_Proyek_Analisis_Data/
├── Dashboard/
│   ├── Dashboard_Analisis_Data.py   # kode dashboard Streamlit
│   └── main_data.csv                # data yang dipakai dashboard
├── data/                            # dataset mentah
├── notebook.ipynb                   # proses analisis data
├── README.md
├── requirements.txt
└── url.txt                          # tautan dashboard yang sudah di-deploy
```

## Prasyarat

- Python 3.9 atau lebih baru (proyek ini diuji dengan Python 3.13)
- pip

## Menjalankan Dashboard di Komputer Lokal

### 1. Salin repositori

```
git clone https://github.com/USERNAME/NAMA-REPO.git
cd NAMA-REPO
```

Atau unduh repositori sebagai ZIP dari GitHub, ekstrak, lalu buka foldernya di terminal.

### 2. (Opsional) Buat virtual environment

Windows:
```
py -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal dependensi

```
py -m pip install -r requirements.txt
```

Pada macOS / Linux, gunakan `python3 -m pip install -r requirements.txt`.

### 4. Jalankan dashboard

```
py -m streamlit run Dashboard/Dashboard_Analisis_Data.py
```

Pada macOS / Linux:
```
python3 -m streamlit run Dashboard/Dashboard_Analisis_Data.py
```

Dashboard akan terbuka otomatis di browser. Jika tidak, buka alamat yang tampil di terminal (biasanya `http://localhost:8501`).

Untuk menghentikan dashboard, tekan `Ctrl + C` di terminal.

> Jika path folder mengandung spasi, bungkus path dengan tanda kutip, misalnya:
> `py -m streamlit run "C:\My Project\NAMA-REPO\Dashboard\Dashboard_Analisis_Data.py"`

## Menggunakan Dashboard

- **Rentang tanggal pembelian** (sidebar): menyaring data transaksi berdasarkan periode.
- **Status pesanan** (sidebar): menyaring data berdasarkan status pesanan.
- **Ringkasan metrik**: total pesanan, total penjualan, rata-rata durasi pengiriman, dan persentase pesanan terlambat.
- **Tren bulanan**: grafik jumlah pesanan dan nilai penjualan per bulan.
- **Pengiriman**: persentase keterlambatan per bulan dan distribusi durasi pengiriman.
- **Segmentasi RFM**: distribusi pelanggan per segmen. Bagian ini dihitung dari seluruh periode transaksi sehingga tidak terpengaruh filter tanggal.

## Dashboard Online

Dashboard dapat diakses melalui tautan berikut:

https://NAMA-APLIKASI.streamlit.app

## Pemecahan Masalah

| Masalah | Solusi |
|---|---|
| `py` tidak dikenali | Pastikan Python terpasang dan opsi "Add Python to PATH" dicentang saat instalasi. |
| `ModuleNotFoundError` | Jalankan ulang `py -m pip install -r requirements.txt`. |
| `FileNotFoundError` untuk `main_data.csv` | Pastikan `main_data.csv` berada satu folder dengan `Dashboard_Analisis_Data.py`. |
| `File does not exist` saat `streamlit run` | Periksa path dan huruf besar/kecil pada nama file dan folder. |

## Package yang Digunakan

- streamlit
- pandas
- numpy
- matplotlib
- seaborn

## Dataset

[E-Commerce Public Dataset](https://drive.google.com/file/d/1MsAjPM7oKtVfJL_wRp1qmCajtSG1mdcK/view?usp=sharing)

## Penulis

Muhamad Zohir Arsyadilla Zafar Dangka
