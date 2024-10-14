import inspect
from typing import Callable, Optional

from ..functions.var_methods.dates import DateMethods
from ..functions.var_methods.system import SystemMethods

Methods = type("Methods", (DateMethods, SystemMethods), dict(methods="methods"))


def var(varstring: str, prefix: Optional[str] = None, methods: Callable = Methods):
    """
    Generate a string from specified variables
    """

    generated = ""

    method_names = [
        i[0] for i in inspect.getmembers(methods, predicate=inspect.isfunction)
    ]
    methods = methods()

    for i, var in enumerate(varstring.split("%")):
        if i == 0:
            continue  ## Varstring starts with %
        if not var in method_names:
            raise TypeError(f"Unrecognized variable '{var}'")

        generated += str(getattr(methods, var)())

    if not prefix == None:
        generated = prefix + generated

    return generated
