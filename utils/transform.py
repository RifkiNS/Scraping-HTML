import pandas as pd

def transform_to_DataFrame(data):
    """Memrubah data hasil scraping menjadi DataFrame"""
    df = pd.DataFrame(data)
    return df

def transform_data(data, exchange_rate):
    
    # Price Transform
    # Langkah 1: Pastikan kolom 'Price' bertipe string agar operasi string bisa dilakukan
    data['Price'] = data['Price'].astype(str)

    data['Price'] = data['Price'].str.replace(',', '', regex=False) # Hapus koma ribuan
    
    # Hapus semua karakter yang bukan digit, bukan titik desimal, dan bukan tanda minus di awal
    # Ini akan menghapus '$', '£', 'Rp', 'USD', '€', spasi, dll.
    data['Price'] = data['Price'].str.replace(r'[^\d.-]', '', regex=True) 

    # Konversi ke numerik. String yang tidak bisa diubah akan menjadi NaN
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
    
    # Drop baris di mana 'Price' menjadi NaN (yang berarti itu adalah string non-valid)
    initial_rows = len(data)
    data = data.dropna(subset=['Price']).copy()
    print(f"Jumlah baris yang dihapus karena 'Price' non-valid: {initial_rows - len(data)}")
    
    try:
        data['Price'] = (data['Price'] * exchange_rate).astype(float) # Mengubah mata uang ke IDR
    
    except Exception as e:
        print(f"Terjadi kesalahan dalam proses: {e}")
    
    # Drop data duplikat
    data = data.drop_duplicates()

    # Drop missing value
    data = data.dropna()

    # Drop nilai invalid
    data = data[data['Title'] != 'Unknown Product']
    data = data[data['Rating'] != 'Invalid Rating']

    # Merubah format data
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce')
    data['Rating'] = data['Rating'].astype(float)
    data['Colors'] = data['Colors'].astype(int)
    return data

