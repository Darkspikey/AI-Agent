# memory.py
import json
import os

FILE = "memory.json"


def load_memory():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_all(memory):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def add_memory(text: str):
    memory = load_memory()
    memory.append(text)
    save_all(memory)
    return "Gespeichert"


def get_memory():
    return load_memory()