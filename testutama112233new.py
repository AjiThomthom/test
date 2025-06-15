import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64

# =============== GENERATE LOGO & HEADER ===============
def create_logo():
    img = Image.new('RGBA', (150, 50), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Desain logo industri
    draw.rectangle([10, 10, 40, 40], fill=(0, 100, 200))  # Kotak biru
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    draw.text((50, 15), "INDUSTRI", fill=(0,0,0), font=font)
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def create_header():
    img = Image.new('RGB', (800, 300), (70, 130, 180))  # Warna biru steel
    draw = ImageDraw.Draw(img)
    
    # Desain header
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    draw.text((50, 100), "APLIKASI MODEL INDUSTRI", fill=(255,255,255), font=font)
    draw.line([(50,150), (750,150)], fill=(255,255,0), width=3)
    
    # Tambahkan ikon grafis
    for i in range(5):
        draw.ellipse([100+i*150, 200, 140+i*150, 240], outline=(255,255,255), width=2)
    
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Encode gambar ke base64
LOGO_BASE64 = create_logo()
HEADER_BASE64 = create_header()

# =============== KONFIGURASI APLIKASI ===============
st.set_page_config(layout="wide", page_title="Aplikasi Model Industri")

# Inisialisasi session state untuk navigasi
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

# Fungsi untuk ganti halaman
def change_page(page_name):
    st.session_state.current_page = page_name

# =============== NAVIGASI SIDEBAR ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", width=200)
    st.title("NAVIGASI")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🏠 Beranda", on_click=change_page, args=("Beranda",), use_container_width=True)
        st.button("📊 Optimasi", on_click=change_page, args=("Optimasi",), use_container_width=True)
    with col2:
        st.button("📦 EOQ", on_click=change_page, args=("EOQ",), use_container_width=True)
        st.button("🔄 Antrian", on_click=change_page, args=("Antrian",), use_container_width=True)
    
    st.markdown("---")
    st.info("""
    **Versi 2.1.0**  
    Dikembangkan oleh:  
    *Tim Matematika Industri*  
    © 2023
    """)

# =============== HALAMAN BERANDA ===============
if st.session_state.current_page == "Beranda":
    st.title("Selamat Datang di Aplikasi Model Industri")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    
    cols = st.columns(3)
    with cols[0]:
        st.info("""
        **📊 Optimasi Produksi**
        - Linear Programming
        - Maksimalkan keuntungan
        """)
        if st.button("Lihat Optimasi", key="opt_btn"):
            change_page("Optimasi")
    with cols[1]:
        st.success("""
        **📦 Model Persediaan (EOQ)**
        - Economic Order Quantity
        - Optimasi inventory
        """)
        if st.button("Lihat EOQ", key="eoq_btn"):
            change_page("EOQ")
    with cols[2]:
        st.warning("""
        **🔄 Model Antrian**
        - Analisis M/M/1
        - Hitung waktu tunggu
        """)
        if st.button("Lihat Antrian", key="antrian_btn"):
            change_page("Antrian")

# [Bagian Optimasi Produksi, EOQ, dan Model Antrian tetap sama seperti kode sebelumnya]
# ... (salin semua kode halaman Optimasi, EOQ, dan Antrian dari versi sebelumnya)

# =============== HALAMAN OPTIMASI PRODUKSI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📈 OPTIMASI PRODUKSI")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
        st.subheader("Contoh Kasus Produksi")
        st.markdown("""
        **Perusahaan XYZ** memproduksi 2 jenis produk:
        - Produk A: Keuntungan Rp5.000/unit, butuh 2 jam/unit
        - Produk B: Keuntungan Rp8.000/unit, butuh 4 jam/unit
        
        Total waktu produksi tersedia: **40 jam/minggu**
        
        Berapa kombinasi produksi optimal untuk keuntungan maksimal?
        """)
        
        if st.button("💡 Lihat Solusi", type="secondary"):
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.latex(r"""
                \begin{aligned}
                \text{Maksimumkan } & Z = 5000x_1 + 8000x_2 \\
                \text{Dengan kendala: } & 2x_1 + 4x_2 \leq 40 \\
                & x_1 \geq 0, x_2 \geq 0
                \end{aligned}
                """)
            
            with cols[1]:
                st.markdown("""
                **Langkah Penyelesaian:**
                1. Gambar grafik kendala
                2. Temukan titik pojok daerah layak
                3. Hitung nilai Z di setiap titik
                """)
            
            # Buat grafik contoh
            fig, ax = plt.subplots()
            x = np.linspace(0, 20, 100)
            y = (40 - 2*x)/4
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, 0, y, alpha=0.1)
            ax.plot(0, 10, 'ro', markersize=8)
            ax.plot(20, 0, 'go', markersize=8)
            ax.set_xlabel('Produk A')
            ax.set_ylabel('Produk B')
            ax.grid(True)
            st.pyplot(fig)
            
            st.success("""
            **Solusi Optimal:**
            - Produksi 0 unit Produk A
            - Produksi 10 unit Produk B
            - Keuntungan Maksimum: Rp80.000/minggu
            """)
    
    # Input Parameter
    with st.expander("🔧 PARAMETER PRODUKSI", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Barang A")
            p_a = st.number_input("Keuntungan/unit (Rp)", 5000, key="p_a")
            t_a = st.number_input("Waktu produksi (jam)", 2, key="t_a")
        with col2:
            st.subheader("Barang B")
            p_b = st.number_input("Keuntungan/unit (Rp)", 8000, key="p_b")
            t_b = st.number_input("Waktu produksi (jam)", 4, key="t_b")
        
        total = st.number_input("Total waktu tersedia (jam)", 40, key="total")
    
    # Hitung Solusi
    if st.button("🧮 HITUNG SOLUSI DETAIL", type="primary", use_container_width=True):
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
        
        # PENYELESAIAN
        titik_A = (0, total/t_b)
        titik_B = (total/t_a, 0)
        
        optimal_value = max(p_a*titik_B[0], p_b*titik_A[1])
        
        # GRAFIK SOLUSI
        fig, ax = plt.subplots(figsize=(10,6))
        x = np.linspace(0, titik_B[0], 100)
        y = (total - t_a*x)/t_b
        ax.plot(x, y, 'b-', linewidth=2, label=f'{t_a}x₁ + {t_b}x₂ ≤ {total}')
        ax.fill_between(x, 0, y, alpha=0.1)
        ax.plot(titik_A[0], titik_A[1], 'ro', markersize=8, label=f'Titik A (0,{titik_A[1]:.0f})')
        ax.plot(titik_B[0], titik_B[1], 'go', markersize=8, label=f'Titik B ({titik_B[0]:.0f},0)')
        ax.set_xlabel('Jumlah Barang A (x₁)')
        ax.set_ylabel('Jumlah Barang B (x₂)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        
        # HASIL
        st.success(f"""
        ## 🎯 KESIMPULAN PRODUKSI OPTIMAL
        **Kombinasi Produksi:**
        - Produksi **Barang A**: {titik_B[0]:.0f} unit
        - Produksi **Barang B**: {titik_A[1]:.0f} unit
        
        **Pendapatan Maksimum:** Rp{optimal_value:,.0f}
        """)

# =============== HALAMAN MODEL PERSEDIAAN (EOQ) ===============
elif st.session_state.current_page == "EOQ":
    st.title("📦 MODEL PERSEDIAAN (EOQ)")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
        st.subheader("Contoh Kasus Inventory")
        st.markdown("""
        **Toko Elektronik ABC** memiliki:
        - Permintaan tahunan: 1.200 unit
        - Biaya pemesanan: Rp200.000/order
        - Biaya penyimpanan: Rp50.000/unit/tahun
        
        Hitung jumlah pesanan ekonomis (EOQ)!
        """)
        
        if st.button("💡 Hitung EOQ Contoh", key="eoq_example"):
            D = 1200
            S = 200000
            H = 50000
            
            eoq = np.sqrt(2*D*S/H)
            total_cost = np.sqrt(2*D*S*H)
            
            st.markdown("---")
            st.subheader("Penyelesaian:")
            st.latex(rf"""
            \begin{{aligned}}
            EOQ &= \sqrt{{\frac{{2DS}}{{H}}}} \\
            &= \sqrt{{\frac{{2 \times 1200 \times 200000}}{{50000}}}} \\
            &= {eoq:.1f} \text{{ unit}}
            \end{{aligned}}
            """)
            
            st.success(f"""
            **Interpretasi:**
            - Pesan **{eoq:.0f} unit** setiap kali order
            - Total biaya persediaan minimum: **Rp{total_cost:,.0f}/tahun**
            - Frekuensi order: **{D/eoq:.1f} kali/tahun**
            """)
    
    # Input Parameter
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
elif st.session_state.current_page == "Antrian":
    st.title("🔄 MODEL ANTRIAN (M/M/1)")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
        st.subheader("Contoh Kasus Antrian Bank")
        st.markdown("""
        **Bank DEF** memiliki sistem antrian dengan:
        - Tingkat kedatangan nasabah: 15 orang/jam
        - Tingkat pelayanan teller: 20 orang/jam
        
        Hitung parameter kinerja sistem!
        """)
        
        if st.button("💡 Analisis Sistem", key="queue_example"):
            λ = 15
            μ = 20
            
            ρ = λ/μ
            W = 1/(μ-λ)
            L = λ*W
            
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.latex(rf"""
                \begin{{aligned}}
                \rho &= \frac{{\lambda}}{{\mu}} = \frac{{15}}{{20}} = 0.75 \\
                W &= \frac{{1}}{{\mu-\lambda}} = \frac{{1}}{{5}} = 0.2 \text{{ jam}} \\
                &= 12 \text{{ menit}}
                \end{{aligned}}
                """)
            
            with cols[1]:
                st.latex(rf"""
                \begin{{aligned}}
                L &= \lambda W = 15 \times 0.2 = 3 \text{{ nasabah}} \\
                L_q &= \lambda W_q \approx 2.25 \text{{ nasabah}}
                \end{{aligned}}
                """)
            
            st.warning("""
            **Rekomendasi Manajerial:**
            - Utilisasi teller 75% (cukup sibuk)
            - Rata-rata nasabah menunggu 12 menit
            - Jika ingin mengurangi waktu tunggu, tambahkan teller kedua
            """)
    
    # Input Parameter
    with st.expander("🔧 PARAMETER PELAYANAN", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            λ = st.number_input("Tingkat kedatangan (pelanggan/jam)", min_value=0.1, value=10.0, step=0.1)
        with col2:
            μ = st.number_input("Tingkat pelayanan (pelanggan/jam)", min_value=0.1, value=12.0, step=0.1)
    
    if st.button("🧮 HITUNG PARAMETER", type="primary", use_container_width=True):
        if μ <= λ:
            st.error("Tingkat pelayanan (μ) harus lebih besar dari tingkat kedatangan (λ) untuk sistem stabil")
        else:
            ρ = λ/μ
            W = 1/(μ-λ)
            Wq = W - (1/μ)
            L = λ*W
            Lq = λ*Wq
            
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
elif st.session_state.current_page == "➕ Tambah Data":
    st.title("TAMBAH DATA BARU")
    st.warning("Fitur dalam pengembangan...")
