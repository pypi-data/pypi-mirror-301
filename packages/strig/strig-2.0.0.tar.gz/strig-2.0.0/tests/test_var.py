import os
import sys

sys.path.append(os.getcwd())

from datetime import datetime

from src.strig import var


def test_dates():
    generated = var("%yyyy%yy%mm%m%dd%d")
    today = datetime.today()

    month = str(today.month)
    if not len(month) == 2:
        month = "0" + month

    day = str(today.day)
    if not len(day) == 2:
        day = "0" + day

    assert (
        generated
        == f"{today.year}{str(today.year)[-2:]}{month}{today.month}{day}{today.day}"
    )


def test_prefix():
    generated = var("%yy", prefix="abc")
    assert generated[:3] == "abc"
