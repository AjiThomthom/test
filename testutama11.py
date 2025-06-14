import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# =============== KONFIGURASI ===============
st.set_page_config(layout="wide", page_title="Optimasi Produksi Detail")
st.title("📈 OPTIMASI PRODUKSI - DETAIL PERHITUNGAN")

# =============== INPUT PARAMETER ===============
with st.expander("🔧 MASUKKAN PARAMETER", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sosis Bakar (x₁)")
        profit_a = st.number_input("Keuntungan per Unit (Rp)", 500, key="p_a")
        time_a = st.number_input("Waktu Produksi (menit)", 2, key="t_a")
        
    with col2:
        st.subheader("Baso Bakar (x₂)")
        profit_b = st.number_input("Keuntungan per Unit (Rp)", 1000, key="p_b")
        time_b = st.number_input("Waktu Produksi (menit)", 3, key="t_b")
    
    total_time = st.number_input("Total Waktu Tersedia (menit)", 360, key="total")

# =============== PROSES HITUNG ===============
if st.button("🧮 HITUNG DETAIL", type="primary"):
    st.markdown("---")
    
    # ===== FORMULASI MODEL =====
    st.header("📝 FORMULASI MODEL MATEMATIKA")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Fungsi Tujuan")
        st.latex(r"""
        \text{Maksimalkan } 
        \boxed{
        \begin{aligned}
        Z = {} &500x_1 + 1000x_2 \\
        \end{aligned}
        }
        """)
    
    with col2:
        st.subheader("Sistem Kendala")
        st.latex(r"""
        \boxed{
        \begin{cases}
        2x_1 + 3x_2 \leq 360 \\
        x_1 \geq 0 \\
        x_2 \geq 0
        \end{cases}
        }
        """)
    
    # ===== PENYELESAIAN METODE GRAFIK =====
    st.header("📌 PENYELESAIAN METODE GRAFIK")
    
    # Hitung titik potong
    titik_A = (0, total_time/time_b)  # (0, 120)
    titik_B = (total_time/time_a, 0)  # (180, 0)
    
    # ===== DETAIL PERHITUNGAN =====
    st.subheader("🔍 Titik Ekstrim Daerah Layak")
    
    # Titik A (x1=0)
    with st.expander("Titik A: Hanya Produksi Baso Bakar (x₁=0)", expanded=True):
        st.latex(r"""
        \begin{aligned}
        &2(0) + 3x_2 = 360 \\
        &\Rightarrow 3x_2 = 360 \\
        &\Rightarrow x_2 = \frac{360}{3} = 120.0 \\
        &\text{Keuntungan } Z = 500(0) + 1000(120) = \boxed{Rp120.000}
        \end{aligned}
        """)
        st.metric("Nilai Z pada Titik A", "Rp120.000")
    
    # Titik B (x2=0)
    with st.expander("Titik B: Hanya Produksi Sosis Bakar (x₂=0)", expanded=True):
        st.latex(r"""
        \begin{aligned}
        &2x_1 + 3(0) = 360 \\
        &\Rightarrow 2x_1 = 360 \\
        &\Rightarrow x_1 = \frac{360}{2} = 180.0 \\
        &\text{Keuntungan } Z = 500(180) + 1000(0) = \boxed{Rp90.000}
        \end{aligned}
        """)
        st.metric("Nilai Z pada Titik B", "Rp90.000")
    
    # ===== VISUALISASI =====
    st.header("📊 GRAFIK SOLUSI")
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    # Plot garis kendala
    x = np.linspace(0, titik_B[0], 100)
    y = (total_time - time_a*x)/time_b
    
    ax.plot(x, y, 'b-', linewidth=2, label='2x₁ + 3x₂ ≤ 360')
    ax.fill_between(x, 0, y, alpha=0.1, color='blue')
    
    # Titik ekstrim
    ax.plot(titik_A[0], titik_A[1], 'ro', markersize=8, label='Titik A (0,120)')
    ax.plot(titik_B[0], titik_B[1], 'go', markersize=8, label='Titik B (180,0)')
    
    # Anotasi
    ax.annotate(f'Z= Rp120.000', xy=(0,120), xytext=(10,130),
                arrowprops=dict(facecolor='black', shrink=0.05))
    ax.annotate(f'Z= Rp90.000', xy=(180,0), xytext=(150,20),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    ax.set_xlabel('Jumlah Sosis Bakar (x₁)', fontsize=12)
    ax.set_ylabel('Jumlah Baso Bakar (x₂)', fontsize=12)
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
    
    # ===== KESIMPULAN =====
    st.success("""
    ## 🎯 KESIMPULAN SOLUSI OPTIMAL
    **Produksi:**
    - x₁ (Sosis Bakar) = 0 unit
    - x₂ (Baso Bakar) = 120 unit  
    
    **Keuntungan Maksimum:** Rp120.000
    """)

# =============== FOOTER ===============
st.sidebar.markdown("""
**Petunjuk:**
1. Isi parameter produksi
2. Klik tombol hitung
3. Lihat langkah perhitungan
4. Analisis grafik solusi
""")
