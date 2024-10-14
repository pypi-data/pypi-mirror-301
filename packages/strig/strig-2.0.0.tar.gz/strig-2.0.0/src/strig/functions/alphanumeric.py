from secrets import choice
from typing import Optional

from ..constants import ALPHANUMERIC, ALPHANUMERIC_LOWER, ALPHANUMERIC_UPPER
from ..types import Case


def alphanumeric(length: int = 6, prefix: Optional[str] = None, case: Case = None):
    "Generate a random string of letters and numbers"

    charset = ALPHANUMERIC
    if case == "upper":
        charset = ALPHANUMERIC_UPPER
    if case == "lower":
        charset = ALPHANUMERIC_LOWER

    generated = "".join(choice(charset) for _ in range(length))
    
    if not prefix == None:
        generated = prefix + generated

    return generated
