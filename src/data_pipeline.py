import pandas as pd
import chardet
import os
import matplotlib.pyplot as plt
import seaborn as sns
import io

def get_max_file_size_mb():
    """
    Get configurable maximum file size from environment variable.

    Returns:
        int: Maximum file size in MB (default: 5)
    """
    default = 5  # MB
    try:
        return int(os.getenv('MAX_FILE_SIZE_MB', default))
    except ValueError:
        return default

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

def load_and_validate_csv(file, max_size_mb=None):
    """
    Load CSV with validation:
    - File type
    - Encoding
    - Size

    Args:
        file: File object to load
        max_size_mb: Maximum file size in MB (optional, uses environment variable if not provided)
    """
    # Use configurable max size if not provided
    if max_size_mb is None:
        max_size_mb = get_max_file_size_mb()

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

def get_numerical_columns(df):
    """
    Get list of numerical columns from DataFrame.

    Args:
        df: pandas DataFrame

    Returns:
        list: List of numerical column names
    """
    return [col for col in df.columns if df[col].dtype in ['int64', 'float64']]

def generate_correlation_heatmap(df):
    """
    Generate correlation heatmap for numerical columns.

    Args:
        df: pandas DataFrame

    Returns:
        matplotlib.figure.Figure: Correlation heatmap figure
    """
    numerical_cols = get_numerical_columns(df)

    if len(numerical_cols) < 2:
        return None  # Need at least 2 numerical columns for correlation

    # Calculate correlation matrix
    corr_matrix = df[numerical_cols].corr()

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Generate heatmap
    sns.heatmap(corr_matrix,
                annot=True,
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8},
                ax=ax)

    ax.set_title('Correlation Heatmap of Numerical Variables', fontsize=14, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    return fig

def generate_histogram(df, column):
    """
    Generate histogram for a specific numerical column.

    Args:
        df: pandas DataFrame
        column: Column name to plot

    Returns:
        matplotlib.figure.Figure: Histogram figure
    """
    if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
        return None

    # Remove null values for plotting
    data = df[column].dropna()

    if data.empty:
        return None

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Generate histogram
    n, bins, patches = ax.hist(data, bins=30, alpha=0.7, edgecolor='black')

    # Add styling
    ax.set_title(f'Distribution of {column}', fontsize=14, pad=20)
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Add statistics as text
    mean_val = data.mean()
    median_val = data.median()
    std_val = data.std()

    stats_text = '.2f'
    ax.text(0.02, 0.98, stats_text,
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()

    return fig

def generate_boxplot(df, column):
    """
    Generate boxplot for a specific numerical column.

    Args:
        df: pandas DataFrame
        column: Column name to plot

    Returns:
        matplotlib.figure.Figure: Boxplot figure
    """
    if column not in df.columns or df[column].dtype not in ['int64', 'float64']:
        return None

    # Remove null values for plotting
    data = df[column].dropna()

    if data.empty:
        return None

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Generate boxplot
    bp = ax.boxplot(data, patch_artist=True, notch=True)

    # Styling
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][0].set_edgecolor('black')
    bp['medians'][0].set_color('red')
    bp['medians'][0].set_linewidth(2)

    # Add styling
    ax.set_title(f'Boxplot of {column}', fontsize=14, pad=20)
    ax.set_ylabel(column, fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')

    # Add statistics
    stats = data.describe()
    stats_text = '.2f'
    ax.text(0.02, 0.98, stats_text,
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    plt.tight_layout()

    return fig
