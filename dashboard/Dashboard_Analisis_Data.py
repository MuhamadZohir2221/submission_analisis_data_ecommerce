import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")
sns.set_theme(style="whitegrid")

# Load dan siapkan data
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "main_data.csv")
    df = pd.read_csv(path)
 
    time_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
 
    # Kolom turunan
    df["order_month"] = (
        df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    )
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days
    df["is_late"] = (
        df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    )
    return df
 
 
all_data = load_data()
 
#Sidebar (filter)
st.sidebar.header("Filter")
 
min_date = all_data["order_purchase_timestamp"].min().date()
max_date = all_data["order_purchase_timestamp"].max().date()
 
## Default mengikuti periode di pertanyaan bisnis (Jan 2017 - Agu 2018)
default_start = max(min_date, pd.Timestamp("2017-01-01").date())
default_end = min(max_date, pd.Timestamp("2018-08-31").date())
 
date_range = st.sidebar.date_input(
    "Rentang tanggal pembelian",
    value=(default_start, default_end),
    min_value=min_date,
    max_value=max_date,
)
 
## date_input mengembalikan 1 nilai saat pengguna baru memilih tanggal awal
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = default_start, default_end
 
status_options = sorted(all_data["order_status"].dropna().unique())
selected_status = st.sidebar.multiselect(
    "Status pesanan", options=status_options, default=status_options
)
 
main_df = all_data[
    (all_data["order_purchase_timestamp"] >= pd.Timestamp(start_date))
    & (all_data["order_purchase_timestamp"] < pd.Timestamp(end_date) + pd.Timedelta(days=1))
    & (all_data["order_status"].isin(selected_status))
]
 
## Data khusus pengiriman: hanya pesanan yang sudah sampai ke pelanggan
delivered_df = main_df[
    (main_df["order_status"] == "delivered") & main_df["delivery_days"].notna()
]
 
st.title("Dashboard Analisis E-Commerce")
st.caption(f"Periode: {start_date} s.d. {end_date}")
 
if main_df.empty:
    st.warning("Tidak ada data pada filter yang dipilih.")
    st.stop()
 
 
#Ringkasan metrik
col1, col2, col3, col4 = st.columns(4)
 
col1.metric("Total Pesanan", f"{main_df['order_id'].nunique():,}")
col2.metric("Total Penjualan", f"{main_df['total_sales'].sum():,.0f}")
 
if not delivered_df.empty:
    col3.metric("Rata-rata Durasi Kirim", f"{delivered_df['delivery_days'].mean():.1f} hari")
    col4.metric("Pesanan Terlambat", f"{delivered_df['is_late'].mean() * 100:.1f}%")
else:
    col3.metric("Rata-rata Durasi Kirim", "-")
    col4.metric("Pesanan Terlambat", "-")
 

# Pertanyaan 1 - Tren bulanan
st.subheader("1. Tren Bulanan Pesanan dan Penjualan")
 
monthly_df = (
    main_df.groupby("order_month")
    .agg(total_orders=("order_id", "nunique"), total_sales=("total_sales", "sum"))
    .reset_index()
)
 
fig, ax = plt.subplots(1, 2, figsize=(16, 5))
 
ax[0].plot(monthly_df["order_month"], monthly_df["total_orders"], marker="o")
ax[0].set_title("Jumlah Pesanan per Bulan")
ax[0].set_xlabel("Bulan")
ax[0].set_ylabel("Jumlah pesanan")
 
ax[1].plot(monthly_df["order_month"], monthly_df["total_sales"], marker="o", color="tab:green")
ax[1].set_title("Nilai Penjualan per Bulan")
ax[1].set_xlabel("Bulan")
ax[1].set_ylabel("Total penjualan")
 
for a in ax:
    a.tick_params(axis="x", rotation=45)
plt.tight_layout()
st.pyplot(fig)
 
best = monthly_df.loc[monthly_df["total_sales"].idxmax()]
worst = monthly_df.loc[monthly_df["total_sales"].idxmin()]
c1, c2 = st.columns(2)
c1.metric(
    "Penjualan Tertinggi",
    f"{best['total_sales']:,.0f}",
    best["order_month"].strftime("%B %Y"),
    delta_color="off",
)
c2.metric(
    "Penjualan Terendah",
    f"{worst['total_sales']:,.0f}",
    worst["order_month"].strftime("%B %Y"),
    delta_color="off",
)
 
 
#Pertanyaan 2 - Pengiriman
st.subheader("2. Durasi Pengiriman dan Keterlambatan")
 
if delivered_df.empty:
    st.info("Tidak ada pesanan terkirim pada filter ini.")
else:
    late_monthly = (
        delivered_df.groupby("order_month")["is_late"].mean().mul(100).reset_index()
    )
    late_monthly["bulan"] = late_monthly["order_month"].dt.strftime("%Y-%m")
 
    fig, ax = plt.subplots(1, 2, figsize=(16, 5))
 
    sns.barplot(data=late_monthly, x="bulan", y="is_late", color="tab:red", ax=ax[0])
    ax[0].set_title("Persentase Pesanan Terlambat per Bulan")
    ax[0].set_xlabel("Bulan")
    ax[0].set_ylabel("Terlambat (%)")
    ax[0].tick_params(axis="x", rotation=45)
 
    sns.histplot(delivered_df["delivery_days"], bins=30, ax=ax[1])
    ax[1].set_title("Distribusi Durasi Pengiriman")
    ax[1].set_xlabel("Durasi (hari)")
    ax[1].set_ylabel("Jumlah pesanan")
 
    plt.tight_layout()
    st.pyplot(fig)
 
 
#Pertanyaan 3 - Segmentasi RFM
st.subheader("3. Segmentasi Pelanggan (RFM)")
st.caption("RFM dihitung dari seluruh periode transaksi, tidak terpengaruh filter tanggal.")
 
 
@st.cache_data
def compute_rfm(df):
    # Tanggal acuan ditentukan dari data: pembelian terakhir + 1 hari
    ref_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
 
    rfm = (
        df.groupby("customer_unique_id")
        .agg(
            last_purchase=("order_purchase_timestamp", "max"),
            frequency=("order_id", "nunique"),
            monetary=("total_sales", "sum"),
        )
        .reset_index()
    )
    rfm["recency"] = (ref_date - rfm["last_purchase"]).dt.days
 
    # Skor 1-4. rank(method="first") mencegah error akibat nilai kembar
    rfm["r_score"] = pd.qcut(
        rfm["recency"].rank(method="first"), 4, labels=[4, 3, 2, 1]
    ).astype(int)  # recency kecil = skor tinggi
    rfm["m_score"] = pd.qcut(
        rfm["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]
    ).astype(int)
    # Frequency didominasi nilai 1, jadi pakai ambang batas
    rfm["f_score"] = pd.cut(
        rfm["frequency"], bins=[0, 1, 2, np.inf], labels=[1, 2, 3]
    ).astype(int)
 
    conditions = [
        (rfm["f_score"] >= 2) & (rfm["r_score"] >= 3),
        (rfm["f_score"] >= 2),
        (rfm["r_score"] >= 3) & (rfm["m_score"] >= 3),
        (rfm["r_score"] >= 3),
        (rfm["m_score"] >= 3),
    ]
    labels = [
        "Champions",
        "Loyal",
        "Baru Bernilai Tinggi",
        "Pelanggan Baru",
        "Berisiko (Nilai Tinggi)",
    ]
    rfm["segment"] = np.select(conditions, labels, default="Pelanggan Tidur")
    return rfm
 
 
rfm_df = compute_rfm(all_data)
segment_counts = rfm_df["segment"].value_counts().reset_index()
segment_counts.columns = ["segment", "jumlah"]
 
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=segment_counts, x="jumlah", y="segment", ax=ax)
ax.set_title("Distribusi Pelanggan per Segmen RFM")
ax.set_xlabel("Jumlah pelanggan")
ax.set_ylabel("Segmen")
plt.tight_layout()
st.pyplot(fig)
 
with st.expander("Lihat ringkasan rata-rata per segmen"):
    summary = (
        rfm_df.groupby("segment")[["recency", "frequency", "monetary"]]
        .mean()
        .round(1)
        .reset_index()
    )
    st.dataframe(summary, use_container_width=True)
 
