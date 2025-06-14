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
    ["🏠 Beranda", "📊 Optimasi Produksi", "📦 Model Persediaan (EOQ)", "🔄 Model Antrian", "➕ Tambah Data"],
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
        **📦 Model Persediaan (EOQ)**
        - Economic Order Quantity
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
            st.subheader("Barang A")
            p_a = st.number_input("Keuntungan/unit (Rp)", 5000, key="p_a")
            t_a = st.number_input("Waktu produksi (menit)", 30, key="t_a")
        with col2:
            st.subheader("Barang B")
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

# =============== HALAMAN MODEL PERSEDIAAN (EOQ) ===============
elif page == "📦 Model Persediaan (EOQ)":
    st.title("📦 MODEL PERSEDIAAN / INVENTORY MODEL (EOQ)")
    
    with st.expander("🔧 PARAMETER INVENTORY", expanded=True):
        D = st.number_input("Permintaan tahunan (unit)", 10000)
        S = st.number_input("Biaya pemesanan per pesanan (Rp)", 50000)
        H = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", 2000)
    
    if st.button("🧮 HITUNG EOQ", type="primary"):
        eoq = np.sqrt(2*D*S/H)
        total_orders = D / eoq
        holding_cost = (eoq/2)*H
        ordering_cost = (D/eoq)*S
        total_cost = holding_cost + ordering_cost
        
        st.markdown("---")
        st.header("📝 HASIL PERHITUNGAN EOQ")
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Rumus EOQ")
            st.latex(r"""
            EOQ = \sqrt{\frac{2DS}{H}}
            """)
            st.latex(fr"""
            = \sqrt{{\frac{{2 \times {D:,} \times {S:,}}}{{{H:,}}}}} 
            = {eoq:.1f} \text{{ unit}}
            """)
            
        with cols[1]:
            st.subheader("Biaya Total")
            st.latex(fr"""
            \begin{{aligned}}
            \text{{Biaya Penyimpanan}} &= \frac{{Q}}{{2}} \times H = \frac{{{eoq:.1f}}}{{2}} \times {H:,} = Rp{holding_cost:,.0f} \\
            \text{{Biaya Pemesanan}} &= \frac{{D}}{{Q}} \times S = \frac{{{D:,}}}{{{eoq:.1f}}} \times {S:,} = Rp{ordering_cost:,.0f} \\
            \text{{Total Biaya}} &= Rp{total_cost:,.0f}
            \end{{aligned}}
            """)
        
        st.success(f"""
        ## 🎯 INTERPRETASI
        **Sebaiknya memesan {eoq:.1f} unit setiap kali** agar total biaya pemesanan dan penyimpanan minimum (Rp{total_cost:,.0f}/tahun)
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
        if λ <= 0 or μ <= 0:
            st.error("Nilai λ dan μ harus positif")
        else:
            ρ = λ/μ  # Utilisasi
            W = 1/(μ-λ)  # Waktu dalam sistem (jam)
            Wq = W - (1/μ)  # Waktu tunggu dalam antrian (jam)
            L = λ*W  # Jumlah pelanggan dalam sistem
            Lq = λ*Wq  # Jumlah pelanggan dalam antrian
            
            st.markdown("---")
            st.header("📝 HASIL PERHITUNGAN")
            
            cols = st.columns(2)
            with cols[0]:
                st.subheader("Parameter Utama")
                st.latex(fr"""
                \begin{{aligned}}
                \rho &= \frac{{\lambda}}{{\mu}} = \frac{{{λ}}}{{{μ}}} = {ρ:.2f} \text{{ (Utilisasi)}} \\
                W &= \frac{{1}}{{\mu - \lambda}} = \frac{{1}}{{{μ} - {λ}}} = {W:.2f} \text{{ jam}} \\
                &= {W*60:.1f} \text{{ menit}} \\
                W_q &= W - \frac{{1}}{{\mu}} = {Wq:.2f} \text{{ jam}} \\
                &= {Wq*60:.1f} \text{{ menit}}
                \end{{aligned}}
                """)
            
            with cols[1]:
                st.subheader("Jumlah Pelanggan")
                st.latex(fr"""
                \begin{{aligned}}
                L &= \lambda W = {λ} \times {W:.2f} = {L:.2f} \\
                L_q &= \lambda W_q = {λ} \times {Wq:.2f} = {Lq:.2f}
                \end{{aligned}}
                """)
            
            # Interpretasi Utilisasi
            util_status = ""
            if ρ <= 0.25:
                util_status = "Tidak sibuk (Underutilized)"
            elif ρ <= 0.5:
                util_status = "Lumayan sibuk (Moderate)"
            elif ρ <= 0.8:
                util_status = "Sibuk (Busy)"
            elif ρ <= 1.0:
                util_status = "Sangat sibuk (Heavy Load)"
            else:
                util_status = "Overload (Tidak Stabil)"
            
            st.success(f"""
            ## 🎯 KESIMPULAN
            **Tingkat Utilisasi Sistem:** {ρ:.0%}  
            **Status:** {util_status}
            
            **Rekomendasi:**
            - Waktu tunggu rata-rata: {W*60:.1f} menit
            - Pelanggan dalam antrian: {Lq:.1f} orang
            """)

# =============== HALAMAN TAMBAH DATA ===============
elif page == "➕ Tambah Data":
    st.title("TAMBAH DATA BARU")
    st.warning("Fitur dalam pengembangan...")

# =============== FOOTER ===============
st.sidebar.markdown("---")
st.sidebar.info("""
**Versi 2.0.0**  
Dikembangkan oleh:  
*Tim Matematika Industri*  
© 2023
""")
