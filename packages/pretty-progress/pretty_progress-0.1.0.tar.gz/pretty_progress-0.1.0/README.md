# pygress

A simple Python progress bar utility for loops.

## Installation

```
pip install pygress
```

## Usage

```python
from pygress import progress_bar

for i in range(100):
    progress_bar(i + 1, 100)
```
