# System Architecture

## Overview

The Quick Dataset Analyzer is a web-based application built with Streamlit that provides CSV data analysis capabilities. The system follows a modular architecture with clear separation of concerns between data processing, user interface, and testing.

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Data Pipeline  │────│   Pandas Data   │
│     (app.py)    │    │(data_pipeline.py)│    │   Processing    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Upload   │    │   Validation    │    │   Statistics    │
│     Interface   │    │   & Cleaning    │    │   Computation   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Components

### 1. User Interface Layer (`src/app.py`)

**Purpose**: Provides the web interface for user interaction

**Key Features**:
- File upload component with CSV validation
- Data preview display
- Statistics visualization with organized sections
- Error handling and user feedback
- Responsive layout with metrics and expandable sections

**Dependencies**:
- Streamlit for web framework
- Pandas for data manipulation
- Custom data_pipeline module

### 2. Data Processing Layer (`src/data_pipeline.py`)

**Purpose**: Handles all data loading, validation, and analysis operations

**Key Functions**:

#### `detect_encoding(file_or_path)`
- **Input**: File object or file path
- **Output**: Detected character encoding
- **Purpose**: Automatically detect CSV file encoding using chardet library
- **Error Handling**: Returns detected encoding or raises exception

#### `load_dataset(file_path)`
- **Input**: File path (string)
- **Output**: Pandas DataFrame
- **Purpose**: Load CSV file with detected encoding
- **Validation**: File format checking (.csv extension)
- **Error Handling**: Comprehensive exception handling for file operations

#### `get_max_file_size_mb()`
- **Input**: None (reads from environment)
- **Output**: Integer (file size limit in MB)
- **Purpose**: Get configurable maximum file size from environment variable
- **Default**: 5MB if environment variable not set
- **Environment Variable**: `MAX_FILE_SIZE_MB`

#### `load_and_validate_csv(file, max_size_mb=None)`
- **Input**: File object (from Streamlit upload), optional max_size_mb
- **Output**: Pandas DataFrame
- **Purpose**: Complete CSV loading and validation pipeline
- **Validations**:
  - File size limit (configurable, default 5MB)
  - Encoding detection
  - CSV parsing validation
  - Empty file detection
- **Error Handling**: Specific error messages for different failure modes

#### `compute_summary_statistics(df)`
- **Input**: Pandas DataFrame
- **Output**: Dictionary with statistical summaries
- **Purpose**: Generate comprehensive statistics for all columns
- **Statistics Generated**:
  - **Numerical columns** (int64, float64): mean, median, standard deviation
  - **Categorical columns** (object): top 5 value frequencies
  - **All columns**: null counts, data types
- **Edge Cases**: Handles empty DataFrames, all-null columns, mixed data types

### 3. Testing Layer (`tests/test_pipeline.py`)

**Purpose**: Ensure reliability and correctness of all functionality

**Test Coverage**:
- Encoding detection (file path and file object)
- Dataset loading (valid and invalid files)
- CSV validation (size limits, empty files, parsing errors)
- Summary statistics computation (mixed data, nulls, edge cases)
- Error handling scenarios

## Data Flow

1. **File Upload**: User selects CSV file through Streamlit interface
2. **Validation**: File size and format validation
3. **Encoding Detection**: Automatic character encoding detection
4. **Data Loading**: CSV parsing with detected encoding
5. **Statistics Computation**: Generate summary statistics for all columns
6. **Display**: Render results in organized, interactive format

## Technology Stack

- **Frontend/UI**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Encoding Detection**: chardet
- **Testing**: pytest
- **Deployment**: Docker (for containerization)

## Design Principles

### Modularity
- Clear separation between UI, data processing, and testing
- Reusable functions with single responsibilities
- Import-based dependency management

### Error Handling
- Comprehensive exception handling at all levels
- User-friendly error messages
- Graceful degradation for edge cases

### Performance
- Efficient pandas operations
- Memory-conscious data processing
- Scalable architecture for future enhancements

### Maintainability
- Comprehensive documentation
- Unit test coverage
- Clean, readable code structure

## Future Extensibility

The modular design allows for easy addition of:
- Additional file format support
- Advanced statistical analysis
- Data visualization enhancements
- Export functionality
- Database integration
- API endpoints

## Security Considerations

- File size limits prevent memory exhaustion
- Input validation prevents malicious file uploads
- No execution of uploaded code
- Safe encoding detection and parsing
