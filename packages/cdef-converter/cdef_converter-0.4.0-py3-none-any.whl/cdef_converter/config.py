import os
import re
from pathlib import Path

OUTPUT_DIRECTORY = Path(os.environ.get("CDEF_OUTPUT_DIR", ""))
FILE_PATTERN = r"([a-zA-Z_]+)(\d+)"
GREEN = "bold_green"
DEFAULT_ENCODING_CHUNK_SIZE = 1  # 1 MB default

# Compile the regex pattern
FILE_PATTERN_REGEX = re.compile(FILE_PATTERN)
