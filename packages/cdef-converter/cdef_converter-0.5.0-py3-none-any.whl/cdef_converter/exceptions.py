class CdefConverterError(Exception):
    """Base exception class for cdef-converter"""


class FileProcessingError(CdefConverterError):
    """Raised when there's an error processing a file"""


class EncodingDetectionError(CdefConverterError):
    """Raised when there's an error detecting file encoding"""


class ParquetWriteError(CdefConverterError):
    """Raised when there's an error writing to Parquet format"""
