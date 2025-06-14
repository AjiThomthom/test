import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ========================================
# KONFIGURASI TAMPILAN
# ========================================
st.set_page_config(layout="wide")

# Hilangkan menu default Streamlit
hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# ========================================
# FUNGSI UTAMA
# ========================================
def main():
    st.title("🚀 Aplikasi Model Industri (Menu Tombol)")
    
    # Inisialisasi session state untuk menyimpan halaman aktif
    if 'page' not in st.session_state:
        st.session_state.page = 'Optimasi Produksi'
    
    # ========================================
    # NAVIGASI BERBASIS TOMBOL
    # ========================================
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Optimasi Produksi", use_container_width=True):
            st.session_state.page = 'Optimasi Produksi'
    with col2:
        if st.button("📦 Model Persediaan", use_container_width=True):
            st.session_state.page = 'Model Persediaan'
    with col3:
        if st.button("🔄 Model Antrian", use_container_width=True):
            st.session_state.page = 'Model Antrian'
    with col4:
        if st.button("➕ Kasus Baru", use_container_width=True):
            st.session_state.page = 'Tambah Kasus'
    
    st.markdown("---")
    
    # ========================================
    # HALAMAN OPTIMASI PRODUKSI
    # ========================================
    if st.session_state.page == 'Optimasi Produksi':
        st.header("🔧 Optimasi Produksi (Linear Programming)")
        
        col1, col2 = st.columns(2)
        with col1:
            produk_a = st.text_input("Nama Produk A", "Sosis Bakar")
            profit_a = st.number_input("Keuntungan per Unit (Rp)", 500)
            time_a = st.number_input("Waktu Produksi (menit)", 2)
        
        with col2:
            produk_b = st.text_input("Nama Produk B", "Baso Bakar")
            profit_b = st.number_input("Keuntungan per Unit (Rp)", 1000)
            time_b = st.number_input("Waktu Produksi (menit)", 3)
        
        total_time = st.number_input("Total Waktu Tersedia (menit)", 240)
        
        if st.button("🚀 Hitung Solusi", key="hitung_optimasi"):
            y_max = total_time / time_b
            x_max = total_time / time_a
            
            if (profit_a * x_max) > (profit_b * y_max):
                solusi = f"{x_max:.1f} {produk_a}"
                profit = profit_a * x_max
            else:
                solusi = f"{y_max:.1f} {produk_b}"
                profit = profit_b * y_max
            
            st.success(f"**Produksi Optimal:** {solusi} | **Keuntungan:** Rp{profit:,.0f}")

    # ========================================
    # HALAMAN MODEL PERSEDIAAN
    # ========================================
    elif st.session_state.page == 'Model Persediaan':
        st.header("📦 Model Persediaan (EOQ)")
        
        D = st.number_input("Permintaan Tahunan (unit)", 10000)
        S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", 50000)
        H = st.number_input("Biaya Penyimpanan per Unit (Rp)", 2000)
        
        if st.button("📊 Hitung EOQ", key="hitung_eoq"):
            eoq = np.sqrt((2 * D * S) / H)
            st.info(f"**EOQ:** {eoq:.1f} unit")

    # ========================================
    # HALAMAN MODEL ANTRIAN
    # ========================================
    elif st.session_state.page == 'Model Antrian':
        st.header("🔄 Model Antrian (M/M/1)")
        
        col1, col2 = st.columns(2)
        with col1:
            λ = st.number_input("Tingkat Kedatangan (pelanggan/jam)", 10.0)
        with col2:
            μ = st.number_input("Tingkat Pelayanan (pelanggan/jam)", 12.0)
        
        if st.button("🧮 Hitung Antrian", key="hitung_antrian"):
            if λ >= μ:
                st.error("Sistem tidak stabil (λ harus < μ)")
            else:
                W = 1 / (μ - λ)
                st.info(f"**Waktu Tunggu Rata-rata:** {W:.2f} jam")

    # ========================================
    # HALAMAN TAMBAH KASUS BARU
    # ========================================
    elif st.session_state.page == 'Tambah Kasus':
        st.header("➕ Tambah Studi Kasus Baru")
        st.write("Fitur dalam pengembangan...")

if __name__ == "__main__":
    main()
