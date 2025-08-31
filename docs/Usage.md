# User Guide

## Quick Start

1. **Launch the Application**
   ```bash
   streamlit run src/app.py
   ```
   The application will open in your default web browser at `http://localhost:8501`

2. **Upload a CSV File**
   - Click "Choose a CSV file" or drag and drop a CSV file
   - File size limit is configurable (default 5MB, set via `MAX_FILE_SIZE_MB` environment variable)
   - Automatic encoding detection handles various file formats

3. **View Results**
   - Data preview shows the first few rows
   - Summary statistics are displayed in organized sections
   - Expand categorical columns to see value frequencies

## Features Overview

### File Upload & Validation

The application accepts CSV files with the following validations:
- **File Format**: Must be .csv extension
- **File Size**: Configurable maximum (default 5MB, set via `MAX_FILE_SIZE_MB` environment variable)
- **Encoding**: Automatic detection (UTF-8, ISO-8859-1, etc.)
- **Content**: Must contain valid CSV data

### Summary Statistics

#### Data Overview
- Total number of rows and columns
- Total count of null values across all columns

#### Numerical Columns
For columns with numerical data (integers, floats):
- **Mean**: Average value
- **Median**: Middle value when sorted
- **Standard Deviation**: Measure of data spread

#### Categorical Columns
For columns with text/categorical data:
- **Top 5 Values**: Most frequent values and their counts
- Expandable sections for detailed viewing

#### Data Quality Information
- **Null Counts**: Number of missing values per column
- **Data Types**: Pandas data type for each column

## Example Usage

### Sample Dataset
Consider a CSV file `employee_data.csv` with the following structure:

```csv
name,age,salary,department,hire_year
John Doe,30,50000,Engineering,2020
Jane Smith,25,45000,Marketing,2021
Bob Johnson,35,60000,Engineering,2019
Alice Brown,28,52000,Sales,2020
Charlie Wilson,42,70000,Engineering,2018
```

### Expected Output

#### Data Preview
Shows the first 5 rows of your uploaded data.

#### Summary Statistics

**Data Overview:**
- Total Rows: 5
- Total Columns: 5
- Total Null Values: 0

**Numerical Columns Statistics:**
```
          mean   median       std
age      32.0     30.0     6.48
salary  55400.0  52000.0  9879.92
```

**Categorical Columns (Top 5 Values):**
- **department**: Engineering (3), Marketing (1), Sales (1)
- **name**: John Doe (1), Jane Smith (1), Bob Johnson (1), Alice Brown (1), Charlie Wilson (1)

**Null Values Summary:**
- No null values found (all columns show 0)

**Column Data Types:**
- name: object
- age: int64
- salary: float64
- department: object
- hire_year: int64

## Error Handling

The application provides clear error messages for common issues:

### File Upload Errors
- **"File is too large"**: File exceeds the configured size limit (default 5MB, set via `MAX_FILE_SIZE_MB`)
- **"Encoding error"**: Unable to detect or decode file encoding
- **"Parsing error"**: File is not a valid CSV format
- **"CSV is empty"**: File contains no data

### Data Processing Errors
- **"Unsupported file format"**: Non-CSV files are rejected
- **"Cannot read CSV"**: Corrupted or invalid CSV structure

## Best Practices

### Data Preparation
1. **Clean Data**: Remove unnecessary columns before upload
2. **Consistent Formatting**: Ensure consistent data types within columns
3. **Encoding**: Save CSV files as UTF-8 when possible
4. **File Size**: Keep files under 5MB for optimal performance

### Data Types
- **Numerical**: age, salary, counts, measurements
- **Categorical**: names, categories, labels, status
- **Dates**: Store as strings initially, convert as needed

## Troubleshooting

### Common Issues

**Application won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.7+ required)
- Verify Streamlit installation

**File upload fails:**
- Check file size (must be < 5MB)
- Ensure file has .csv extension
- Try saving file with UTF-8 encoding

**Statistics not showing:**
- Verify CSV has valid data
- Check for special characters in headers
- Ensure columns have appropriate data types

**Performance issues:**
- Large files (>1MB) may take longer to process
- Consider sampling large datasets
- Close other applications to free memory

## Advanced Usage

### Programmatic Access

You can also use the data pipeline functions directly in Python:

```python
from src.data_pipeline import load_and_validate_csv, compute_summary_statistics
import pandas as pd
from io import BytesIO

# Load data
with open('data.csv', 'rb') as f:
    df = load_and_validate_csv(f)

# Compute statistics
stats = compute_summary_statistics(df)

# Access specific statistics
numerical_stats = stats['numerical_stats']
categorical_stats = stats['categorical_stats']
null_counts = stats['null_counts']
```

### Integration with Other Tools

The modular design allows integration with:
- Jupyter notebooks for further analysis
- Database systems for data storage
- API endpoints for automated processing
- Dashboard tools for enhanced visualization

## Support

For issues or questions:
1. Check this documentation first
2. Review error messages for specific guidance
3. Ensure your environment matches requirements
4. Test with sample data to isolate issues

## Configuration

### Configuration Options

The application supports multiple ways to configure the file size limit:

#### Environment Variables
- **MAX_FILE_SIZE_MB**: Controls the application's validation limit (default: 5MB)
  ```bash
  export MAX_FILE_SIZE_MB=10  # Allow files up to 10MB
  ```

#### Streamlit Configuration
For the UI to match the actual limit, also configure Streamlit:

**Local development** (`.streamlit/config.toml`):
```toml
[server]
maxUploadSize = 10
```

**Cloud deployment** (environment variable):
```bash
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=10
```

### Docker Deployment

When deploying with Docker, set both environment variables:

```yaml
environment:
  - MAX_FILE_SIZE_MB=20
  - STREAMLIT_SERVER_MAX_UPLOAD_SIZE=20
```

## Version Information

- **Current Version**: 1.0.0
- **Python Version**: 3.7+
- **Key Dependencies**: Streamlit, Pandas, chardet
- **File Size Limit**: Configurable (default 5MB)
- **Supported Formats**: CSV only
