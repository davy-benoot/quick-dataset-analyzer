import io
import pandas as pd
import pytest
import tempfile
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_pipeline import detect_encoding, load_dataset, load_and_validate_csv

def test_detect_encoding_with_path(tmp_path):
    # Create a temp file with known encoding
    test_file = tmp_path / "test.csv"
    test_file.write_text("name,age\nJohn,30\nJane,25", encoding='utf-8')
    encoding = detect_encoding(str(test_file))
    assert encoding in ['utf-8', 'UTF-8', 'ascii']

def test_detect_encoding_with_file_object():
    data = b"name,age\nJohn,30\nJane,25"
    file_obj = io.BytesIO(data)
    encoding = detect_encoding(file_obj)
    assert encoding in ['utf-8', 'UTF-8', 'ascii']

def test_load_dataset_valid_csv(tmp_path):
    test_file = tmp_path / "test.csv"
    test_file.write_text("name,age\nJohn,30\nJane,25", encoding='utf-8')
    df = load_dataset(str(test_file))
    assert not df.empty
    assert list(df.columns) == ['name', 'age']
    assert len(df) == 2

def test_load_dataset_invalid_format(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("some text")
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_dataset(str(test_file))

def test_load_and_validate_csv_valid():
    data = b"name,age\nJohn,30\nJane,25"
    file_obj = io.BytesIO(data)
    df = load_and_validate_csv(file_obj)
    assert not df.empty
    assert list(df.columns) == ['name', 'age']
    assert len(df) == 2

def test_load_and_validate_csv_too_large():
    # Create large data > 5MB
    large_data = b"a,b\n" + b"1,2\n" * 2000000  # approx 10MB
    file_obj = io.BytesIO(large_data)
    with pytest.raises(ValueError, match="File is too large"):
        load_and_validate_csv(file_obj)

def test_load_and_validate_csv_empty():
    data = b"name,age\n"
    file_obj = io.BytesIO(data)
    with pytest.raises(ValueError, match="CSV is empty"):
        load_and_validate_csv(file_obj)

def test_load_and_validate_csv_invalid_csv():
    data = b""  # Empty data causes pd.read_csv to raise EmptyDataError
    file_obj = io.BytesIO(data)
    with pytest.raises(ValueError, match="Cannot read CSV"):
        load_and_validate_csv(file_obj)
