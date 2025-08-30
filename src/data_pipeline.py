import pandas as pd
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def load_dataset(file_path):
    encoding = detect_encoding(file_path)
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding=encoding)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    except Exception as e:
        raise ValueError(f"Error loading dataset: {e}")
    return df

def load_and_validate_csv(file, max_size_mb=5):
    """
    Load CSV with validation:
    - File type
    - Encoding
    - Size
    """
    # Check file size
    file.seek(0, 2)  # move to end
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    if size_mb > max_size_mb:
        raise ValueError(f"File is too large ({size_mb:.2f} MB), max {max_size_mb} MB allowed.")

    # Detect encoding
    encoding = detect_encoding(file)

    # Load CSV
    try:
        df = pd.read_csv(file, encoding=encoding)
    except Exception as e:
        raise ValueError(f"Cannot read CSV: {e}")

    if df.empty:
        raise ValueError("CSV is empty")

    return df