# Trace Generator

This package generates random traces based on various sequence schemas.
Creator : Dr. Kovacs Laszlo

## Usage

```python
from trace_generator import manual_trace, Cseqs

# Generate 100 random traces using schema "S_X_01"
traces = manual_trace(Cseqs["S_X_01"], N=100)
print(traces)
