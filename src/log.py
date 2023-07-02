import colorama
from typing import Any


def iprint(*args: Any, **kwargs: Any) -> None:
    """prints a informatory message
    """
    print(colorama.Fore.CYAN, "[i] ", end='')
    print(colorama.Fore.RESET, end='')
    print(*args, **kwargs)


def wprint(*args: Any, **kwargs: Any) -> None:
    """prints a warning message
    """
    print(colorama.Fore.YELLOW, "[w] ", end='')
    print(colorama.Fore.RESET, end='')
    print(*args, **kwargs)


def eprint(*args: Any, **kwargs: Any) -> None:
    """prints a error message
    """
    print(colorama.Fore.RED, "[e] ", end='')
    print(colorama.Fore.RESET, end='')
    print(*args, **kwargs)


def cprint(*args: Any, **kwargs: Any) -> None:
    """prints a completion message
    """
    print(colorama.Fore.GREEN, "[c] ", end='')
    print(colorama.Fore.RESET, end='')
    print(*args, **kwargs)


def iformat(*args: Any, **kwargs: Any) -> str:
    """formats a informatory message
    """
    return f"{colorama.Fore.CYAN}[i] {colorama.Fore.RESET}" + \
        f"{str(*args, **kwargs)}"
