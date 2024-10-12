"""
The `decentriq_util` library provides helpers for common operations,
not only when automating your workflows with the `decentriq_platform` package,
but also when writing your own Python computations inside Data Clean Rooms.

It is available inside the computation container for Python scripts
and can be imported just like any other library. For example:
```python
import decentriq_util
data = decentriq_util.sql.read_sql_data_from_dir("/path/to/computation")
```
"""
from . import sql
from . import proto
from . import python
from . import error
from . import spark

from .sql import (
    read_tabular_data,
    write_tabular_data
)

__pdoc__ = {
    "sql": True,
    "proto": False,
    "python": False,
    "error": False,
}
