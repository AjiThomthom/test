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

# =============== HALAMAN JOHNSON'S RULE ===============
elif st.session_state.current_page == "Johnson":
    st.title("⏱ PENJADWALAN DENGAN JOHNSON'S RULE")
    
    with st.expander("📚 Penjelasan Algoritma", expanded=True):
        st.markdown("""
        **Johnson's Rule** digunakan untuk penjadwalan **2 mesin** dan **N pekerjaan** dengan ketentuan:
        - Setiap pekerjaan harus melalui Mesin 1 lalu Mesin 2
        - Tujuan: **Meminimalkan makespan** (total waktu penyelesaian)
        """)
        st.image("https://i.imgur.com/JjQfZgX.png", use_container_width=True)
    
    # Input Data
    with st.expander("🔧 INPUT DATA PEKERJAAN", expanded=True):
        num_jobs = st.number_input("Jumlah Pekerjaan", min_value=2, max_value=10, value=3)
        
        cols = st.columns(2)
        m1_times, m2_times = [], []
        with cols[0]:
            st.subheader("Mesin 1")
            m1_times = [st.number_input(f"Pekerjaan {i+1}", min_value=1, value=(i+1)*2, key=f"m1_{i}") for i in range(num_jobs)]
        with cols[1]:
            st.subheader("Mesin 2")
            m2_times = [st.number_input(f"Pekerjaan {i+1}", min_value=1, value=(i+1)*3, key=f"m2_{i}") for i in range(num_jobs)]
        
        jobs = list(zip(m1_times, m2_times))

    if st.button("🧮 HITUNG JADWAL OPTIMAL", type="primary", use_container_width=True):
        # Algoritma Johnson's Rule
        def johnsons_rule(jobs):
            group1 = [ (i, m1, m2) for i, (m1, m2) in enumerate(jobs) if m1 <= m2 ]
            group2 = [ (i, m2, m1) for i, (m1, m2) in enumerate(jobs) if m1 > m2 ]
            group1_sorted = sorted(group1, key=lambda x: x[1])
            group2_sorted = sorted(group2, key=lambda x: x[1], reverse=True)
            return [x[0] for x in group1_sorted] + [x[0] for x in group2_sorted]
        
        optimal_sequence = johnsons_rule(jobs)
        
        # Hitung Makespan
        def calculate_makespan(sequence, jobs):
            m1_time = m2_time = 0
            m1_schedule, m2_schedule = [], []
            
            for job in sequence:
                m1_start = m1_time
                m1_time += jobs[job][0]
                m1_schedule.append((job, m1_start, m1_time))
                
                m2_start = max(m1_time, m2_time)
                m2_time = m2_start + jobs[job][1]
                m2_schedule.append((job, m2_start, m2_time))
            
            return m1_schedule, m2_schedule, m2_time
        
        m1_sched, m2_sched, makespan = calculate_makespan(optimal_sequence, jobs)
        
        # Tampilkan Hasil
        st.markdown("---")
        st.header("📝 HASIL PENJADWALAN")
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Urutan Optimal")
            st.write(" → ".join([f"Pekerjaan {i+1}" for i in optimal_sequence]))
            
            st.subheader("Detail Waktu")
            for i in optimal_sequence:
                st.markdown(f"""
                **Pekerjaan {i+1}**:
                - Mesin 1: {jobs[i][0]} satuan waktu
                - Mesin 2: {jobs[i][1]} satuan waktu
                """)
        
        with cols[1]:
            st.subheader("Diagram Gantt")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
            
            # Plot Mesin 1
            for job, start, end in m1_sched:
                ax1.barh("Mesin 1", end-start, left=start, label=f'P{job+1}')
                ax1.text((start+end)/2, 0, f'P{job+1}', ha='center', va='center', color='white')
            
            # Plot Mesin 2
            for job, start, end in m2_sched:
                ax2.barh("Mesin 2", end-start, left=start, label=f'P{job+1}')
                ax2.text((start+end)/2, 0, f'P{job+1}', ha='center', va='center', color='white')
            
            ax1.set_xlabel("Waktu")
            ax2.set_xlabel("Waktu")
            plt.tight_layout()
            st.pyplot(fig)
        
        st.success(f"""
        ## 🎯 TOTAL WAKTU PENYELESAIAN (MAKESPAN): {makespan} satuan waktu
        """)

# =============== FOOTER ===============
st.sidebar.markdown("---")
st.sidebar.info("""
**Versi 2.2.0**  
Dikembangkan oleh:  
*Tim Matematika Industri*  
© 2023
""")
