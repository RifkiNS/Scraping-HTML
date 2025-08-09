from utils import load, transform, extract

def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev'
    EXCHANGE_RATE = 16000
    DB_URL = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashionsdb'
    CSV_PATH = 'fashion_data.csv'

    all_data = extract.scrape_data(BASE_URL, start_page=1)
    if all_data:
        try:
            df = transform.transform_to_DataFrame(all_data)
            df = transform.transform_data(df, EXCHANGE_RATE)
            # Panggil fungsi load untuk simpan ke CSV dan database
            load.save_to_csv(df, CSV_PATH)
            load.load_to_postgre(df, DB_URL)
        except Exception as e:
            print(f"Terjadi kesalahan dalam proses: {e}")
    else:
        print("Tidak ada data yang berhasil di-scrape.")

if __name__ == '__main__':
    main()