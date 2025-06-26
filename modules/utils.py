import os

def ensure_dir(path: str) -> None:
    """
    Tworzy katalog „path”, jeśli nie istnieje.
    """
    os.makedirs(path, exist_ok=True)