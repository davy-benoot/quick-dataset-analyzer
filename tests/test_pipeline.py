import io
import pandas as pd
import pytest
import tempfile
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_pipeline import detect_encoding, load_dataset, load_and_validate_csv, compute_summary_statistics, get_max_file_size_mb

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

def test_get_max_file_size_mb_default():
    # Test default value when no environment variable is set
    # Remove env var if it exists
    if 'MAX_FILE_SIZE_MB' in os.environ:
        del os.environ['MAX_FILE_SIZE_MB']
    assert get_max_file_size_mb() == 5

def test_get_max_file_size_mb_custom():
    # Test custom value from environment variable
    os.environ['MAX_FILE_SIZE_MB'] = '10'
    try:
        assert get_max_file_size_mb() == 10
    finally:
        # Clean up
        del os.environ['MAX_FILE_SIZE_MB']

def test_get_max_file_size_mb_invalid():
    # Test invalid environment variable (should fallback to default)
    os.environ['MAX_FILE_SIZE_MB'] = 'invalid'
    try:
        assert get_max_file_size_mb() == 5
    finally:
        # Clean up
        del os.environ['MAX_FILE_SIZE_MB']

def test_load_and_validate_csv_too_large():
    # Create large data > default 5MB limit
    large_data = b"a,b\n" + b"1,2\n" * 2000000  # approx 10MB
    file_obj = io.BytesIO(large_data)
    with pytest.raises(ValueError, match="File is too large"):
        load_and_validate_csv(file_obj)

def test_load_and_validate_csv_custom_limit():
    # Test with custom file size limit
    large_data = b"a,b\n" + b"1,2\n" * 100000  # approx 1MB (under custom limit of 2MB)
    file_obj = io.BytesIO(large_data)
    df = load_and_validate_csv(file_obj, max_size_mb=2)
    assert not df.empty

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

def test_compute_summary_statistics_mixed_data():
    # Create test DataFrame with mixed data types
    df = pd.DataFrame({
        'age': [25, 30, 35, 40, 45],
        'salary': [50000.0, 60000.0, 70000.0, 80000.0, 90000.0],
        'category': ['A', 'B', 'A', 'C', 'B'],
        'name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie']
    })
    stats = compute_summary_statistics(df)

    # Check numerical stats
    assert 'age' in stats['numerical_stats']
    assert 'salary' in stats['numerical_stats']
    assert stats['numerical_stats']['age']['mean'] == 35.0
    assert stats['numerical_stats']['age']['median'] == 35.0
    assert stats['numerical_stats']['salary']['mean'] == 70000.0

    # Check categorical stats
    assert 'category' in stats['categorical_stats']
    assert 'name' in stats['categorical_stats']
    assert len(stats['categorical_stats']['category']) <= 5
    assert stats['categorical_stats']['category']['A'] == 2
    assert stats['categorical_stats']['category']['B'] == 2

    # Check null counts
    assert all(count == 0 for count in stats['null_counts'].values())

    # Check data types
    assert stats['data_types']['age'] == 'int64'
    assert stats['data_types']['salary'] == 'float64'
    assert stats['data_types']['category'] == 'object'

def test_compute_summary_statistics_with_nulls():
    df = pd.DataFrame({
        'num_col': [1, 2, None, 4, 5],
        'cat_col': ['A', None, 'B', 'A', 'C']
    })
    stats = compute_summary_statistics(df)

    # Check null counts
    assert stats['null_counts']['num_col'] == 1
    assert stats['null_counts']['cat_col'] == 1

    # Check numerical stats (should still work with nulls)
    assert 'num_col' in stats['numerical_stats']
    assert stats['numerical_stats']['num_col']['mean'] == 3.0  # (1+2+4+5)/4

def test_compute_summary_statistics_empty_df():
    df = pd.DataFrame()
    stats = compute_summary_statistics(df)

    assert stats['numerical_stats'] == {}
    assert stats['categorical_stats'] == {}
    assert stats['null_counts'] == {}
    assert stats['data_types'] == {}

def test_compute_summary_statistics_all_null_numerical():
    df = pd.DataFrame({
        'all_null_num': [None, None, None],
        'valid_cat': ['A', 'B', 'C']
    })
    stats = compute_summary_statistics(df)

    # All null numerical column should not have stats
    assert 'all_null_num' not in stats['numerical_stats']

    # Categorical should still work
    assert 'valid_cat' in stats['categorical_stats']

    # Null counts should be correct
    assert stats['null_counts']['all_null_num'] == 3

def test_compute_summary_statistics_all_null_categorical():
    df = pd.DataFrame({
        'valid_num': [1, 2, 3],
        'all_null_cat': [None, None, None]
    })
    stats = compute_summary_statistics(df)

    # All null categorical column should not have stats
    assert 'all_null_cat' not in stats['categorical_stats']

    # Numerical should still work
    assert 'valid_num' in stats['numerical_stats']

def test_compute_summary_statistics_single_value_categorical():
    df = pd.DataFrame({
        'single_cat': ['A', 'A', 'A', 'A', 'A']
    })
    stats = compute_summary_statistics(df)

    assert stats['categorical_stats']['single_cat']['A'] == 5
    assert len(stats['categorical_stats']['single_cat']) == 1

def test_compute_summary_statistics_more_than_5_categories():
    df = pd.DataFrame({
        'many_cat': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
    })
    stats = compute_summary_statistics(df)

    # Should only return top 5
    assert len(stats['categorical_stats']['many_cat']) == 5

    # Most frequent should be A, B, C (appearing twice each)
    top_values = stats['categorical_stats']['many_cat']
    assert 'A' in top_values
    assert 'B' in top_values
    assert 'C' in top_values
    assert top_values['A'] == 2
