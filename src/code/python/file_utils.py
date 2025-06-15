import os


def read_file(file_path: str) -> str:
    """Read a file and return its contents as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path: str, content: str):
    """Write a string to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def get_file_size(file_path: str) -> int:
    """Return the size of a file in bytes."""
    return os.path.getsize(file_path)
