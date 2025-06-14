import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from streamlit_extras.switch_page_button import switch_page

# =============== KONFIGURASI ===============
st.set_page_config(layout="wide", page_title="Aplikasi Model Industri")
st.sidebar.image("https://via.placeholder.com/150x50?text=MY-APP-LOGO", width=200)

# =============== DEFINISI PENJELASAN ===============
def show_explanation(topic):
    explanations = {
        "📊 Optimasi Produksi": {
            "definisi": """
            **Optimasi Produksi** adalah proses menemukan solusi terbaik untuk mengalokasikan sumber daya produksi 
            yang terbatas guna memaksimalkan keuntungan atau meminimalkan biaya.
            
            **Metode**: 
            - Linear Programming (Pemrograman Linear)
            - Analisis Sensitivitas
            - Solusi Grafis untuk kasus 2 variabel
            """,
            "contoh": """
            **Contoh Soal:**
            Sebuah pabrik memproduksi 2 jenis produk:
            - Produk A: Keuntungan Rp500/unit, waktu produksi 2 menit/unit
            - Produk B: Keuntungan Rp1000/unit, waktu produksi 3 menit/unit
            
            Total waktu produksi tersedia: 360 menit (6 jam)
            
            **Pertanyaan:**
            Berapa masing-masing produk harus diproduksi untuk memaksimalkan keuntungan?
            """
        },
        "📦 Model Persediaan (EOQ)": {
            "definisi": """
            **Model Persediaan EOQ (Economic Order Quantity)** adalah model untuk menentukan jumlah pesanan 
            optimal yang meminimalkan total biaya persediaan.
            
            **Komponen Biaya:**
            - Biaya pemesanan (ordering cost)
            - Biaya penyimpanan (holding cost)
            - Biaya kekurangan persediaan (shortage cost)
            """,
            "contoh": """
            **Contoh Soal:**
            Sebuah toko memiliki:
            - Permintaan tahunan: 10,000 unit
            - Biaya pemesanan: Rp50,000 per pesanan
            - Biaya penyimpanan: Rp2,000 per unit per tahun
            
            **Pertanyaan:**
            Berapa jumlah pesanan optimal (EOQ) yang harus dilakukan?
            """
        },
        "🔄 Model Antrian": {
            "definisi": """
            **Model Antrian M/M/1** adalah model antrian paling dasar dengan:
            - Kedatangan Poisson (Markovian)
            - Waktu pelayanan Eksponensial
            - 1 server/channel pelayanan
            
            **Parameter Utama:**
            - λ (lambda): Tingkat kedatangan pelanggan
            - μ (mu): Tingkat pelayanan
            - ρ (rho): Utilisasi sistem (λ/μ)
            """,
            "contoh": """
            **Contoh Soal:**
            Sebuah bank memiliki:
            - Tingkat kedatangan nasabah: 10 orang/jam
            - Tingkat pelayanan teller: 12 orang/jam
            
            **Pertanyaan:**
            Berapa waktu tunggu rata-rata nasabah dalam sistem?
            """
        }
    }
    
    with st.expander(f"ℹ️ Penjelasan {topic}", expanded=True):
        st.markdown("#### 📚 Definisi")
        st.markdown(explanations[topic]["definisi"])
        
        st.markdown("#### 📝 Contoh Soal")
        st.markdown(explanations[topic]["contoh"])
        
        if st.button(f"Lihat Aplikasi {topic.split()[0]}"):
            switch_page(topic[2:])  # Hapus emoji untuk navigasi

# =============== NAVIGASI TOMBOL ===============
st.sidebar.title("NAVIGASI")
page = st.sidebar.radio("", 
    ["🏠 Beranda", "📊 Optimasi Produksi", "📦 Model Persediaan (EOQ)", "🔄 Model Antrian", "➕ Tambah Data"],
    label_visibility="collapsed")

# Tampilkan penjelasan untuk halaman yang dipilih (kecuali Beranda dan Tambah Data)
if page not in ["🏠 Beranda", "➕ Tambah Data"]:
    show_explanation(page)

# =============== HALAMAN BERANDA ===============
if page == "🏠 Beranda":
    st.title("Selamat Datang di Aplikasi Model Industri")
    st.image("https://via.placeholder.com/800x300?text=ANALISIS+INDUSTRI", use_container_width=True)  # Diubah dari use_column_width
    
    cols = st.columns(3)
    with cols[0]:
        if st.button("📊 Optimasi Produksi", use_container_width=True):
            switch_page("Optimasi Produksi")
        st.info("""
        **Linear Programming**
        - Maksimalkan keuntungan
        - Alokasi sumber daya
        """)
    with cols[1]:
        if st.button("📦 Model Persediaan", use_container_width=True):
            switch_page("Model Persediaan (EOQ)")
        st.success("""
        **Economic Order Quantity**
        - Optimasi inventory
        - Minimalisasi biaya
        """)
    with cols[2]:
        if st.button("🔄 Model Antrian", use_container_width=True):
            switch_page("Model Antrian")
        st.warning("""
        **Analisis M/M/1**
        - Hitung waktu tunggu
        - Evaluasi kinerja sistem
        """)

# =============== HALAMAN OPTIMASI PRODUKSI ===============
elif page == "📊 Optimasi Produksi":
    st.title("📈 OPTIMASI PRODUKSI - BARANG A & B")
    
    # Input Parameter
    with st.expander("🔧 PARAMETER PRODUKSI", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Barang A")
            p_a = st.number_input("Keuntungan/unit (Rp)", 500, key="p_a")
            t_a = st.number_input("Waktu produksi (menit)", 2, key="t_a")
        with col2:
            st.subheader("Barang B")
            p_b = st.number_input("Keuntungan/unit (Rp)", 1000, key="p_b")
            t_b = st.number_input("Waktu produksi (menit)", 3, key="t_b")
        
        total = st.number_input("Total waktu tersedia (menit)", 360, key="total")
    
    # Hitung Solusi
    if st.button("🧮 HITUNG SOLUSI DETAIL", type="primary", use_container_width=True):  # Diubah parameter
        st.markdown("---")
        
        # FORMULASI MODEL
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
        
        # PENYELESAIAN METODE GRAFIK
        st.header("📌 PENYELESAIAN METODE GRAFIK")
        
        # Hitung titik ekstrim
        titik_A = (0, total/t_b)
        titik_B = (total/t_a, 0)
        
        # DETAIL PERHITUNGAN
        st.subheader("🔍 Titik Ekstrim Daerah Layak")
        
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Titik A: Hanya Produksi Barang B (x₁=0)**")
            st.latex(fr"""
            \begin{{aligned}}
            &{t_a}(0) + {t_b}x_2 = {total} \\
            &\Rightarrow x_2 = \frac{{{total}}}{{{t_b}}} = {titik_A[1]:.1f} \\
            &Z = {p_a}(0) + {p_b}({titik_A[1]:.1f}) = \boxed{{Rp{p_b*titik_A[1]:,.0f}}}
            \end{{aligned}}
            """)
            st.metric("Nilai Z pada Titik A", f"Rp{p_b*titik_A[1]:,.0f}")
        
        with cols[1]:
            st.markdown("**Titik B: Hanya Produksi Barang A (x₂=0)**")
            st.latex(fr"""
            \begin{{aligned}}
            &{t_a}x_1 + {t_b}(0) = {total} \\
            &\Rightarrow x_1 = \frac{{{total}}}{{{t_a}}} = {titik_B[0]:.1f} \\
            &Z = {p_a}({titik_B[0]:.1f}) + {p_b}(0) = \boxed{{Rp{p_a*titik_B[0]:,.0f}}}
            \end{{aligned}}
            """)
            st.metric("Nilai Z pada Titik B", f"Rp{p_a*titik_B[0]:,.0f}")
        
        # VISUALISASI
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
        
        ax.set_xlabel('Jumlah Barang A (x₁)', fontsize=12)
        ax.set_ylabel('Jumlah Barang B (x₂)', fontsize=12)
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
        
        # KESIMPULAN PRODUKSI
        optimal_value = max(p_a*titik_B[0], p_b*titik_A[1])
        if optimal_value == p_b*titik_A[1]:
            solusi = f"""
            - Produksi **Barang A** = 0 unit
            - Produksi **Barang B** = {titik_A[1]:.0f} unit
            """
        else:
            solusi = f"""
            - Produksi **Barang A** = {titik_B[0]:.0f} unit
            - Produksi **Barang B** = 0 unit
            """
        
        st.success(f"""
        ## 🎯 KESIMPULAN PRODUKSI OPTIMAL
        **Kombinasi Produksi:**
        {solusi}
        
        **Pendapatan Maksimum:** Rp{optimal_value:,.0f}
        
        **Strategi:**
        Fokuskan produksi pada {'Barang B' if optimal_value == p_b*titik_A[1] else 'Barang A'} 
        untuk memaksimalkan keuntungan dengan kendala waktu produksi.
        """)
        
        # Download
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        st.download_button("💾 Download Grafik Solusi", buf.getvalue(), "solusi_optimasi.png")

# =============== HALAMAN MODEL PERSEDIAAN (EOQ) ===============
elif page == "📦 Model Persediaan (EOQ)":
    st.title("📦 MODEL PERSEDIAAN / INVENTORY MODEL (EOQ)")
    
    with st.expander("🔧 PARAMETER INVENTORY", expanded=True):
        D = st.number_input("Permintaan tahunan (unit)", 10000)
        S = st.number_input("Biaya pemesanan per pesanan (Rp)", 50000)
        H = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", 2000)
    
    if st.button("🧮 HITUNG EOQ", type="primary", use_container_width=True):
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
            λ = st.number_input("Tingkat kedatangan (pelanggan/jam)", min_value=0.1, value=10.0, step=0.1)  # Diubah validasi
        with col2:
            μ = st.number_input("Tingkat pelayanan (pelanggan/jam)", min_value=0.1, value=12.0, step=0.1)  # Diubah validasi
    
    if st.button("🧮 HITUNG PARAMETER", type="primary", use_container_width=True):
        if μ <= λ:
            st.error("Tingkat pelayanan (μ) harus lebih besar dari tingkat kedatangan (λ) untuk sistem stabil")
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
**Versi 2.1.0**  
Dikembangkan oleh:  
*Tim Matematika Industri*  
© 2023
""")
