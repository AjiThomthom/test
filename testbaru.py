# 1. IMPORTS (tetap seperti semula)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image

# 2. SET PAGE CONFIG (PINDAHKAN KE SINI, SEBELUM APAPUN)
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Analisis Data",
    page_icon="📊",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# 3. KODE ANDA YANG LAIN (setelah set_page_config)
st.title("Analisis Data")
# ... lanjutkan dengan kode Anda yang lain ...

# =============== GENERATE LOGO & HEADER ===============
def create_logo():
    try:
        img = Image.new('RGBA', (300, 100), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        for i in range(100):
            draw.line([(0,i), (300,i)], fill=(0, 100+i, 200))
        
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((30, 35), "APLIKASI MODEL MATEMATIKA", 
                fill=(255,255,255), font=font)
        
        img = ImageOps.expand(img, border=3, fill=(255,195,0))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error membuat logo: {str(e)}")
        return ""

def create_header():
    try:
        img = Image.new('RGB', (1200, 250), (33, 37, 41))
        draw = ImageDraw.Draw(img)
        
        for i in range(-250, 1200, 40):
            draw.line([(i,0), (i+300,250)], fill=(52, 58, 64), width=3)
        
        try:
            font = ImageFont.truetype("arialbd.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        draw.text((150, 80), "APLIKASI MODEL MATEMATIKA INDUSTRI", 
                fill=(70, 200, 200), font=font)
        
        try:
            subfont = ImageFont.truetype("arial.ttf", 20)
        except:
            subfont = ImageFont.load_default()
        
        draw.text((150, 150), "Alat Optimasi untuk Solusi Industri", 
                fill=(200,200,200), font=subfont)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=90)
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error membuat header: {str(e)}")
        return ""

# =============== KONFIGURASI APLIKASI ===============
LOGO_BASE64 = create_logo()
HEADER_BASE64 = create_header()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

def change_page(page_name):
    st.session_state.current_page = page_name

st.set_page_config(
    layout="wide", 
    page_title="Aplikasi Model Industri",
    page_icon="🧮",
    menu_items={
        'Get Help': 'https://wa.me/6283153610195',
        'Report a bug': None,
        'About': "Aplikasi untuk optimasi proses industri"
    }
)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

def change_page(page_name):
    st.session_state.current_page = page_name

# =============== NAVIGASI SIDEBAR ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", use_container_width=True)
    st.title("MENU UTAMA")
    
    # Tombol navigasi dengan ikon menarik
    nav_options = [
        ("🏠", "Beranda"),
        ("📊", "Optimasi"),
        ("📦", "EOQ"),
        ("🔄", "Antrian"),
        ("⏱", "Johnson")
    ]
    
    for icon, page in nav_options:
        st.button(f"{icon} {page}", 
                 on_click=change_page, 
                 args=(page,), 
                 use_container_width=True,
                 key=f"nav_{page}")
    
    # Tambahkan tombol Model Baru dengan style berbeda
    st.markdown("---")
    st.button("✨ MODEL BARU", 
             on_click=change_page, 
             args=("Model Baru",),
             use_container_width=True,
             type="primary")
    
    st.markdown("---")
    st.info("""
    **Kontak Pengembang:**
    [WhatsApp](https://wa.me/6283153610195)
    
    **Versi 3.0**  
    🇮🇩 🇵🇸  
    © 2025
    """)

# =============== HALAMAN BERANDA ===============
if st.session_state.current_page == "Beranda":
    st.title("Selamat Datang di Aplikasi Model Matematika Industri")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    
    # Metrics cards
    cols = st.columns(4)
    features = [
        ("📊", "Optimasi Produksi", "Linear Programming untuk maksimalkan keuntungan", "#3498db"),
        ("📦", "Manajemen Inventori", "Model EOQ untuk optimasi persediaan", "#2ecc71"),
        ("🔄", "Analisis Antrian", "Model M/M/1 untuk sistem pelayanan", "#e74c3c"),
        ("⏱", "Penjadwalan", "Johnson's Rule untuk minimasi makespan", "#f39c12")
    ]
    
    for col, (icon, title, desc, color) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div style="
                border-left: 5px solid {color};
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
                margin-bottom: 20px;
                height: 180px;
            ">
                <h3>{icon} {title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Panduan Cepat
    with st.expander("📚 PANDUAN PENGGUNAAN", expanded=True):
        st.write("""
        1. Pilih menu di sidebar sesuai kebutuhan
        2. Masukkan parameter yang diminta
        3. Klik tombol hitung untuk melihat hasil
        4. Gunakan menu atas untuk ekspor hasil
        """)
        st.image("https://via.placeholder.com/600x200?text=Tutorial+Penggunaan", use_container_width=True)

# =============== HALAMAN MODEL BARU ===============
elif st.session_state.current_page == "Model Baru":
    st.title("✨ FITUR BARU")
    st.image("https://via.placeholder.com/800x300?text=Fitur+Sedang+Dikembangkan", use_container_width=True)
    
    with st.container(border=True):
        st.warning("""
        ## 🚧 FITUR DALAM PENGEMBANGAN
        Kami sedang mengembangkan fitur-fitur baru untuk aplikasi ini.
        """)
        
        st.info("""
        ### 💡 Punya ide fitur?
        Kirim saran Anda via:
        **WhatsApp: [+62 831-5361-0195](https://wa.me/6283153610195)**
        """)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 30px;">
            <img src="https://via.placeholder.com/150?text=Coming+Soon" width="200">
            <p style="font-style: italic;">Versi berikutnya akan segera hadir</p>
        </div>
        """, unsafe_allow_html=True)

# =============== HALAMAN OPTIMASI PRODUKSI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📊 OPTIMASI PRODUKSI")
    
    with st.expander("📚 CONTOH KASUS", expanded=True):
        st.subheader("Studi Kasus: Perusahaan Furniture")
        st.markdown("""
        **PT Kayu Indah** memproduksi:
        - **Meja**: Keuntungan Rp120.000/unit, butuh 3 jam pengerjaan
        - **Kursi**: Keuntungan Rp80.000/unit, butuh 2 jam pengerjaan
        
        **Kendala:**
        - Waktu produksi maksimal 120 jam/minggu
        - Permintaan pasar maksimal 30 meja dan 40 kursi per minggu
        """)
        
        if st.button("💡 Lihat Solusi Contoh", type="secondary"):
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.latex(r"""
                \begin{aligned}
                \text{Maksimalkan } & Z = 120000x_1 + 80000x_2 \\
                \text{Dengan kendala: } & 3x_1 + 2x_2 \leq 120 \\
                & x_1 \leq 30 \\
                & x_2 \leq 40 \\
                & x_1 \geq 0, x_2 \geq 0
                \end{aligned}
                """)
            
            with cols[1]:
                st.markdown("""
                **Solusi Optimal:**
                - Produksi 30 meja
                - Produksi 15 kursi
                - Keuntungan maksimum: Rp4.800.000/minggu
                """)
            
            fig, ax = plt.subplots(figsize=(10,6))
            x = np.linspace(0, 40, 100)
            y1 = (120 - 3*x)/2
            ax.plot(x, y1, 'b-', label='3x₁ + 2x₂ ≤ 120')
            ax.axvline(30, color='r', label='x₁ ≤ 30')
            ax.axhline(40, color='g', label='x₂ ≤ 40')
            ax.fill_between(x, 0, np.minimum(y1, 40), where=(x<=30), alpha=0.1)
            ax.plot(30, 15, 'ro', markersize=8)
            ax.set_xlabel('Meja (x₁)')
            ax.set_ylabel('Kursi (x₂)')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    with st.expander("🔧 PARAMETER PRODUKSI", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Produk 1")
            p1 = st.number_input("Keuntungan/unit (Rp)", 120000, key="p1")
            t1 = st.number_input("Waktu produksi (jam)", 3, key="t1")
            max1 = st.number_input("Maksimal permintaan", 30, key="max1")
        with col2:
            st.subheader("Produk 2")
            p2 = st.number_input("Keuntungan/unit (Rp)", 80000, key="p2")
            t2 = st.number_input("Waktu produksi (jam)", 2, key="t2")
            max2 = st.number_input("Maksimal permintaan", 40, key="max2")
        
        total_time = st.number_input("Total waktu tersedia (jam)", 120, key="total")

    if st.button("🧮 HITUNG SOLUSI OPTIMAL", type="primary", use_container_width=True):
        titik_A = (0, 0)
        titik_B = (max1, 0)
        titik_C = (max1, min((total_time - t1*max1)/t2, max2))
        titik_D = (min((total_time - t2*max2)/t1, max1), max2)
        titik_E = (0, min(total_time/t2, max2))
        
        nilai_Z = [
            p1*titik_A[0] + p2*titik_A[1],
            p1*titik_B[0] + p2*titik_B[1],
            p1*titik_C[0] + p2*titik_C[1],
            p1*titik_D[0] + p2*titik_D[1],
            p1*titik_E[0] + p2*titik_E[1]
        ]
        optimal_idx = np.argmax(nilai_Z)
        optimal_value = nilai_Z[optimal_idx]
        optimal_point = [titik_A, titik_B, titik_C, titik_D, titik_E][optimal_idx]

        st.markdown("---")
        st.header("📊 HASIL PERHITUNGAN")
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Fungsi Tujuan")
            st.latex(fr"""
            \text{{Maksimalkan }}
            \boxed{{
            Z = {p1}x_1 + {p2}x_2
            }}
            """)
            
            st.subheader("Titik Pojok")
            st.write(f"A(0,0) = Rp{nilai_Z[0]:,.0f}")
            st.write(f"B({max1},0) = Rp{nilai_Z[1]:,.0f}")
            st.write(f"C({titik_C[0]:.0f},{titik_C[1]:.0f}) = Rp{nilai_Z[2]:,.0f}")
            st.write(f"D({titik_D[0]:.0f},{max2}) = Rp{nilai_Z[3]:,.0f}")
            st.write(f"E(0,{titik_E[1]:.0f}) = Rp{nilai_Z[4]:,.0f}")
        
        with cols[1]:
            st.subheader("Visualisasi Solusi")
            fig, ax = plt.subplots(figsize=(8,6))
            x = np.linspace(0, max1*1.1, 100)
            y = (total_time - t1*x)/t2
            ax.plot(x, y, 'b-', label=f'{t1}x₁ + {t2}x₂ ≤ {total_time}')
            ax.fill_between(x, 0, np.minimum(y, max2), where=(x<=max1), alpha=0.1)
            ax.axvline(max1, color='r', label=f'x₁ ≤ {max1}')
            ax.axhline(max2, color='g', label=f'x₂ ≤ {max2}')
            ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=8)
            ax.set_xlabel('Produk 1 (x₁)')
            ax.set_ylabel('Produk 2 (x₂)')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        
        st.success(f"""
        ## 🎯 SOLUSI OPTIMAL
        **Produksi:**
        - Produk 1: {optimal_point[0]:.0f} unit
        - Produk 2: {optimal_point[1]:.0f} unit
        
        **Keuntungan Maksimum:** Rp{optimal_value:,.0f}
        """)

# =============== HALAMAN EOQ ===============
elif st.session_state.current_page == "EOQ":
    st.title("📦 MODEL PERSEDIAAN (EOQ)")
    
    with st.expander("📚 CONTOH KASUS", expanded=True):
        st.subheader("Studi Kasus: Toko Bahan Bangunan")
        st.markdown("""
        **Toko Bangun Jaya** memiliki data:
        - Permintaan semen: 10,000 sak/tahun
        - Biaya pemesanan: Rp150.000/order
        - Biaya penyimpanan: Rp5.000/sak/tahun
        - Waktu tunggu pengiriman: 5 hari
        """)
        
        if st.button("💡 Hitung Contoh", type="secondary"):
            D = 10000
            S = 150000
            H = 5000
            L = 5
            
            eoq = np.sqrt(2*D*S/H)
            rop = (D/365)*L
            total_cost = np.sqrt(2*D*S*H)
            
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.latex(rf"""
                \begin{{aligned}}
                EOQ &= \sqrt{{\frac{{2DS}}{{H}}}} \\
                &= \sqrt{{\frac{{2 \times 10000 \times 150000}}{{5000}}}} \\
                &= {eoq:.0f} \text{{ sak}}
                \end{{aligned}}
                """)
                
                st.latex(rf"""
                \begin{{aligned}}
                ROP &= \frac{{D}}{{365}} \times L \\
                &= \frac{{10000}}{{365}} \times 5 \\
                &= {rop:.1f} \text{{ sak}}
                \end{{aligned}}
                """)
            
            with cols[1]:
                st.latex(rf"""
                \begin{{aligned}}
                TC &= \sqrt{{2DSH}} \\
                &= \sqrt{{2 \times 10000 \times 150000 \times 5000}} \\
                &= \text{{Rp}}{total_cost:,.0f}
                \end{{aligned}}
                """)
            
            st.success(f"""
            **Interpretasi:**
            - Pesan **{eoq:.0f} sak** setiap kali order
            - Lakukan pemesanan ulang saat stok **{rop:.1f} sak**
            - Total biaya persediaan: **Rp{total_cost:,.0f}/tahun**
            - Frekuensi order: **{D/eoq:.1f} kali/tahun**
            """)

    with st.expander("🔧 PARAMETER INVENTORY", expanded=True):
        D = st.number_input("Permintaan tahunan (unit)", 10000)
        S = st.number_input("Biaya pemesanan per pesanan (Rp)", 150000)
        H = st.number_input("Biaya penyimpanan per unit per tahun (Rp)", 5000)
        L = st.number_input("Waktu tunggu pengiriman (hari)", 5)

    if st.button("🧮 HITUNG EOQ", type="primary", use_container_width=True):
        eoq = np.sqrt(2*D*S/H)
        rop = (D/365)*L
        total_cost = np.sqrt(2*D*S*H)
        
        st.markdown("---")
        st.header("📊 HASIL PERHITUNGAN")
        
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
            
            st.subheader("Titik Pemesanan Ulang (ROP)")
            st.latex(fr"""
            ROP = \frac{{D}}{{365}} \times L = \frac{{{D:,}}}{{365}} \times {L} = {rop:.1f}
            """)
            
        with cols[1]:
            st.subheader("Biaya Total")
            st.latex(fr"""
            \begin{{aligned}}
            \text{{Biaya Penyimpanan}} &= \frac{{Q}}{{2}} \times H = \frac{{{eoq:.1f}}}{{2}} \times {H:,} = \text{{Rp}}{(eoq/2*H):,.0f} \\
            \text{{Biaya Pemesanan}} &= \frac{{D}}{{Q}} \times S = \frac{{{D:,}}}{{{eoq:.1f}}} \times {S:,} = \text{{Rp}}{(D/eoq*S):,.0f} \\
            \text{{Total Biaya}} &= \text{{Rp}}{total_cost:,.0f}
            \end{{aligned}}
            """)
        
        st.success(f"""
        ## 🎯 REKOMENDASI
        **Jumlah pesanan ekonomis:** {eoq:.0f} unit  
        **Frekuensi pemesanan:** {D/eoq:.1f} kali/tahun  
        **Lakukan pemesanan ulang ketika stok mencapai:** {rop:.1f} unit  
        **Total biaya persediaan minimum:** Rp{total_cost:,.0f}/tahun
        """)

# =============== HALAMAN ANTRIAN ===============
elif st.session_state.current_page == "Antrian":
    st.title("🔄 MODEL ANTRIAN (M/M/1)")
    
    with st.expander("📚 CONTOH KASUS", expanded=True):
        st.subheader("Studi Kasus: Klinik Kesehatan")
        st.markdown("""
        **Klinik Sehat Bahagia** memiliki:
        - Kedatangan pasien: 12 pasien/jam
        - Tingkat pelayanan: 15 pasien/jam
        - Biaya menunggu pasien: Rp50.000/jam
        - Biaya tambahan dokter: Rp200.000/jam
        """)
        
        if st.button("💡 Analisis Contoh", type="secondary"):
            λ = 12
            μ = 15
            ρ = λ/μ
            Wq = (λ)/(μ*(μ-λ))
            Lq = λ*Wq
            cost_waiting = Wq*λ*50000
            
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.latex(rf"""
                \begin{{aligned}}
                \rho &= \frac{{\lambda}}{{\mu}} = \frac{{12}}{{15}} = 0.8 \\
                W_q &= \frac{{\lambda}}{{\mu(\mu-\lambda)}} = \frac{{12}}{{15(15-12)}} = {Wq:.3f} \text{{ jam}} \\
                &= {Wq*60:.1f} \text{{ menit}} \\
                L_q &= \lambda W_q = 12 \times {Wq:.3f} = {Lq:.1f} \text{{ pasien}}
                \end{{aligned}}
                """)
            
            with cols[1]:
                st.latex(rf"""
                \begin{{aligned}}
                \text{{Biaya Menunggu}} &= W_q \times \lambda \times 50000 \\
                &= {Wq:.3f} \times 12 \times 50000 \\
                &= \text{{Rp}}{cost_waiting:,.0f}/\text{{jam}}
                \end{{aligned}}
                """)
            
            st.warning("""
            **Rekomendasi Manajerial:**
            - Utilisasi sistem saat ini: 80% (sangat sibuk)
            - Rata-rata pasien menunggu 16 menit
            - Biaya antrian: Rp1.200.000/jam
            - **Pertimbangkan** menambah dokter jika biaya antrian > biaya tambahan dokter
            """)

    with st.expander("🔧 PARAMETER PELAYANAN", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            λ = st.number_input("Tingkat kedatangan (pelanggan/jam)", min_value=0.1, value=12.0, step=0.1)
        with col2:
            μ = st.number_input("Tingkat pelayanan (pelanggan/jam)", min_value=0.1, value=15.0, step=0.1)
        
        cost_waiting = st.number_input("Biaya menunggu per pelanggan/jam (Rp)", 50000)
        cost_add_server = st.number_input("Biaya tambahan server/jam (Rp)", 200000)

    if st.button("🧮 HITUNG PARAMETER", type="primary", use_container_width=True):
        if μ <= λ:
            st.error("Error: Tingkat pelayanan harus > tingkat kedatangan (μ > λ)")
        else:
            ρ = λ/μ
            W = 1/(μ-λ)
            Wq = W - (1/μ)
            L = λ*W
            Lq = λ*Wq
            total_waiting_cost = Wq*λ*cost_waiting
            
            st.markdown("---")
            st.header("📊 HASIL PERHITUNGAN")
            
            cols = st.columns(2)
            with cols[0]:
                st.subheader("Parameter Utama")
                st.latex(rf"""
                \begin{{aligned}}
                \rho &= \frac{{\lambda}}{{\mu}} = \frac{{{λ}}}{{{μ}}} = {ρ:.2f} \\
                W &= \frac{{1}}{{\mu-\lambda}} = \frac{{1}}{{{μ}-{λ}}} = {W:.2f} \text{{ jam}} \\
                W_q &= W - \frac{{1}}{{\mu}} = {Wq:.2f} \text{{ jam}} \\
                &= {Wq*60:.1f} \text{{ menit}}
                \end{{aligned}}
                """)
            
            with cols[1]:
                st.subheader("Jumlah Pelanggan")
                st.latex(rf"""
                \begin{{aligned}}
                L &= \lambda W = {λ} \times {W:.2f} = {L:.1f} \\
                L_q &= \lambda W_q = {λ} \times {Wq:.2f} = {Lq:.1f}
                \end{{aligned}}
                """)
            
            st.subheader("Analisis Biaya")
            st.write(f"**Biaya menunggu total:** Rp{total_waiting_cost:,.0f}/jam")
            
            if cost_add_server > 0:
                new_μ = μ + 15
                new_Wq = (λ)/(new_μ*(new_μ-λ))
                new_cost = new_Wq*λ*cost_waiting + cost_add_server
                improvement = (total_waiting_cost - new_cost)/total_waiting_cost*100
                
                st.write(f"**Dengan tambahan server (μ={new_μ}):**")
                st.write(f"- Waktu tunggu baru: {new_Wq*60:.1f} menit")
                st.write(f"- Total biaya baru: Rp{new_cost:,.0f}/jam")
                st.write(f"- Penghematan: {improvement:.1f}%")
            
            util_status = ""
            if ρ <= 0.7:
                util_status = "Optimal (70% atau kurang)"
            elif ρ <= 0.8:
                util_status = "Batas Atas (80%)"
            elif ρ <= 0.9:
                util_status = "Sibuk (90%)"
            else:
                util_status = "Overload (>90%)"
            
            st.success(f"""
            ## 🎯 STATUS SISTEM
            **Tingkat Utilisasi:** {ρ:.0%}  
            **Kategori:** {util_status}
            
            **Rekomendasi:**
            - Waktu tunggu rata-rata: {Wq*60:.1f} menit
            - Pelanggan dalam antrian: {Lq:.1f}
            - {'Pertimbangkan penambahan server' if ρ > 0.7 else 'Sistem dalam kondisi baik'}
            """)

# =============== HALAMAN JOHNSON ===============
elif st.session_state.current_page == "Johnson":
    st.title("⏱ PENJADWALAN (JOHNSON'S RULE)")
    
    with st.expander("📚 CONTOH KASUS", expanded=True):
        st.subheader("Studi Kasus: Bengkel Mobil")
        st.markdown("""
        **Bengkel Cepat** memiliki 5 pekerjaan dengan waktu proses:
        | Pekerjaan | Pengecatan (Jam) | Perakitan (Jam) |
        |-----------|------------------|-----------------|
        | Mobil A   | 3                | 6               |
        | Mobil B   | 5                | 2               |
        | Mobil C   | 1                | 7               |
        | Mobil D   | 6                | 4               |
        | Mobil E   | 7                | 3               |
        """)
        
        if st.button("💡 Lihat Solusi", type="secondary"):
            jobs = [(3,6), (5,2), (1,7), (6,4), (7,3)]
            sequence = [2, 0, 3, 4, 1]  # C, A, D, E, B
            makespan = 28
            
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Langkah Algoritma:**")
                st.write("1. Kelompokkan pekerjaan dengan M1 ≤ M2 (C, A, D)")
                st.write("2. Urutkan berdasarkan M1 menaik: C(1), A(3), D(6)")
                st.write("3. Kelompokkan pekerjaan dengan M1 > M2 (B, E)")
                st.write("4. Urutkan berdasarkan M2 menurun: E(3), B(2)")
                st.write("5. Gabungkan urutan: C → A → D → E → B")
                
                st.markdown("**Urutan Optimal:**")
                st.write(" → ".join([f"Mobil {['A','B','C','D','E'][i]}" for i in sequence]))
            
            with cols[1]:
                st.markdown("**Diagram Gantt**")
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,4))
                
                # Machine 1 Schedule
                m1_times = [0, 1, 4, 10, 17]
                for i, job_idx in enumerate(sequence):
                    duration = jobs[job_idx][0]
                    ax1.barh("Pengecatan", duration, left=m1_times[i], 
                            label=f'Mobil {["A","B","C","D","E"][job_idx]}')
                    ax1.text(m1_times[i]+duration/2, 0, f'{["A","B","C","D","E"][job_idx]}', 
                            ha='center', va='center', color='white')
                
                # Machine 2 Schedule
                m2_times = [1, 7, 13, 17, 20]
                for i, job_idx in enumerate(sequence):
                    duration = jobs[job_idx][1]
                    ax2.barh("Perakitan", duration, left=m2_times[i])
                    ax2.text(m2_times[i]+duration/2, 0, f'{["A","B","C","D","E"][job_idx]}', 
                            ha='center', va='center', color='white')
                
                ax1.set_xlim(0, makespan)
                ax2.set_xlim(0, makespan)
                ax1.set_xticks(range(0, makespan+1, 2))
                ax2.set_xticks(range(0, makespan+1, 2))
                ax1.grid(True)
                ax2.grid(True)
                st.pyplot(fig)
            
            st.success(f"""
            **Hasil Akhir:**
            - Makespan: {makespan} jam
            - Efisiensi: {sum(j[0]+j[1] for j in jobs)/makespan/2*100:.1f}%
            """)

    with st.expander("🔧 INPUT DATA PEKERJAAN", expanded=True):
        num_jobs = st.number_input("Jumlah Pekerjaan", min_value=2, max_value=10, value=5, key="num_jobs")
        
        st.write("**Waktu Proses di Setiap Mesin:**")
        jobs = []
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Mesin 1")
            m1_times = [st.number_input(f"Pekerjaan {i+1}", min_value=1, 
                                      value=[3,5,1,6,7][i] if i<5 else 2, 
                                      key=f"m1_{i}") for i in range(num_jobs)]
        with cols[1]:
            st.subheader("Mesin 2")
            m2_times = [st.number_input(f"Pekerjaan {i+1}", min_value=1, 
                                      value=[6,2,7,4,3][i] if i<5 else 3, 
                                      key=f"m2_{i}") for i in range(num_jobs)]
        
        jobs = list(zip(m1_times, m2_times))

    if st.button("🧮 HITUNG JADWAL OPTIMAL", type="primary", use_container_width=True):
        group1 = [(i, m1, m2) for i, (m1, m2) in enumerate(jobs) if m1 <= m2]
        group2 = [(i, m2, m1) for i, (m1, m2) in enumerate(jobs) if m1 > m2]
        
        group1_sorted = sorted(group1, key=lambda x: x[1])
        group2_sorted = sorted(group2, key=lambda x: x[1], reverse=True)
        
        sequence = [x[0] for x in group1_sorted] + [x[0] for x in group2_sorted]
        
        m1_time = 0
        m2_time = 0
        m1_schedule = []
        m2_schedule = []
        
        for job in sequence:
            m1_start = m1_time
            m1_time += jobs[job][0]
            m1_schedule.append((job, m1_start, m1_time))
            
            m2_start = max(m1_time, m2_time)
            m2_time = m2_start + jobs[job][1]
            m2_schedule.append((job, m2_start, m2_time))
        
        makespan = m2_time
        
        st.markdown("---")
        st.header("📊 HASIL PENJADWALAN")
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Urutan Optimal")
            st.write(" → ".join([f"Pekerjaan {i+1}" for i in sequence]))
            
            st.subheader("Detail Waktu")
            for i, job in enumerate(sequence):
                st.write(f"**Pekerjaan {job+1}**:")
                st.write(f"- Mesin 1: {jobs[job][0]} jam (mulai: {m1_schedule[i][1]}, selesai: {m1_schedule[i][2]})")
                st.write(f"- Mesin 2: {jobs[job][1]} jam (mulai: {m2_schedule[i][1]}, selesai: {m2_schedule[i][2]})")
        
        with cols[1]:
            st.subheader("Diagram Gantt")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,6))
            
            for job, start, end in m1_schedule:
                ax1.barh("Mesin 1", end-start, left=start, 
                        label=f'P{job+1}')
                ax1.text(start + (end-start)/2, 0, f'P{job+1}', 
                        ha='center', va='center', color='white')
            
            for job, start, end in m2_schedule:
                ax2.barh("Mesin 2", end-start, left=start)
                ax2.text(start + (end-start)/2, 0, f'P{job+1}', 
                        ha='center', va='center', color='white')
            
            ax1.set_xlim(0, makespan)
            ax2.set_xlim(0, makespan)
            ax1.set_xticks(range(0, makespan+1, max(1, makespan//10)))
            ax2.set_xticks(range(0, makespan+1, max(1, makespan//10)))
            ax1.grid(True)
            ax2.grid(True)
            ax1.set_xlabel("Waktu (jam)")
            ax2.set_xlabel("Waktu (jam)")
            plt.tight_layout()
            st.pyplot(fig)
        
        total_processing = sum(m1+m2 for m1,m2 in jobs)
        efficiency = total_processing/(2*makespan)*100
        
        st.success(f"""
        ## 🎯 PERFORMANCE
        **Makespan:** {makespan} jam  
        **Efisiensi:** {efficiency:.1f}%  
        **Total Waktu Proses:** {total_processing} jam  
        **Idle Time Mesin 1:** {makespan - sum(m1 for m1,m2 in jobs):.1f} jam  
        **Idle Time Mesin 2:** {makespan - sum(m2 for m1,m2 in jobs):.1f} jam
        """)

# =============== STYLE CUSTOM ===============
st.markdown("""
<style>
    /* Tombol lebih menarik */
    .stButton>button {
        transition: all 0.3s;
        border-radius: 8px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Font konsisten */
    .st-emotion-cache-1qg05tj {
        font-family: "Arial", sans-serif;
    }
    
    /* Warna tema */
    :root {
        --primary: #3498db;
        --secondary: #2ecc71;
    }
    
    /* Header cards */
    .stMarkdown h3 {
        color: var(--primary);
    }
</style>
""", unsafe_allow_html=True)
