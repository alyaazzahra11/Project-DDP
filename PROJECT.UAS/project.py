import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

from datetime import datetime, timedelta
from streamlit_option_menu import option_menu


# Judul Aplikasi
st.set_page_config(page_title="Aplikasi Kalkulator Keuangan Pribadi", page_icon="💵", layout="wide")

# CSS
st.markdown(
    """
    <style>
    /* Warna latar belakang aplikasi */
    .stApp{
        background-color: #D9EAFD;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #9AA6B2;
        color: white;
        padding: 5px;
        widht: 400px;
    }

    .sidebar{
    width: 500px;
    }
   
    /* Tabel styling */
    .dataframe {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }

    /* Teks styling */
    h2{
        text-align: center;
    }

    .stMarkdown{
        text-align: justify;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Fungsi untuk memuat data dari CSV
def load_data(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=["Tanggal", "Kategori", "Jenis", "Jumlah", "Keterangan"])

def load_budget(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=["Kategori","Periode", "Jenis", "Anggaran", "Pengeluaran", "Sisa anggaran"])

# Fungsi untuk menyimpan data ke CSV
def save_data(data, file):                  #menyimpan data ke keuangan csv
    data.to_csv(file, index=False)

def save_budget(budget, file):              #menyimpan data ke anggaran csv
    budget.to_csv(file, index=False)

# file untuk menyimpan data
data_file = "data_keuangan.csv"
budget_file = "anggaran.csv"

# fungsi st.session_state untuk memanggil data dari fitur lain ke fitur lainnya 
if "jumlah" not in st.session_state:
    st.session_state["jumlah"] = 0
if "anggaran" not in st.session_state:
    st.session_state["anggaran"] = 0
if "total_anggaran" not in st.session_state:
    st.session_state["total_anggaran"] = 0
if "total_pengeluaran" not in st.session_state:
    st.session_state["total_pengeluaran"] = 0
if "sisa_anggaran" not in st.session_state:
    st.session_state["sisa_anggaran"] = 0

# Load data transaksi dan anggaran
data = load_data(data_file)
budget = load_budget(budget_file)

# Menu navigasi
with st.sidebar:
     selected = option_menu("Pilih Menu", 
                         ["Home", 
                          "Transaksi",
                          "Anggaran",
                          "Ringkasan Keuangan",
                          "Grafik Pengeluaran",
                          "Tentang Kami"],
                          icons= ["house", "plus", "tags", "",  "circle", "info"],
                          default_index=0,
                          styles={"container": {"background-color": "#F8FAFC"},
                                 "icon": {"color": "white", "font-size": "15px"},
                                 "nav-link": {"font-size": "14px", "text-align": "left"}})
    
# Beranda depan
if selected == "Home":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("keuangan.jpg", width=700)
    
    st.header ("Selamat Datang di Aplikasi Kalkulator Keuangan Pribadi")
    st.write ("Aplikasi Kalkulator Keuangan Pribadi ini memudahkan anda untuk mengelola keuangan dengan lebih efisien.")
    st.markdown ("""
                Fitur yang anda dapatkan dalam aplikasi:
                - **Transaksi**: untuk menginput pengeluaran yang telah dilakukan. \n
                - **Ringkasan Keuangan**: memuat ringkasan juga riwayat keuangan yang telah di input pada menu transaksi.\n
                - **Anggaran**: untuk mengatur anggaran setiap jenis pengeluaran yang dilakukan.\n
                - **Grafik Pengeluaran**: memuat grafik diagram pengeluaran.\n
                """)
    st.markdown ("""<h3 style="text-align: center;">"Hidup lebih terkendali dengan perencanaan keuangan"</h3>""", unsafe_allow_html=True)


# Tambah Transaksi
elif selected == "Transaksi":
    st.header("Tambahkan Transaksi")

    # Form input transaksi
    tanggal = st.date_input("Tanggal")
    kategori = st.radio("Kategori", ["Pengeluaran", "Tabungan"])
    jenis = st.selectbox("Jenis", ["🍔 Makanan", "🚍 Transportasi", "🎮 Hiburan", "🤝 Sosial", "💰 Tabungan", "📦 Lainnya"])
    jumlah = st.number_input("Jumlah", min_value=0, step=1000)
    keterangan = st.text_input("Keterangan")

    if st.button("Simpan"):
        kolom_data = {"Tanggal": tanggal, "Kategori": kategori, "Jenis": jenis, "Jumlah": jumlah, "Keterangan": keterangan}              #untuk menyimpan data ke keuangan.csv
        data = pd.concat([data, pd.DataFrame([kolom_data])], ignore_index=True)
        save_data(data, data_file)

        if kategori == "Pengeluaran":
            anggaran_pengeluaran = budget[(budget["Kategori"] == kategori) & (budget["Jenis"] == jenis)].index
            if not anggaran_pengeluaran.empty:
                budget.loc[anggaran_pengeluaran, "Pengeluaran"] += jumlah
                budget.loc[anggaran_pengeluaran, "Sisa anggaran"] = budget.loc[anggaran_pengeluaran, "Anggaran"] - budget.loc[anggaran_pengeluaran, "Pengeluaran"]
                save_budget(budget, budget_file)

                # mengambil sisa anggaran yang terlah tersimpan
                sisa_anggaran = budget.loc[anggaran_pengeluaran, "Sisa anggaran"].values[0]

                if budget.loc[anggaran_pengeluaran, "Anggaran"].values[0] < 0:
                    st.success(f"{kategori} dengan jenis {jenis} berhasil disimpan!")
                elif budget.loc[anggaran_pengeluaran, "Sisa anggaran"].values[0] >= 0:
                    st.success(f"{kategori} {jenis} berhasil ditambahkan, sisa anggaran anda {sisa_anggaran}")
                else:
                    st.error(f"{kategori} {jenis} melebihi anggaran yang disediakan!")
            else:
                st.success(f"{kategori} dengan jenis {jenis} berhasil disimpan!")


# Fitur Anggaran
elif selected == "Anggaran":
    st.header("Anggaran Bulanan")

    kategori = st.radio("Kategori", ["Pengeluaran", "Tabungan"])
    jenis = st.selectbox("Jenis", ["🍔 Makanan", "🚍 Transportasi", "🎮 Hiburan", "🤝 Sosial", "💰 Tabungan", "📦 Lainnya"])
    periode = "Bulanan"
    anggaran = st.number_input("Jumlah", min_value=0, step=1000)

    if st.button("Simpan Anggaran"):
        anggaran_pengeluaran = budget[(budget["Kategori"] == kategori) & (budget["Jenis"] == jenis)].index
        if not anggaran_pengeluaran.empty:
            budget.loc[anggaran_pengeluaran, "Anggaran"] = anggaran
            budget.loc[anggaran_pengeluaran, "Sisa anggaran"] = anggaran - budget.loc[anggaran_pengeluaran, "Pengeluaran"]
        else:
            new_budget = {"Kategori": kategori, "Periode": periode, "Jenis": jenis, "Anggaran": anggaran, "Pengeluaran": 0, "Sisa anggaran": anggaran}
            budget = pd.concat([budget, pd.DataFrame([new_budget])], ignore_index=True)

        save_budget(budget, budget_file)
        st.success(f"Anggaran dengan jenis {jenis} berhasil disimpan!")

        if jenis != "Semua":
            st.metric("Total Anggaran untuk", f"{jenis} : Rp. {anggaran}")
        else:
            st.warning("Tidak ada anggaran yang disiapkan")

    # data anggaran
    st.dataframe(budget)

    # Meriset data anggaran
    if st.button("Reset anggaran"):
        budget = pd.DataFrame(columns=["Kategori", "Periode", "Jenis", "Anggaran", "Pengeluaran", "Sisa anggaran"])
        save_budget(budget, budget_file)
        st.success("Anggaran berhasil direset! Silahkan refresh ulang")
            

# Fitur Ringkasan Keuangan
elif selected == "Ringkasan Keuangan":
    st.header("Ringkasan Keuangan")
    
    # Total pemasukan, pengeluaran, tabungan
    if not data.empty:
        total_tabungan = data[data["Kategori"] == "Tabungan"]["Jumlah"].sum()
        total_anggaran = data[data["Kategori"] == "Anggaran"]["Jumlah"].sum()
        total_pengeluaran = data[data["Kategori"] == "Pengeluaran"]["Jumlah"].sum()
        sisa_anggaran = total_anggaran - total_pengeluaran

        st.metric("Total Tabungan", f"Rp. {total_tabungan}")
        st.metric("Total Pengeluaran", f"Rp. {total_pengeluaran}")
    else:
        st.warning("Belum ada data transaksi yang tersedia.")

    # Melihat riwayat transaksi
    st.subheader("Riwayat Transaksi")

    # Filter Kategori
    filter_jenis = st.selectbox("Jenis", ["Semua", "🍔 Makanan", "🚍 Transportasi", "🎮 Hiburan", "🤝 Sosial", "💰 Tabungan", "📦 Lainnya"])
    if filter_jenis != "Semua":
        data_filtered = data[data["Jenis"] == filter_jenis]
        st.dataframe(data_filtered)
    else:
        st.dataframe(data)

        # Meriset data anggaran
        if st.button("Reset Data"):
            data = pd.DataFrame(columns=["Tanggal", "Kategori", "Jenis", "Jumlah", "Keterangan"])
            save_data(data, data_file)
            st.success("Data berhasil direset! Silahkan refresh ulang")


# Fitur Grafik Pengeluaran
elif selected == "Grafik Pengeluaran":
    st.header("Grafik Pengeluaran per Kategori")

    if not data.empty:
        pengeluaran_data = data[data["Kategori"] == "Pengeluaran"]
        if not pengeluaran_data.empty:
            kategori_group = pengeluaran_data.groupby("Jenis")["Jumlah"].sum()
            kategori_persen = (kategori_group / kategori_group.sum()) * 100

            # warna dalam diagram
            colors = ["#4C585B", "#7E99A3", "#A5BFCC", "#ECEBDE", "#D8D2C2", "#A59D84"]

            # Plot diagram lingkaran
            fig, ax = plt.subplots(figsize=(5,4))
            fig.patch.set_facecolor("#D9EAF7")
            ax.pie(kategori_persen, labels=kategori_persen.index, autopct="%1.1f%%", startangle=90, colors=colors)
            ax.axis("equal")  # Equal untuk memastikan diagram lingkaran berbentuk bulat
            st.pyplot(fig)

            # Keterangan jumlah perjenis
            data_grafik = pd.DataFrame({
                "Total" : kategori_group,
                "Persentase (%)" : kategori_persen.map(lambda i: f"{i:.2f}%")  #untuk mengubah format kedalam persen
            })
            st.table(data_grafik)
    else:
        st.warning("Tidak ada data pengeluaran untuk ditampilkan.")


elif selected == "Tentang Kami":
    st.header("Tentang Kami")
    st.markdown("""
                **Aplikasi Kalkulator Keuangan Pribadi** adalah aplikasi web yang dibuat oleh mahasiswa semester satu Sistem Informasi untuk memudahkan anda dalam mengatur keuangan pribadi.
                Aplikasi ini dibuat untuk membantu orang-orang agar bisa mengatur keuangan secara efisien.
                """)
    
    st.subheader("Latar Belakang")
    st.markdown("""
                Banyaknya orang yang mulai sadar akan finansial tetapi kesulitan dalam mengatur keuangan membuat kita tertarik untuk membuat Aplikasi Keuangan Pribadi ini. 
                Dengan perkembangan teknologi di era digital ini, aplikasi berbasis web yang praktis menjadi solusi dalam mengelola keuangan secara mudah dan efisien.
                Aplikasi Kalkulator Keuangan Pribadi dirancang untuk memberikan layanan yang lebih baik dan memudahkan pengguna dalam mengatur keuangan.
                """)

    st.subheader("Manfaat Aplikasi")
    st.markdown ("""
                Manfaat yang didapatkan dari aplikasi ini, diantaranya:
                - Memantau pengeluaran anda: aplikasi ini memudahkan anda dalam memonitor pengeluran yang sudah ada lakukan\n
                - Memudahkan pengelolaan keuangan: aplikasi ini mempermudah anda untuk membuat anggaran, mencatat pengeluaran, juga memantau sisa anggaran yang telah dibuat dalam kurun waktu satu bulan\n
                - Mengontrol pengeluaran dengan anggaran yang disediakan: dengan adanya anggaran, anda dapat lebih mengatur keuangan dengan lebih baik\n
                - Meningkatkan kesadaran finansial: dengan menggunakan aplikasi ini, anda dapat lebih sadar akan pengeluaran yang perlu dilakukan dengan pengeluaran yang tidak perlu dilakukan\n
                """)
    
    st.subheader("Our Team")
    st.markdown ("""
                **Aplikasi Kalkulkator Keuangan Pribadi** dibuat dalam rangka memenuhi tugas project untuk UAS mata kuliah Dasar-Dasar Pemprograman semester satu. 
                 Aplikasi ini dibuat oleh:
                 - **Alya Az-Zahra**
                 - **Hilwah Qurrotul Aini**
                 - **Naylla Agustina Putria**
                 - **Syafiq Alwan Syauqi**
                 """)
