import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64

# =============== GENERATE LOGO & HEADER (VERSI UPGRADED) ===============
def create_logo():
    try:
        img = Image.new('RGBA', (200, 80), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        # Background gradient
        for i in range(80):
            draw.line([(0,i), (200,i)], fill=(0, 100+i, 200))
        
        # Text with shadow effect
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()
        draw.text((50, 20), "INDUSTRI 4.0", fill=(255,255,255), font=font, stroke_width=2, stroke_fill=(0,0,0))
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error creating logo: {e}")
        return ""

def create_header():
    try:
        img = Image.new('RGB', (1000, 200), (70, 130, 180))
        draw = ImageDraw.Draw(img)
        
        # Diagonal pattern
        for i in range(-200, 1000, 30):
            draw.line([(i,0), (i+200,200)], fill=(100,150,200), width=2)
        
        # Main title
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except:
            font = ImageFont.load_default()
        draw.text((100, 60), "APLIKASI MODEL INDUSTRI", fill=(255,255,0), font=font)
        
        # Add small logo
        logo_img = Image.open(BytesIO(base64.b64decode(LOGO_BASE64)))
        logo_img = logo_img.resize((150,60))
        img.paste(logo_img, (800, 20), logo_img)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Error creating header: {e}")
        return ""

LOGO_BASE64 = create_logo()
HEADER_BASE64 = create_header()

# =============== KONFIGURASI APLIKASI ===============
st.set_page_config(
    layout="wide", 
    page_title="Aplikasi Model Industri",
    page_icon="🏭"
)

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Beranda"

def change_page(page_name):
    st.session_state.current_page = page_name

# =============== NAVIGASI SIDEBAR (DENGAN TOMBOL TAMBAHAN) ===============
with st.sidebar:
    st.image(f"data:image/png;base64,{LOGO_BASE64}", use_column_width=True)
    st.title("NAVIGASI")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🏠 Beranda", on_click=change_page, args=("Beranda",), use_container_width=True)
        st.button("📊 Optimasi", on_click=change_page, args=("Optimasi",), use_container_width=True)
        st.button("⏱ Johnson", on_click=change_page, args=("Johnson",), use_container_width=True)
    with col2:
        st.button("📦 EOQ", on_click=change_page, args=("EOQ",), use_container_width=True)
        st.button("🔄 Antrian", on_click=change_page, args=("Antrian",), use_container_width=True)
        st.button("➕ Model Baru", on_click=change_page, args=("Model Baru",), use_container_width=True)
    
    st.markdown("---")
    st.info("""
    **Versi 2.2.1**  
    Dikembangkan oleh:  
    *Megatama Setiaji & Ronnan Ghazi*  
    🇮🇩 🇵🇸  
    © 2025
    """)

# =============== HALAMAN BERANDA (DIPERBAIKI) ===============
if st.session_state.current_page == "Beranda":
    st.title("Selamat Datang di Aplikasi Model Matematika Industri")
    st.image(f"data:image/jpeg;base64,{HEADER_BASE64}", use_container_width=True)
    
    cols = st.columns(4)  # Diubah dari 3 menjadi 4 kolom
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
    with cols[3]:
        st.info("""
        **⏱ Optimasi Penjadwalan**
        - Johnson's Rule
        - Minimasi makespan
        """)
    
    st.markdown("---")
    st.subheader("📚 Panduan Cepat")
    st.write("""
    1. Pilih menu di sidebar untuk mengakses fitur
    2. Masukkan parameter sesuai kasus Anda
    3. Klik tombol hitung untuk melihat hasil
    """)

# =============== HALAMAN MODEL BARU ===============
elif st.session_state.current_page == "Model Baru":
    st.title("🆕 Model Baru")
    st.warning("Fitur dalam pengembangan! Silakan kontribusi kode Anda.")
    
    tab1, tab2 = st.tabs(["📝 Formulir", "📊 Visualisasi"])
    
    with tab1:
        st.subheader("Parameter Model")
        model_type = st.selectbox(
            "Jenis Model", 
            ["Transportasi", "Proyek (CPM/PERT)", "Forecasting"]
        )
        
        if model_type == "Transportasi":
            st.number_input("Jumlah Sumber", 1, 10, 3)
            st.number_input("Jumlah Tujuan", 1, 10, 4)
        
        elif model_type == "Proyek (CPM/PERT)":
            st.number_input("Jumlah Aktivitas", 1, 50, 10)
        
        elif model_type == "Forecasting":
            st.selectbox("Metode", ["Moving Average", "Exponential Smoothing"])
    
    with tab2:
        st.subheader("Preview Visualisasi")
        if model_type == "Transportasi":
            st.image("https://via.placeholder.com/600x300?text=Diagram+Transportasi", use_column_width=True)
        elif model_type == "Proyek (CPM/PERT)":
            st.image("https://via.placeholder.com/600x300?text=Diagram+Jaringan", use_column_width=True)
        else:
            st.line_chart(np.random.randn(20, 1))

# =============== HALAMAN OPTIMASI PRODUKSI ===============
elif st.session_state.current_page == "Optimasi":
    st.title("📈 OPTIMASI PRODUKSI")
    
    # ... (kode optimasi produksi sebelumnya tetap sama)
    # Pastikan untuk menyalin bagian ini dari kode asli Anda

# =============== HALAMAN EOQ ===============
elif st.session_state.current_page == "EOQ":
    st.title("📦 MODEL PERSEDIAAN (EOQ)")
    
    # ... (kode EOQ sebelumnya tetap sama)

# =============== HALAMAN ANTRIAN ===============
elif st.session_state.current_page == "Antrian":
    st.title("🔄 MODEL ANTRIAN (M/M/1)")
    
    # ... (kode antrian sebelumnya tetap sama)

# =============== HALAMAN JOHNSON ===============
elif st.session_state.current_page == "Johnson":
    st.title("⏱ PENJADWALAN DENGAN JOHNSON'S RULE")
    
    # ... (kode Johnson's Rule sebelumnya tetap sama)

# =============== STYLE CUSTOM ===============
st.markdown("""
<style>
    .stButton>button {
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .st-emotion-cache-1qg05tj {
        font-family: "Arial", sans-serif;
    }
</style>
""", unsafe_allow_html=True)
