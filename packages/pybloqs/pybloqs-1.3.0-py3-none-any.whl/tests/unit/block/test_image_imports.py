import sys
from unittest.mock import patch

import pytest


def test_missing_matplotlib_raises_error():
    with patch.dict("sys.modules", {"matplotlib.pyplot": None}):
        # Force re-import if imported in previous test
        if "pybloqs.block.image" in sys.modules:
            del sys.modules["pybloqs.block.image"]
        with pytest.raises(ImportError):
            import pybloqs.block.image  # noqa: F401


def test_missing_plotly_does_not_raise_error():
    with patch.dict("sys.modules", {"plotly": None}):
        # Force re-import if imported in previous test
        if "pybloqs.block.image" in sys.modules:
            del sys.modules["pybloqs.block.image"]
        import pybloqs.block.image  # noqa: F401


def test_missing_bokeh_does_not_raise_error():
    with patch.dict("sys.modules", {"bokeh": None}):
        # Force re-import if imported in previous test
        if "pybloqs.block.image" in sys.modules:
            del sys.modules["pybloqs.block.image"]
        import pybloqs.block.image  # noqa: F401
