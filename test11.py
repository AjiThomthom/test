import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# ===== KONFIGURASI =====
st.set_page_config(layout="wide", page_title="Optimasi Produksi PT. Bakar-Bakar")
st.title("📊 OPTIMASI PRODUKSI PT. BAKAR-BAKAR")

# ===== INPUT DATA =====
with st.expander("🔧 MASUKKAN PARAMETER PRODUKSI", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Sosis Bakar (Produk A)")
        profit_a = st.number_input("Keuntungan per Unit (Rp)", 500, key="p_a")
        time_a = st.number_input("Waktu Produksi (menit)", 2, key="t_a")
        
    with col2:
        st.subheader("Baso Bakar (Produk B)")
        profit_b = st.number_input("Keuntungan per Unit (Rp)", 1000, key="p_b")
        time_b = st.number_input("Waktu Produksi (menit)", 3, key="t_b")
    
    with col3:
        st.subheader("Kapasitas Produksi")
        total_time = st.number_input("Total Waktu Tersedia (menit)", 240, key="t_total")
        st.markdown("*(4 jam = 240 menit)*")

# ===== PROSES HITUNG =====
if st.button("🧮 HITUNG SOLUSI OPTIMAL", type="primary"):
    st.markdown("---")
    
    # ===== LANGKAH 1: FORMULASI MATEMATIS =====
    st.header("📝 FORMULASI MODEL MATEMATIKA")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Fungsi Tujuan")
            st.latex(fr"""
            \text{{Maksimalkan }} Z = {profit_a}x_1 + {profit_b}x_2
            """)
            st.markdown("""
            Dimana:
            - $x_1$ = Jumlah Sosis Bakar
            - $x_2$ = Jumlah Baso Bakar
            """)
        
        with col2:
            st.subheader("Sistem Kendala")
            st.latex(fr"""
            \begin{{cases}}
            {time_a}x_1 + {time_b}x_2 \leq {total_time} \\
            x_1 \geq 0 \\
            x_2 \geq 0
            \end{{cases}}
            """)
    
    # ===== LANGKAH 2: SOLUSI GRAFIK =====
    st.header("📌 PENYELESAIAN METODE GRAFIK")
    
    # Hitungan Titik Potong
    titik_x = total_time / time_a  # Jika hanya produksi x1
    titik_y = total_time / time_b  # Jika hanya produksi x2
    
    with st.expander("🔍 LIHAT DETAIL PERHITUNGAN", expanded=True):
        st.subheader("Titik Ekstrim Daerah Layak")
        col1, col2 = st.columns(2)
        with col1:
            st.latex(fr"""
            \text{{Jika }} x_2 = 0:
            {time_a}x_1 = {total_time} \\
            \Rightarrow x_1 = \frac{{{total_time}}}{{{time_a}}} = {titik_x:.1f}
            """)
            st.metric("Z pada titik ini", f"Rp{profit_a * titik_x:,.0f}")
            
        with col2:
            st.latex(fr"""
            \text{{Jika }} x_1 = 0:
            {time_b}x_2 = {total_time} \\
            \Rightarrow x_2 = \frac{{{total_time}}}{{{time_b}}} = {titik_y:.1f}
            """)
            st.metric("Z pada titik ini", f"Rp{profit_b * titik_y:,.0f}", delta="SOLUSI OPTIMAL")
    
    # ===== VISUALISASI GRAFIK =====
    st.header("📊 GRAFIK DAERAH SOLUSI LAYAK")
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    # Plot garis kendala
    x = np.linspace(0, titik_x*1.1, 500)
    y = (total_time - time_a * x) / time_b
    
    ax.plot(x, y, label=f'{time_a}$x_1$ + {time_b}$x_2$ ≤ {total_time}', linewidth=2, color='navy')
    ax.fill_between(x, 0, y, alpha=0.1, color='blue')
    
    # Titik-titik penting
    ax.scatter(0, 0, color='green', s=100, label='Titik (0,0)')
    ax.scatter(titik_x, 0, color='red', s=100, label=f'Titik ({titik_x:.1f}, 0)')
    ax.scatter(0, titik_y, color='purple', s=100, label=f'Titik (0, {titik_y:.1f})')
    
    # Formatting
    ax.set_xlim(0, titik_x*1.1)
    ax.set_ylim(0, titik_y*1.1)
    ax.set_xlabel('Jumlah Sosis Bakar ($x_1$)', fontsize=12)
    ax.set_ylabel('Jumlah Baso Bakar ($x_2$)', fontsize=12)
    ax.set_title('Daerah Solusi Layak', pad=20, fontsize=14)
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Simpan ke buffer untuk download
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    
    # Tampilkan di Streamlit
    st.pyplot(fig)
    
    # ===== HASIL AKHIR =====
    st.success(fr"""
    ## 🎯 SOLUSI OPTIMAL
    **Produksi:**
    - $x_1$ (Sosis Bakar) = 0 unit
    - $x_2$ (Baso Bakar) = {titik_y:.1f} unit
    
    **Keuntungan Maksimum:** Rp{profit_b * titik_y:,.0f}
    """)
    
    # Tombol Download
    st.download_button(
        label="⬇️ Download Grafik Solusi",
        data=buf.getvalue(),
        file_name="solusi_optimasi.png",
        mime="image/png",
        use_container_width=True
    )

# ===== DOKUMENTASI =====
with st.sidebar.expander("📚 PETUNJUK PENGGUNAAN"):
    st.markdown("""
    1. Masukkan parameter produksi
    2. Klik tombol **Hitung Solusi Optimal**
    3. Analisis hasil perhitungan:
       - Formulasi matematis
       - Titik-titik ekstrim
       - Grafik solusi
    4. Download grafik jika diperlukan
    """)

st.sidebar.markdown("""
**Dikembangkan oleh:**  
Tim Matematika Industri  
*Universitas Pelita Bangsa*
""")
