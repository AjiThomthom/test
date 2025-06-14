import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("🔥 Optimasi Produksi PT. Bakar-Bakar")

# Input Parameter
st.header("📊 Masukkan Parameter")
col1, col2 = st.columns(2)
with col1:
    waktu_harian = st.number_input("Total Waktu Harian (menit)", value=240)
with col2:
    waktu_mingguan = st.number_input("Total Waktu Mingguan (menit)", value=1200)

# Hitung Solusi
if st.button("🎯 Hitung Solusi Optimal"):
    # Solusi Harian
    y_harian = waktu_harian / 3
    z_harian = 1000 * y_harian

    # Solusi Mingguan
    y_mingguan = waktu_mingguan / 3
    z_mingguan = 1000 * y_mingguan

    # Tampilkan Hasil
    st.success(f"""
    **🔹 Harian (4 Jam)**  
    - Produksi: **0 sosis bakar**, **{y_harian:.0f} baso bakar**  
    - Keuntungan Maksimal: **Rp{z_harian:,.0f}**  

    **🔹 Mingguan (20 Jam)**  
    - Produksi: **0 sosis bakar**, **{y_mingguan:.0f} baso bakar**  
    - Keuntungan Maksimal: **Rp{z_mingguan:,.0f}**  
    """)

    # Grafik Kendala Harian
    fig, ax = plt.subplots()
    x = np.linspace(0, waktu_harian/2, 100)
    y = (waktu_harian - 2*x) / 3
    ax.plot(x, y, label="Kendala Waktu Harian")
    ax.fill_between(x, 0, y, alpha=0.1)
    ax.scatter(0, y_harian, color="red", label="Solusi Optimal")
    ax.set_xlabel("Sosis Bakar (x)")
    ax.set_ylabel("Baso Bakar (y)")
    ax.legend()
    st.pyplot(fig)
