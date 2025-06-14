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

# =============== HALAMAN OPTIMASI PRODUKSI (DETAIL) ===============
elif page == "📊 Optimasi Produksi":
    st.title("📈 OPTIMASI PRODUKSI - DETAIL PERHITUNGAN")
    
    # Input Parameter
    with st.expander("🔧 PARAMETER PRODUKSI", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Pruduk A (x₁)")
            p_a = st.number_input("Keuntungan/unit (Rp)", 500, key="p_a")
            t_a = st.number_input("Waktu produksi (menit)", 2, key="t_a")
        with col2:
            st.subheader("Produk B (x₂)")
            p_b = st.number_input("Keuntungan/unit (Rp)", 1000, key="p_b")
            t_b = st.number_input("Waktu produksi (menit)", 3, key="t_b")
        
        total = st.number_input("Total waktu tersedia (menit)", 360, key="total")
    
    # Hitung Solusi
    if st.button("🧮 HITUNG SOLUSI DETAIL", type="primary"):
        st.markdown("---")
        
        # ===== FORMULASI MODEL =====
        st.header("📝 FORMULASI MODEL MATEMATIKA")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Fungsi Tujuan")
            st.latex(fr"""
            \text{{Maksimalkan }}
            \boxed{{
            Z = {p_a}x_1 + {p_b}x_2
            }}
            """)
        
        with col2:
            st.subheader("Sistem Kendala")
            st.latex(fr"""
            \boxed{{
            \begin{{cases}}
            {t_a}x_1 + {t_b}x_2 \leq {total} \\
            x_1 \geq 0 \\
            x_2 \geq 0
            \end{{cases}}
            }}
            """)
        
        # ===== PENYELESAIAN METODE GRAFIK =====
        st.header("📌 PENYELESAIAN METODE GRAFIK")
        
        # Hitung titik ekstrim
        titik_A = (0, total/t_b)  # (0, 120)
        titik_B = (total/t_a, 0)  # (180, 0)
        
        # ===== DETAIL PERHITUNGAN =====
        st.subheader("🔍 Titik Ekstrim Daerah Layak")
        
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Titik A: Hanya Produksi Produk B (x₁=0)**")
            st.latex(fr"""
            \begin{{aligned}}
            &{t_a}(0) + {t_b}x_2 = {total} \\
            &\Rightarrow x_2 = \frac{{{total}}}{{{t_b}}} = {titik_A[1]:.1f} \\
            &Z = {p_a}(0) + {p_b}({titik_A[1]:.1f}) = \boxed{{Rp{p_b*titik_A[1]:,.0f}}}
            \end{{aligned}}
            """)
            st.metric("Nilai Z pada Titik A", f"Rp{p_b*titik_A[1]:,.0f}")
        
        with cols[1]:
            st.markdown("**Titik B: Hanya Produksi Pruduk A (x₂=0)**")
            st.latex(fr"""
            \begin{{aligned}}
            &{t_a}x_1 + {t_b}(0) = {total} \\
            &\Rightarrow x_1 = \frac{{{total}}}{{{t_a}}} = {titik_B[0]:.1f} \\
            &Z = {p_a}({titik_B[0]:.1f}) + {p_b}(0) = \boxed{{Rp{p_a*titik_B[0]:,.0f}}}
            \end{{aligned}}
            """)
            st.metric("Nilai Z pada Titik B", f"Rp{p_a*titik_B[0]:,.0f}")
        
        # ===== VISUALISASI =====
        st.header("📊 GRAFIK SOLUSI")
        
        fig, ax = plt.subplots(figsize=(10,6))
        
        # Plot garis kendala
        x = np.linspace(0, titik_B[0], 100)
        y = (total - t_a*x)/t_b
        
        ax.plot(x, y, 'b-', linewidth=2, label=f'{t_a}x₁ + {t_b}x₂ ≤ {total}')
        ax.fill_between(x, 0, y, alpha=0.1)
        
        # Titik ekstrim
        ax.plot(titik_A[0], titik_A[1], 'ro', markersize=8, label=f'Titik A (0,{titik_A[1]:.0f})')
        ax.plot(titik_B[0], titik_B[1], 'go', markersize=8, label=f'Titik B ({titik_B[0]:.0f},0)')
        
        # Anotasi
        ax.annotate(f'Z= Rp{p_b*titik_A[1]:,.0f}', xy=(0,titik_A[1]), xytext=(10,titik_A[1]+10),
                    arrowprops=dict(facecolor='black', shrink=0.05))
        ax.annotate(f'Z= Rp{p_a*titik_B[0]:,.0f}', xy=(titik_B[0],0), xytext=(titik_B[0]-40,20),
                    arrowprops=dict(facecolor='black', shrink=0.05))
        
        ax.set_xlabel('Jumlah Pruduk A (x₁)', fontsize=12)
        ax.set_ylabel('Jumlah Produk B (x₂)', fontsize=12)
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
        
        # ===== KESIMPULAN =====
        optimal_value = max(p_a*titik_B[0], p_b*titik_A[1])
        st.success(f"""
        ## 🎯 KESIMPULAN SOLUSI OPTIMAL
        **Produksi:**
        - x₁ (Pruduk A) = {0 if optimal_value == p_b*titik_A[1] else titik_B[0]:.0f} unit
        - x₂ (Produk B) = {titik_A[1] if optimal_value == p_b*titik_A[1] else 0:.0f} unit  
        
        **Keuntungan Maksimum:** Rp{optimal_value:,.0f}
        """)
        
        # Download
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        st.download_button("💾 Download Grafik Solusi", buf.getvalue(), "solusi_optimasi.png")

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
