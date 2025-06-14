import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# =============== KONFIGURASI ===============
st.set_page_config(layout="wide", page_title="Aplikasi Model Industri")
st.sidebar.image("https://via.placeholder.com/150x50?text=MY-APP-LOGO", width=200)

# =============== NAVIGASI TOMBOL ===============
st.sidebar.title("NAVIGASI")
page = st.sidebar.radio("", 
    ["🏠 Beranda", "📊 Optimasi Produksi", "📦 Model Persediaan", "🔄 Model Antrian", "➕ Tambah Data"],
    label_visibility="collapsed")

# =============== HALAMAN BERANDA ===============
if page == "🏠 Beranda":
    st.title("Selamat Datang di Aplikasi Model Industri")
    st.image("https://via.placeholder.com/800x300?text=ANALISIS+INDUSTRI", use_column_width=True)
    
    cols = st.columns(3)
    with cols[0]:
        st.info("""
        **📊 Optimasi Produksi**
        - Linear Programming
        - Maksimalkan keuntungan
        """)
    with cols[1]:
        st.success("""
        **📦 Model Persediaan**
        - Perhitungan EOQ
        - Optimasi inventory
        """)
    with cols[2]:
        st.warning("""
        **🔄 Model Antrian**
        - Analisis M/M/1
        - Hitung waktu tunggu
        """)

# =============== HALAMAN OPTIMASI PRODUKSI ===============
elif page == "📊 Optimasi Produksi":
    st.title("📈 OPTIMASI PRODUKSI")
    
    # Input Parameter
    with st.expander("🔧 PARAMETER PRODUKSI", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Produk A")
            p_a = st.number_input("Keuntungan/unit (Rp)", 5000, key="p_a")
            t_a = st.number_input("Waktu produksi (menit)", 30, key="t_a")
        with col2:
            st.subheader("Produk B")
            p_b = st.number_input("Keuntungan/unit (Rp)", 8000, key="p_b")
            t_b = st.number_input("Waktu produksi (menit)", 45, key="t_b")
        
        total = st.number_input("Total waktu tersedia (menit)", 480, key="total")
    
    # Hitung Solusi
    if st.button("🧮 HITUNG SOLUSI", type="primary"):
        # Perhitungan
        titik_x = total / t_a
        titik_y = total / t_b
        optimal = max(p_a * titik_x, p_b * titik_y)
        
        # Visualisasi
        fig, ax = plt.subplots(figsize=(10,6))
        x = np.linspace(0, titik_x, 100)
        y = (total - t_a*x)/t_b
        ax.plot(x, y, 'b-', linewidth=2)
        ax.fill_between(x, 0, y, alpha=0.1)
        ax.scatter([0, titik_x], [titik_y, 0], color='red', s=100)
        
        # Tampilkan Hasil
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Hasil Perhitungan")
            st.latex(fr"\text{{Maksimum }} Z = {p_a}x + {p_b}y")
            st.latex(fr"{t_a}x + {t_b}y \leq {total}")
            st.success(f"Keuntungan Maksimal: Rp{optimal:,.0f}")
        
        with cols[1]:
            st.subheader("Visualisasi")
            st.pyplot(fig)
            
            # Download
            buf = BytesIO()
            plt.savefig(buf, format="png")
            st.download_button("💾 Download Grafik", buf.getvalue(), "optimasi.png")

# =============== HALAMAN MODEL PERSEDIAAN ===============
elif page == "📦 Model Persediaan":
    st.title("📦 MODEL PERSEDIAAN (EOQ)")
    
    with st.expander("🔧 PARAMETER INVENTORY", expanded=True):
        D = st.number_input("Permintaan tahunan (unit)", 10000)
        S = st.number_input("Biaya pemesanan (Rp)", 50000)
        H = st.number_input("Biaya penyimpanan (Rp/unit/tahun)", 2000)
    
    if st.button("🧮 HITUNG EOQ", type="primary"):
        eoq = np.sqrt(2*D*S/H)
        st.success(f"""
        **Hasil Perhitungan:**
        - EOQ: {eoq:.1f} unit
        - Frekuensi Pemesanan: {D/eoq:.1f} kali/tahun
        """)

# =============== HALAMAN MODEL ANTRIAN ===============
elif page == "🔄 Model Antrian":
    st.title("🔄 MODEL ANTRIAN (M/M/1)")
    
    with st.expander("🔧 PARAMETER PELAYANAN", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            λ = st.number_input("Tingkat kedatangan (pelanggan/jam)", 10.0)
        with col2:
            μ = st.number_input("Tingkat pelayanan (pelanggan/jam)", 12.0)
    
    if st.button("🧮 HITUNG PARAMETER", type="primary"):
        if λ >= μ:
            st.error("Sistem tidak stabil (λ harus < μ)")
        else:
            W = 1/(μ-λ)
            st.success(f"""
            **Hasil Perhitungan:**
            - Waktu tunggu rata-rata: {W:.2f} jam
            - Utilisasi sistem: {λ/μ:.0%}
            """)

# =============== HALAMAN TAMBAH DATA ===============
elif page == "➕ Tambah Data":
    st.title("TAMBAH DATA BARU")
    st.warning("Fitur dalam pengembangan...")

# =============== FOOTER ===============
st.sidebar.markdown("---")
st.sidebar.info("""
**Versi 1.0.0**  
Dikembangkan oleh:  
*Tim Matematika Industri*  
© 2023
""")
