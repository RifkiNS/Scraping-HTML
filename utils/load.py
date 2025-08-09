from sqlalchemy import create_engine


def load_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL"""
    try:
        # Membuat engine database
        engine = create_engine(db_url)

        # Menyimpan data ke tabel 'fashiontoscrape' jika tabel sudah ada, data akan ditambahkan
        with engine.connect() as con:
            data.to_sql('fashiontoscrape', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan!")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")

def save_to_csv(data, file_path):
    try:
        data.to_csv(file_path, index=False)
        print("Data berhasil disimpan ke CSV!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")

    

    