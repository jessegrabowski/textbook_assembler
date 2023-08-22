import numpy as np

EXPECTED_KEYS = ["week", "date", "topic", "reference", "chapter", "page_start", "page_end"]
EXPECTED_DTYPES = {
    "week": np.dtype(int),
    "date": np.dtype("datetime64[ns]"),
    "topic": np.dtype("O"),
    "reference": np.dtype("O"),
    "chapter": np.dtype(float),
    "page_start": np.dtype(float),
    "page_end": np.dtype(float),
}
