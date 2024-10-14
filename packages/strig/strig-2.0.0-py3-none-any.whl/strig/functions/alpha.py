from secrets import choice
from typing import Optional

from ..constants import ALPHA, ALPHA_LOWER, ALPHA_UPPER
from ..types import Case


def alpha(length: int = 6, prefix: Optional[str] = None, case: Case = None):
    "Generate a random string of letters"

    charset = ALPHA
    if case == "upper":
        charset = ALPHA_UPPER
    if case == "lower":
        charset = ALPHA_LOWER

    generated = "".join(choice(charset) for _ in range(length))
    
    if not prefix == None:
        generated = prefix + generated

    return generated
