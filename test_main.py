import pytest
from main import get_notebook_cells, get_date_from_filename
from pathlib import Path
import tempfile
import json
from datetime import datetime

def test_get_notebook_cells_reads_cells():
    # Create a minimal notebook file
    nb = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Title"], "metadata": {}},
            {"cell_type": "code", "source": ["print('hi')"], "metadata": {}, "outputs": []}
        ]
    }
    with tempfile.NamedTemporaryFile(suffix=".ipynb", mode="w+", delete=False) as f:
        json.dump(nb, f)
        f.flush()
        path = Path(f.name)
        cells = get_notebook_cells(path)
        assert len(cells) == 2
        assert cells[0]["cell_type"] == "markdown"
        assert cells[1]["cell_type"] == "code"
        assert cells[0]["content"] == "# Title"
        assert cells[1]["content"] == "print('hi')"


def test_get_notebook_cells_file_not_found():
    cells = get_notebook_cells(Path("/tmp/doesnotexist.ipynb"))
    assert cells == []


def test_get_date_from_filename_valid():
    fname = "2025-01-12-Get-Date-From-This.ipynb"
    dt = get_date_from_filename(fname)
    assert isinstance(dt, datetime)
    assert dt.year == 2025 and dt.month == 1 and dt.day == 12


def test_get_date_from_filename_invalid():
    fname = "notadate-at-all.ipynb"
    dt = get_date_from_filename(fname)
    assert isinstance(dt, datetime)
    # Should return now, so year should be current year
    assert abs((dt - datetime.now()).total_seconds()) < 5
