import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import sympy as sp

# ===== KONFIGURASI =====
st.set_page_config(layout="wide")
st.title("📈 Optimasi Produksi PT. Bakar-Bakar")

# ===== INPUT PARAMETER =====
st.header("🔧 Masukkan Parameter")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Produk A (Sosis Bakar)")
    profit_a = st.number_input("Keuntungan per Unit (Rp)", 500, key="profit_a")
    time_a = st.number_input("Waktu Produksi per Unit (menit)", 2, key="time_a")

with col2:
    st.subheader("Produk B (Baso Bakar)")
    profit_b = st.number_input("Keuntungan per Unit (Rp)", 1000, key="profit_b")
    time_b = st.number_input("Waktu Produksi per Unit (menit)", 3, key="time_b")

total_time = st.number_input("Total Waktu Tersedia (menit)", 240, key="total_time")

# ===== PROSES PERHITUNGAN =====
if st.button("🚀 Hitung Solusi Optimal"):
    st.header("📝 Langkah-langkah Penyelesaian")
    
    # Langkah 1: Definisikan Variabel
    st.subheader("Langkah 1: Definisikan Variabel")
    st.latex(r"""
    \begin{align*}
    x &= \text{Jumlah Sosis Bakar} \\
    y &= \text{Jumlah Baso Bakar}
    \end{align*}
    """)
    
    # Langkah 2: Fungsi Tujuan
    st.subheader("Langkah 2: Fungsi Tujuan (Maksimalkan Keuntungan)")
    st.latex(fr"""
    Z = {profit_a}x + {profit_b}y
    """)
    
    # Langkah 3: Kendala
    st.subheader("Langkah 3: Sistem Kendala")
    st.latex(fr"""
    \begin{{cases}}
    {time_a}x + {time_b}y \leq {total_time} \\
    x \geq 0 \\
    y \geq 0
    \end{{cases}}
    """)
    
    # Langkah 4: Mencari Titik Potong
    st.subheader("Langkah 4: Mencari Titik Ekstrim")
    st.write("**a. Titik ketika x = 0**")
    st.latex(fr"""
    {time_b}y = {total_time} \implies y = \frac{{{total_time}}}{{{time_b}}} = {total_time/time_b:.1f}
    """)
    
    st.write("**b. Titik ketika y = 0**")
    st.latex(fr"""
    {time_a}x = {total_time} \implies x = \frac{{{total_time}}}{{{time_a}}} = {total_time/time_a:.1f}
    """)
    
    # Langkah 5: Evaluasi Titik Ekstrim
    st.subheader("Langkah 5: Evaluasi Fungsi Tujuan")
    st.write("**a. Produksi Sosis Bakar saja**")
    st.latex(fr"""
    Z = {profit_a} \times {total_time/time_a:.1f} = Rp{profit_a * (total_time/time_a):,.0f}
    """)
    
    st.write("**b. Produksi Baso Bakar saja**")
    st.latex(fr"""
    Z = {profit_b} \times {total_time/time_b:.1f} = Rp{profit_b * (total_time/time_b):,.0f}
    """)
    
    # Simpulan
    optimal_y = total_time / time_b
    optimal_profit = profit_b * optimal_y
    
    st.success(fr"""
    **SOLUSI OPTIMAL:**  
    Produksi **0 unit Sosis Bakar** dan **{optimal_y:.1f} unit Baso Bakar**  
    **Keuntungan Maksimal:** Rp{optimal_profit:,.0f}
    """)
    
    # ===== VISUALISASI GRAFIK =====
    st.header("📊 Visualisasi Grafik")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot garis kendala
    x_values = np.linspace(0, total_time/time_a, 100)
    y_values = (total_time - time_a * x_values) / time_b
    
    ax.plot(x_values, y_values, label=f'{time_a}x + {time_b}y ≤ {total_time}', color='blue')
    ax.fill_between(x_values, 0, y_values, alpha=0.1, color='blue')
    
    # Titik ekstrim
    ax.scatter(0, optimal_y, color='red', s=100, label='Solusi Optimal')
    ax.scatter(total_time/time_a, 0, color='green', s=100, label='Titik Alternatif')
    
    # Formatting
    ax.set_xlabel('Jumlah Sosis Bakar (x)', fontsize=12)
    ax.set_ylabel('Jumlah Baso Bakar (y)', fontsize=12)
    ax.set_title('Daerah Solusi Layak', fontsize=14)
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
    
    # Ekspor Grafik
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    st.download_button(
        label="⬇️ Download Grafik",
        data=buf.getvalue(),
        file_name="optimasi_produksi.png",
        mime="image/png"
    )

# ===== INFORMASI TAMBAHAN =====
st.sidebar.markdown("""
**Pet
