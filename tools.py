# tools.py
import math
import re
from memory import add_memory, get_memory


def calculate(expression: str):
    try:
        allowed = {
            "sqrt": math.sqrt
        }

        return str(eval(expression, {"__builtins__": {}}, allowed))
    except Exception as e:
        return f"Fehler: {e}"


def is_valid_calculation(arg: str):
    return bool(re.match(r"^[0-9\+\-\*\/\(\)\s\.sqrt]+$", arg))


def save_memory(text: str):
    return add_memory(text)


def load_memory(_=None):
    return ", ".join(get_memory())