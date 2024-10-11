# cdef-converter

cdef-converter is a Python CLI tool that converts CSV files to Parquet format efficiently.

## Features

- Convert multiple CSV files to Parquet format in parallel
- Detect file encoding automatically
- Generate summary of processed files
- Progress tracking with rich console output
- Real-time status updates and summary display

## Installation

```bash
pip install cdef-converter
```

## Usage

```bash
cdef-converter /path/to/input/directory --processes 4
```

## Options

- `input_directory`: Path to the directory containing CSV files (required)
- `output_directory`: Path to the directory where Parquet files will be saved (default: `./registers`)
- `--processes`: Number of processes to use for parallel processing (default: 4)
- `--encoding-chunk-size`: Chunk size in MB for encoding detection (default: 1 MB)
- `--recursive`: Recursively search for files in subdirectories

## Output

- Parquet files are saved in `/path/to/your/fixed/output/directory/registers`
- A summary JSON file is generated at `register_summary.json`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Recent Changes

### Real-time Status and Summary Display

- Implemented a live updating display with Rich library
- Added a status table showing current file processing status for each process
- Included a summary table that updates in real-time as files are processed
- Added a progress bar showing overall completion status
- Displayed the most recent log message below the progress bar

### Encoding Chunk Size Modification

- The default encoding chunk size is now 1 MB
- Users can specify the encoding chunk size in MB using the `--encoding-chunk-size` option
- Internally, the program converts the MB value to bytes for processing

### Error Handling Improvements

- Enhanced exception handling throughout the codebase
- Added more specific error messages for common issues like file not found and permission errors

### Type Hinting Updates

- Updated type hints to be compatible with Python 3.12
- Added missing type annotations to functions and variables

### Code Structure and Style

- Improved code organization and readability
- Added or updated docstrings for better function documentation

### Performance Optimization

- Implemented dynamic chunk size adjustment for very large files in the encoding detection process

### Recursive File Processing

- Added a `--recursive` option to search for files in subdirectories

### Logging Enhancements

- Implemented a custom logging setup with both console and file output
- Added rich formatting to console log messages
