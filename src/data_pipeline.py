import pandas as pd
import chardet

def detect_encoding(file_or_path):
    if isinstance(file_or_path, str):
        with open(file_or_path, 'rb') as f:
            data = f.read()
    else:
        data = file_or_path.read()
        file_or_path.seek(0)
    result = chardet.detect(data)
    return result['encoding']

def load_dataset(file_path):
    encoding = detect_encoding(file_path)
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding=encoding)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV file.")
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

def compute_summary_statistics(df):
    """
    Compute summary statistics for the dataset.

    Returns a dictionary with:
    - numerical_stats: dict of column -> {mean, median, std}
    - categorical_stats: dict of column -> {value: count} for top 5 values
    - null_counts: dict of column -> null count
    - data_types: dict of column -> dtype
    """
    if df.empty:
        return {
            'numerical_stats': {},
            'categorical_stats': {},
            'null_counts': {},
            'data_types': {}
        }

    numerical_stats = {}
    categorical_stats = {}
    null_counts = {}
    data_types = {}

    for col in df.columns:
        data_types[col] = str(df[col].dtype)
        null_counts[col] = df[col].isnull().sum()

        # Numerical columns
        if df[col].dtype in ['int64', 'float64']:
            if not df[col].isnull().all():  # Skip if all values are null
                numerical_stats[col] = {
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std()
                }
        # Categorical columns (object/string)
        elif df[col].dtype == 'object':
            if not df[col].isnull().all():
                value_counts = df[col].value_counts().head(5)
                categorical_stats[col] = value_counts.to_dict()

    return {
        'numerical_stats': numerical_stats,
        'categorical_stats': categorical_stats,
        'null_counts': null_counts,
        'data_types': data_types
    }
