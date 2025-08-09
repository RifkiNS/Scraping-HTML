import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils import extract
import pandas as pd


def test_fetching_content_success():
    with patch("requests.Session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<html></html>"
        mock_get.return_value = mock_response
        result = extract.fetching_content("http://example.com")
        assert result == b"<html></html>"

def test_fetching_content_failure():
    with patch("requests.Session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("error")
        mock_get.return_value = mock_response
        result = extract.fetching_content("http://example.com")
        assert result is None

def test_extract_fashion_data_complete():
    html = '''
    <div>
        <h3 class="product-title">Test Product</h3>
        <span class="price">$100</span>
        <p style="font-size: 14px; color: #777;">Rating: 4.5 / 5</p>
        <p style="font-size: 14px; color: #777;">Red Colors</p>
        <p style="font-size: 14px; color: #777;">Size: XL</p>
        <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
    </div>
    '''
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div")
    data = extract.extract_fashion_data(div)
    assert data["Title"] == "Test Product"
    assert data["Price"] == "$100"
    assert data["Rating"] == "4.5"
    assert data["Colors"] == "Red"
    assert data["Size"] == "XL"
    assert data["Gender"] == "Unisex"
    assert "Timestamp" in data

def test_extract_fashion_data_missing_fields():
    html = '<div></div>'
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div")
    data = extract.extract_fashion_data(div)
    assert data["Title"] is None
    assert data["Price"] is None
    assert data["Rating"] is None
    assert data["Colors"] is None
    assert data["Size"] is None
    assert data["Gender"] is None

def test_next_page_found():
    html = '''
    <ul>
        <li class="page-item next">
            <a class="page-link" href="/page2"></a>
        </li>
    </ul>
    '''
    soup = BeautifulSoup(html, "html.parser")
    url = extract.next_page(soup, "http://baseurl.com/")
    assert url == "http://baseurl.com/page2"

def test_next_page_not_found():
    html = '<ul></ul>'
    soup = BeautifulSoup(html, "html.parser")
    url = extract.next_page(soup, "http://baseurl.com/")
    assert url is None

def test_scrape_data_empty(monkeypatch):
    def fake_fetching_content(url):
        return None
    monkeypatch.setattr(extract, "fetching_content", fake_fetching_content)
    result = extract.scrape_data("http://baseurl.com")
    assert result == []

def test_scrape_data_one_page(monkeypatch):
    html = '''
    <div class="collection-card">
        <h3 class="product-title">Test Product</h3>
        <span class="price">$100</span>
        <p style="font-size: 14px; color: #777;">Rating: 4.5 / 5</p>
        <p style="font-size: 14px; color: #777;">Red Colors</p>
        <p style="font-size: 14px; color: #777;">Size: XL</p>
        <p style="font-size: 14px; color: #777;">Gender: Unisex</p>
    </div>
    '''
    def fake_fetching_content(url):
        return html.encode()
    def fake_next_page(soup, base_url):
        return None
    monkeypatch.setattr(extract, "fetching_content", fake_fetching_content)
    monkeypatch.setattr(extract, "next_page", fake_next_page)
    result = extract.scrape_data("http://baseurl.com")
    assert isinstance(result, list)
    assert result[0]["Title"] == "Test Product"

