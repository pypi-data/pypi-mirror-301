from secrets import choice
from typing import Optional

from ..constants import NUMERIC


def numeric(length: int = 6, prefix: Optional[int] = None) -> int:
    "Generate a random number"

    charset = NUMERIC
    generated = "".join(choice(charset) for _ in range(length))

    ## If the first number is a 0, it will be stripped when converting
    ## it to an integer. Replace it with another number
    ## to make sure the length is correct
    if generated[0] == "0":
        generated = choice(charset.replace("0", "")) + generated[1:]

    if not isinstance(prefix, int):
        if not prefix == None:
            raise TypeError("Prefix should be of type int")
    
    if not prefix == None:
        generated = f"{prefix}{generated:}"

    return int(generated)
