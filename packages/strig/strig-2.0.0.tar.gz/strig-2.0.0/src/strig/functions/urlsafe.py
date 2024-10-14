from random import randint, shuffle
from secrets import choice
from typing import Optional

from ..constants import ALPHANUMERIC, URLSAFE


def urlsafe(length: int = 6, prefix: Optional[str] = None):
    "Generate a random string of letters and numbers and unreserved url characters"

    charset = ALPHANUMERIC + URLSAFE

    generated_chars = [choice(charset) for _ in range(length)]

    ## Ensure there is always a character present from
    ## every enabled characterset
    generated_chars[randint(0, len(generated_chars) - 1)] = choice(URLSAFE)

    shuffle(generated_chars)
    generated = "".join(generated_chars)

    if not prefix == None:
        generated = prefix + generated

    return generated
