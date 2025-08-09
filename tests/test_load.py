import pandas as pd
from utils import load
import os

def test_load_to_postgre(monkeypatch):
    df = pd.DataFrame([{"Title": "A"}])
    class DummyEngine:
        def connect(self): return self
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass
    monkeypatch.setattr("sqlalchemy.create_engine", lambda url: DummyEngine())
    monkeypatch.setattr(df, "to_sql", lambda *a, **k: None)
    load.load_to_postgre(df, "postgresql://user:pass@localhost/db")

def test_save_to_csv(tmp_path):
    df = pd.DataFrame([{"Title": "A"}])
    file_path = tmp_path / "test.csv"

    load.save_to_csv(df, str(file_path))
    
    # Cek file tercipta dan isinya benar
    assert os.path.exists(file_path)
    df_loaded = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df, df_loaded)
