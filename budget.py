import streamlit as st
import pandas as pd
import io

# Fungsi untuk memformat angka ke format Rupiah
def format_rupiah(amount):
    """Mengubah angka menjadi format Rupiah dengan titik sebagai pemisah ribuan."""
    amount_str = f"{int(amount):,}"  # Format angka dengan ribuan
    return f"Rp {amount_str.replace(',', '.')}"

# Fungsi untuk memproses input saat diketik
def process_input():
    """Memproses input dari pengguna untuk format langsung."""
    input_amount = st.session_state["input_amount"]  # Ambil input dari pengguna
    raw_amount = input_amount.replace(".", "").replace("Rp ", "")  # Hilangkan titik dan simbol Rp
    
    if raw_amount.isdigit():  # Periksa apakah input valid (hanya angka)
        formatted_amount = format_rupiah(int(raw_amount))
        st.session_state["input_amount"] = formatted_amount  # Tampilkan input dalam format Rupiah

# Fungsi untuk memuat data CSV
def load_csv(file):
    """Memuat file CSV dan mengonversinya ke DataFrame."""
    try:
        df = pd.read_csv(file)

        # Pastikan kolom Amount diubah menjadi angka tanpa simbol Rp dan titik pemisah ribuan
        if 'Amount' in df.columns:
            df['Amount'] = df['Amount'].replace({r'Rp\s*': '', r'\.': ''}, regex=True)
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

        st.session_state['transactions'] = df
        st.success("CSV file loaded successfully!")
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")

# Inisialisasi transaksi di memori jika belum ada
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = pd.DataFrame(columns=['Category', 'Amount', 'Date', 'Type'])

# **Tampilan yang lebih menarik**
st.set_page_config(page_title="Transaction Tracker", layout="wide", page_icon="💰")

# Menampilkan Judul dan Pengantar
st.title("💰 Transaction Tracker")
st.markdown("""
Welcome to the Transaction Tracker JamilJamblungz!  
This tool helps you record, track, and manage your income and expenses in an easy-to-use format.  
Upload your transactions, or add new ones manually, and see your financial overview in real-time.
""")

# Langkah 1: Upload CSV file
uploaded_file = st.file_uploader("Upload your transactions CSV", type=["csv"])

if uploaded_file is not None:
    load_csv(uploaded_file)

# **Desain layout menggunakan kolom**
col1, col2 = st.columns(2)

with col1:
    # Langkah 2: Pilih jenis transaksi (Income/Expense)
    transaction_type = st.radio("Select the type of transaction", ['Income', 'Expense'])

with col2:
    # Langkah 3: Pilih kategori transaksi
    if transaction_type == 'Income':
        categories = ['Salary', 'Bonus', 'Investment', 'Other']
    else:
        categories = ['Rent', 'Groceries', 'Utilities', 'Entertainment', 'Other']
    category = st.selectbox('Select the category', categories)

# **Langkah 4**: Input jumlah dengan format Rupiah secara otomatis
st.text_input(
    'Amount (Rupiah)',
    value="Rp 0" if "input_amount" not in st.session_state else st.session_state["input_amount"],
    key="input_amount",
    on_change=process_input,
    label_visibility="collapsed"
)

# **Langkah 5**: Pilih tanggal transaksi
date = st.date_input('Date')

# **Langkah 6**: Tombol untuk menambahkan transaksi
if st.button('Add Transaction 📝'):
    # Konversi jumlah dari format Rupiah kembali ke angka
    try:
        final_amount = int(st.session_state["input_amount"].replace("Rp ", "").replace(".", ""))
        if final_amount > 0:
            new_transaction = pd.DataFrame({
                'Category': [category],
                'Amount': [final_amount],
                'Date': [date],
                'Type': [transaction_type]
            })
            st.session_state['transactions'] = pd.concat([st.session_state['transactions'], new_transaction], ignore_index=True)
            st.success("Transaction Added Successfully!")
            st.balloons()
    except ValueError:
        st.error("Please enter a valid amount!")

# Menampilkan transaksi yang sudah ditambahkan dengan pemformatan tabel lebih rapi
transactions = st.session_state['transactions']
if not transactions.empty:
    st.write("### Your Transactions:")

    # Tampilkan tabel transaksi dengan jumlah dalam format Rupiah dan kolom rata tengah
    formatted_transactions = transactions.copy()
    formatted_transactions['Amount'] = formatted_transactions['Amount'].apply(format_rupiah)

    # Menampilkan DataFrame di Streamlit dengan kolom rata tengah dan desain tabel lebih rapih
    st.dataframe(
        formatted_transactions.style.set_properties(
            **{'text-align': 'center'}
        )
    )

    # Fitur untuk mengunduh tabel transaksi dalam format CSV
    def convert_df(df):
        """Konversi DataFrame ke CSV."""
        return df.to_csv(index=False)

    csv = convert_df(formatted_transactions)

    # Tombol untuk mengunduh CSV
    st.download_button(
        label="Download Transactions as CSV 📥",
        data=csv,
        file_name='transactions.csv',
        mime='text/csv',
        use_container_width=True
    )

# Menghitung total pendapatan dan pengeluaran
total_income = transactions[transactions['Type'] == 'Income']['Amount'].sum()
total_expenses = transactions[transactions['Type'] == 'Expense']['Amount'].sum()

# Menampilkan informasi saldo dengan desain yang lebih menarik
balance = total_income - total_expenses
st.markdown(f"### **Total Income**: {format_rupiah(total_income)}")
st.markdown(f"### **Total Expenses**: {format_rupiah(total_expenses)}")
st.markdown(f"### **Remaining Balance**: {format_rupiah(balance)}")

# Informasi tambahan
st.markdown("""
---
For further assistance, please contact our support team at **jamiljamblung@gmail.com**.
""")
