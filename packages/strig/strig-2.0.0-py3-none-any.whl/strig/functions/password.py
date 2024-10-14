from random import randint, shuffle
from secrets import choice
from typing import Optional

from ..constants import ALPHA, ALPHA_LOWER, ALPHA_UPPER, NUMERIC, SYMBOLS
from ..types import Case


def password(
    length: int = 20,
    prefix: Optional[str] = None,
    case: Case = None,
    digits=True,
    symbols=True,
):
    """Generate a cryptographically secure random password"""

    charset = ALPHA
    if case == "upper":
        charset = ALPHA_UPPER
    if case == "lower":
        charset = ALPHA_LOWER

    if digits:
        charset += NUMERIC

    if symbols:
        charset += SYMBOLS + SYMBOLS

    generated_chars = [choice(charset) for _ in range(length)]

    ## Ensure there is always a character present from
    ## every enabled characterset
    if digits:
        generated_chars[randint(0, len(generated_chars) - 1)] = choice(NUMERIC)
    if symbols:
        generated_chars[randint(0, len(generated_chars) - 1)] = choice(SYMBOLS)

    shuffle(generated_chars)
    generated = "".join(generated_chars)

    if not prefix == None:
        generated = prefix + generated

    return generated
