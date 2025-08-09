import time
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan"""
    session = requests.Session()
    
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None
    
def extract_fashion_data(div):
    """Mengambil data fashion berupa title, rating, colors, price, size dan gender dari URL"""
    # Inisialisasi semua variabel dengan None
    title = None
    price = None
    rating = None
    colors = None
    size = None
    gender = None

    # Ekstraksi Title
    title_element = div.find('h3', class_="product-title")
    if title_element:
        title = title_element.text.strip()
    
    # Ekstraksi Price
    price_element = div.find('span', class_="price")
    if price_element:
        price = price_element.text.strip()

    # Ekstraksi Rating, Colors, Size, Gender dari elemen <p>

    p_tags = div.find_all('p', style="font-size: 14px; color: #777;")
    for p_tag in p_tags:
        text = p_tag.text.strip()
        if "Rating:" in text:
            # Mengambil rating berupa angka
            match = re.search(r'Rating:.*?(\d+\.?\d*)\s*/\s*5', text)
            rating = match.group(1) if match else "Invalid Rating"
        elif "Colors" in text: # Mengambil data warna dengan menghilangkan " Colors"
            colors = text.replace(" Colors", "").strip()
        elif "Size:" in text: # Mengambil data ukuran dengan menghilangkan "Size:"
            size = text.replace("Size:", "").strip()
        elif "Gender:" in text: # Mengambil data jenis kelamin dengan menghilangkan "Gender:"
            gender = text.replace("Gender:", "").strip()

    # Menambahkan timestamp saat data ini diekstrak
    extraction_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Mengembalikan data title, price, rating, color, size dan gender dengan menambahkan kolom baru timestamp
    return {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
        "Timestamp": extraction_timestamp # Kolom baru
    }
def next_page(soup, base_url):
    """Fungsi untuk mengambil data dinext page"""
    next_button = soup.find('li', class_="page-item next")
    if next_button:
        next_button = next_button.find('a', class_="page-link")
        if next_button and "href" in next_button.attrs:
            relative_path = next_button['href']
            clean_base_url = base_url.rstrip('/')
            return f"{clean_base_url}{relative_path}"
    return None
            

def scrape_data(base_url, start_page=1, delay=2):
    """Fungsi untuk mengambil seluruh data dari URL dan menyimpannya"""
    all_products_data = []
    
    # Inisialisasi URL halaman pertama
    # Jika start_page > 1, kita asumsikan formatnya '/pageX'
    if start_page == 1:
        current_page_url = base_url # Asumsi halaman 1 adalah base_url itu sendiri
    else:
        current_page_url = f"{base_url}/page{start_page}"


    while current_page_url:
        print(f'Scraping Halaman: {current_page_url}')

        content = fetching_content(current_page_url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            
            product_div_elements = soup.find_all('div', class_='collection-card')
            
            if not product_div_elements:
                print("Tidak ada produk ditemukan di halaman ini. Menghentikan scraping.")
                break

            for product_div in product_div_elements:
                product_details = extract_fashion_data(product_div)
                all_products_data.append(product_details)

            # Dapatkan URL halaman berikutnya menggunakan fungsi manual
            next_page_url = next_page(soup, base_url)

            if next_page_url and next_page_url != current_page_url:
                current_page_url = next_page_url
                time.sleep(delay)
            else:
                print("Tidak ada halaman 'Next' yang ditemukan atau sudah mencapai akhir pagination.")
                break

        else:
            print("Konten tidak dapat diambil. Menghentikan scraping.")
            break

    return all_products_data