import os
from os import path as osp
from typing import Generator, Optional, Union


def scandir(
    dir_path: str, 
    suffix: Optional[Union[str, tuple]] = None, 
    recursive: bool = False, 
    full_path: bool = False
) -> Generator[str, None, None]:
    """Scan a directory to find files of interest.

    Args:
        dir_path (str): Path of the directory to scan.
        suffix (str | tuple(str), optional): File suffix(es) to filter by. Default: None.
        recursive (bool, optional): Whether to recursively scan subdirectories. Default: False.
        full_path (bool, optional): Whether to return the full file path or relative path. Default: False.

    Returns:
        Generator[str]: A generator for all matching files with either full or relative paths.
    """

    if suffix is not None and not isinstance(suffix, (str, tuple)):
        raise TypeError('"suffix" must be a string or a tuple of strings.')

    root = dir_path

    def _scandir(current_dir: str) -> Generator[str, None, None]:
        """Helper function to scan directory and yield files."""
        for entry in os.scandir(current_dir):
            if entry.is_file() and not entry.name.startswith('.'):
                return_path = entry.path if full_path else osp.relpath(entry.path, root)

                if suffix is None or return_path.endswith(suffix):
                    yield return_path
            elif entry.is_dir() and recursive:
                yield from _scandir(entry.path)

    return _scandir(dir_path)
