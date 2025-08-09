from utils import transform
import pandas as pd
import numpy as np

def test_transform_to_DataFrame():
    data = [
        {"Title": "A", "Price": "$100", "Rating": "4", "Colors": "1", "Size": "M", "Gender": "Male", "Timestamp": "2024-01-01 00:00:00"}
    ]
    df = transform.transform_to_DataFrame(data)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Title" in df.columns

def test_transform_data_valid():
    df = pd.DataFrame([
        {"Title": "A", "Price": "$100", "Rating": "4.5", "Colors": "2", "Size": "M", "Gender": "Male", "Timestamp": "2024-01-01 00:00:00"}
    ])
    kurs = 15000
    result = transform.transform_data(df, kurs)
    assert not result.empty
    assert result["Price"].iloc[0] == 100 * kurs
    assert isinstance(result["Rating"].iloc[0], float)
    assert isinstance(result["Colors"].iloc[0], (int, np.integer))
    assert pd.api.types.is_datetime64_any_dtype(result["Timestamp"])

def test_transform_data_invalid_price():
    df = pd.DataFrame([
        {"Title": "A", "Price": "invalid", "Rating": "4.5", "Colors": "2", "Size": "M", "Gender": "Male", "Timestamp": "2024-01-01 00:00:00"}
    ])
    kurs = 15000
    result = transform.transform_data(df, kurs)
    # Baris dengan Price invalid akan di-drop
    assert result.empty

def test_transform_data_invalid_rating_and_title():
    df = pd.DataFrame([
        {"Title": "Unknown Product", "Price": "$100", "Rating": "Invalid Rating", "Colors": "2", "Size": "M", "Gender": "Male", "Timestamp": "2024-01-01 00:00:00"}
    ])
    kurs = 15000
    result = transform.transform_data(df, kurs)
    # Baris dengan Title 'Unknown Product' dan Rating 'Invalid Rating' akan