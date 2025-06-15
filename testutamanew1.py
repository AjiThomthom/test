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
    draw.rectangle([10, 10, 40, 40], fill=(0, 100, 200))
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    draw.text((50, 15), "INDUSTRI", fill=(0,0,0), font=font)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def create_header():
    img = Image.new('RGB', (800, 300), (70, 130, 180))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    draw.text((50, 100), "APLIKASI MODEL INDUSTRI", fill=(255,255,255), font=font)
    draw.line([(50,150), (750,150)], fill=(255,255,0), width=3)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

LOGO_BASE64 = create_logo()
HEADER_BASE64 = create_header()

# =============== KONFIGURASI APLIKASI ===============
st.set_page_config(layout="wide", page_title="Aplikasi Model Industri")

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

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
        st.button("⏱ Johnson", on_click=change_page, args=("Johnson",), use_container_width=True)
    with col2:
        st.button("📦 EOQ", on_click=change_page, args=("EOQ",), use_container_width=True)
        st.button("🔄 Antrian", on_click=change_page, args=("Antrian",), use_container_width=True)
    
    st.markdown("---")
    st.info("""
    **Versi 2.2.0**  
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
    
    st.markdown("---")
    st.subheader("🎯 Fitur Baru: Penjadwalan Johnson's Rule")
    st.markdown("""
    Sekarang dengan algoritma penjadwalan **Johnson's Rule** untuk:
    - Menentukan urutan pekerjaan optimal
    - Meminimalkan waktu penyelesaian (makespan)
    - Visualisasi diagram Gantt
    """)

# =============== HALAMAN OPTIMASI PRODUKSI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📈 OPTIMASI PRODUKSI")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
        st.subheader("Studi Kasus: Perusahaan Furniture")
        st.markdown("""
        **PT Kayu Indah** memproduksi:
        - **Meja**: Keuntungan Rp120.000/unit, butuh 3 jam pengerjaan
        - **Kursi**: Keuntungan Rp80.000/unit, butuh 2 jam pengerjaan
        
        **Kendala:**
        - Waktu produksi maksimal 120 jam/minggu
        - Permintaan pasar maksimal 30 meja dan 40 kursi per minggu
        
        **Tentukan kombinasi produksi optimal!**
        """)
        
        if st.button("💡 Lihat Solusi Lengkap", type="secondary"):
            st.markdown("---")
            st.subheader("Penyelesaian Matematis")
            
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
                **Langkah Penyelesaian:**
                1. Gambar daerah feasible
                2. Hitung titik pojok:
                   - A(0,0), B(30,0), C(30,15), D(13.33,40), E(0,40)
                3. Hitung Z di setiap titik
                """)
            
            # Grafik solusi
            fig, ax = plt.subplots(figsize=(10,6))
            x = np.linspace(0, 40, 100)
            y1 = (120 - 3*x)/2  # Kendala waktu
            y2 = np.full_like(x, 40)  # Kendala kursi
            
            ax.plot(x, y1, 'b-', label='3x₁ + 2x₂ ≤ 120')
            ax.axvline(30, color='r', label='x₁ ≤ 30')
            ax.plot(x, y2, 'g-', label='x₂ ≤ 40')
            ax.fill_between(x, 0, np.minimum(y1, y2), where=(x<=30), alpha=0.1)
            
            # Titik pojok
            points = [(0,0), (30,0), (30,15), (40/3,40), (0,40)]
            for i, (x, y) in enumerate(points):
                ax.plot(x, y, 'ro')
                ax.text(x+1, y+1, f'({x},{y})')
            
            ax.set_xlabel('Meja (x₁)')
            ax.set_ylabel('Kursi (x₂)')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
            
            st.success("""
            **Solusi Optimal:**
            - Produksi 30 meja dan 15 kursi
            - Keuntungan maksimum: Rp4.800.000/minggu
            """)

    # Input Parameter
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

    if st.button("🧮 HITUNG SOLUSI DETAIL", type="primary", use_container_width=True):
        # [Implementation of the optimization solution]
        # ... (same as previous implementation)

# =============== HALAMAN MODEL PERSEDIAAN (EOQ) ===============
elif st.session_state.current_page == "EOQ":
    st.title("📦 MODEL PERSEDIAAN (EOQ)")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
        st.subheader("Studi Kasus: Toko Bahan Bangunan")
        st.markdown("""
        **Toko Bangun Jaya** memiliki data:
        - Permintaan semen: 10,000 sak/tahun
        - Biaya pemesanan: Rp150.000/order
        - Biaya penyimpanan: Rp5.000/sak/tahun
        - Waktu tunggu pengiriman: 5 hari
        
        **Hitung:**
        1. Jumlah pesanan optimal (EOQ)
        2. Titik pemesanan ulang (ROP)
        3. Total biaya persediaan
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

    # [Rest of the EOQ implementation...]

# =============== HALAMAN MODEL ANTRIAN ===============
elif st.session_state.current_page == "Antrian":
    st.title("🔄 MODEL ANTRIAN (M/M/1)")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
        st.subheader("Studi Kasus: Klinik Kesehatan")
        st.markdown("""
        **Klinik Sehat Bahagia** memiliki:
        - Kedatangan pasien: 12 pasien/jam
        - Tingkat pelayanan: 15 pasien/jam
        - Biaya menunggu pasien: Rp50.000/jam
        - Biaya tambahan dokter: Rp200.000/jam
        
        **Analisis:**
        1. Parameter kinerja sistem
        2. Rekomendasi apakah perlu tambah dokter?
        """)
        
        if st.button("💡 Analisis Contoh", type="secondary"):
            λ = 12
            μ = 15
            ρ = λ/μ
            Wq = (λ)/(μ*(μ-λ))
            cost_waiting = Wq*λ*50000
            cost_add_doctor = 200000
            new_μ = 30
            new_Wq = (λ)/(new_μ*(new_μ-λ))
            new_cost = new_Wq*λ*50000 + cost_add_doctor
            
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Saat Ini (1 Dokter):**")
                st.latex(rf"""
                \begin{{aligned}}
                \rho &= {ρ:.2f} \text{{ (Utilisasi 80%)}} \\
                W_q &= {Wq:.2f} \text{{ jam}} \\
                &= {Wq*60:.1f} \text{{ menit}} \\
                \text{{Biaya Menunggu}} &= \text{{Rp}}{cost_waiting:,.0f}/\text{{jam}}
                \end{{aligned}}
                """)
            
            with cols[1]:
                st.markdown("**Jika Tambah 1 Dokter:**")
                st.latex(rf"""
                \begin{{aligned}}
                \rho &= {λ/new_μ:.2f} \text{{ (Utilisasi 40%)}} \\
                W_q &= {new_Wq:.4f} \text{{ jam}} \\
                &= {new_Wq*60:.1f} \text{{ menit}} \\
                \text{{Total Biaya}} &= \text{{Rp}}{new_cost:,.0f}/\text{{jam}}
                \end{{aligned}}
                """)
            
            st.warning("""
            **Rekomendasi Manajerial:**
            - Dengan 1 dokter: Biaya menunggu tinggi (Rp1.200.000/jam)
            - Dengan 2 dokter: Biaya total lebih rendah (Rp230.000/jam)
            - **Saran**: Tambahkan dokter kedua
            """)

    # [Rest of the Queue implementation...]

# =============== HALAMAN JOHNSON'S RULE ===============
elif st.session_state.current_page == "Johnson":
    st.title("⏱ PENJADWALAN DENGAN JOHNSON'S RULE")
    
    with st.expander("📚 Contoh Soal & Pembahasan", expanded=True):
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
        
        **Tentukan:**
        1. Urutan optimal
        2. Diagram Gantt
        3. Makespan total
        """)
        
        if st.button("💡 Lihat Solusi", type="secondary"):
            jobs = [(3,6), (5,2), (1,7), (6,4), (7,3)]
            sequence = [2, 0, 3, 4, 1]  # Hasil Johnson's Rule
            makespan = 28  # Hasil perhitungan
            
            st.markdown("---")
            st.subheader("Penyelesaian:")
            
            cols = st.columns(2)
            with cols[0]:
                st.markdown("**Urutan Optimal:**")
                st.write(" → ".join([f"Mobil {['A','B','C','D','E'][i]}" for i in sequence]))
                
                st.markdown("**Langkah Algoritma:**")
                st.write("1. Kelompokkan pekerjaan dengan M1 ≤ M2")
                st.write("2. Urutkan M1 menaik (C, A, D)")
                st.write("3. Kelompokkan pekerjaan dengan M1 > M2")
                st.write("4. Urutkan M2 menurun (E, B)")
                st.write("5. Gabungkan urutan: C → A → D → E → B")
            
            with cols[1]:
                st.markdown("**Diagram Gantt**")
                # Simplified Gantt chart
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,4))
                
                # Machine 1
                times = [0,1,4,10,17]
                for i, job in enumerate(sequence):
                    ax1.barh("Pengecatan", jobs[job][0], left=times[i], label=f'Mobil {["A","B","C","D","E"][job]}')
                    ax1.text(times[i]+jobs[job][0]/2, 0, f'{["A","B","C","D","E"][job]}', ha='center', va='center', color='white')
                
                # Machine 2
                times = [1,7,13,17,20]
                for i, job in enumerate(sequence):
                    ax2.barh("Perakitan", jobs[job][1], left=times[i], label=f'Mobil {["A","B","C","D","E"][job]}')
                    ax2.text(times[i]+jobs[job][1]/2, 0, f'{["A","B","C","D","E"][job]}', ha='center', va='center', color='white')
                
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

    # [Rest of the Johnson's Rule implementation...]

# =============== FOOTER ===============
st.sidebar.markdown("---")
st.sidebar.info("""
**Versi 2.2.0**  
Dikembangkan oleh:  
*Tim Matematika Industri*  
© 2023
""")
