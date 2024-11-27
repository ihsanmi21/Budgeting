import streamlit as st
import pandas as pd

# Fungsi untuk memformat angka ke format Rupiah secara manual
def format_rupiah(amount):
    """Mengubah angka menjadi format Rupiah dengan titik sebagai pemisah ribuan."""
    amount_str = f"{int(amount):,}"  # Format angka dengan ribuan
    return f"Rp {amount_str.replace(',', '.')}"

# Fungsi untuk memproses input secara real-time dan mengubahnya menjadi format Rupiah
def process_and_format_input():
    """Memproses input dari pengguna dan memperbarui input dengan format Rupiah."""
    input_amount = st.session_state["input_amount"]  # Ambil input dari pengguna
    input_amount = input_amount.replace(".", "")  # Hilangkan titik pemisah ribuan sebelumnya
    
    if input_amount.isdigit():  # Periksa apakah input valid (hanya angka)
        formatted_amount = format_rupiah(input_amount)
        st.session_state["input_amount"] = formatted_amount  # Perbarui input dengan format Rupiah
    elif input_amount == "":
        st.session_state["input_amount"] = ""
    else:
        st.warning("Please enter only numeric values.")

# Inisialisasi transaksi di memori
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = pd.DataFrame(columns=['Category', 'Amount', 'Date', 'Type'])

# Langkah 1: Pilih jenis transaksi (Income/Expense)
transaction_type = st.radio("Select the type of transaction", ['Income', 'Expense'])

# Langkah 2: Pilih kategori transaksi
if transaction_type == 'Income':
    categories = ['Salary', 'Bonus', 'Investment', 'Other']
else:
    categories = ['Rent', 'Groceries', 'Utilities', 'Entertainment', 'Other']
category = st.selectbox('Select the category', categories)

# Langkah 3: Input jumlah dengan format Rupiah secara otomatis
st.text_input(
    'Amount (Rupiah)',
    value="0" if "input_amount" not in st.session_state else st.session_state["input_amount"],
    key="input_amount",
    on_change=process_and_format_input
)

# Langkah 4: Pilih tanggal transaksi
date = st.date_input('Date')

# Langkah 5: Tombol untuk menambahkan transaksi
if st.button('Add Transaction'):
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
    st.write("Your Transactions:")

    # Tampilkan tabel transaksi dengan jumlah dalam format Rupiah dan kolom rata tengah
    formatted_transactions = transactions.copy()
    formatted_transactions['Amount'] = formatted_transactions['Amount'].apply(format_rupiah)

    # Menampilkan DataFrame di Streamlit dengan kolom rata tengah
    st.dataframe(
        formatted_transactions.style.set_properties(
            **{'text-align': 'center'}
        ).set_table_styles(
            [{'selector': 'th', 'props': [('text-align', 'center')]}]
        )
    )

# Menghitung total pendapatan dan pengeluaran
total_income = transactions[transactions['Type'] == 'Income']['Amount'].sum()
total_expenses = transactions[transactions['Type'] == 'Expense']['Amount'].sum()

# Menampilkan informasi saldo
balance = total_income - total_expenses
st.write(f"Total Income: {format_rupiah(total_income)}")
st.write(f"Total Expenses: {format_rupiah(total_expenses)}")
st.write(f"Remaining Balance: {format_rupiah(balance)}")
