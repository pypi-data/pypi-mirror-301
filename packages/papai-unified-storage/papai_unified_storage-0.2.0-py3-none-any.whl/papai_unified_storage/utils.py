import os
from pathlib import Path
from typing import TypeVar


def create_local_dir_tree(path: str):
    """Create a directory tree in the local file system if it doesn't
    already exist.

    Parameters
    ----------
    path : str
        Path that will be created. If it is a file (i.e. it ends with a
        trailing slash), the parent directories will be created, but not the
        file itself.
    """
    path_ = Path(path)

    if not path.endswith(os.sep):
        # If the path is a file, we want to create the parent directories
        path_ = path_.parent

    path_.mkdir(parents=True, exist_ok=True)


def joinpath(*path_pieces: str | list[str]) -> str | list[str]:
    """Join paths.

    If one of the path piece is a list, the function will join each element of
    the list with the other path pieces.

    os separator in the path pieces will be remove, except for the trailing
    separator of the last piece which is used to differenciate folders from
    files.

    Parameters
    ----------
    *path_pieces : str | list[str]
        Path pieces to join.

    Returns
    -------
    str | list[str]
        the joined path: str if all the components are strings, list of strings
        otherwise.

    Examples
    --------
    >>> joinpath("a", "b", "c")
    "a/b/c"
    >>> joinpath(["a", "b"], "c/")
    ["a/c/", "b/c/"]
    >>> joinpath(["a", "b"], ["c", "d"], "e")
    ["a/c/e", "a/d/e", "b/c/e", "b/d/e"]
    """
    if len(path_pieces) < 2:
        raise ValueError("At least two path pieces are required.")
    if len(path_pieces) > 2:
        # Recursive call to join the first two pieces and the rest of the pieces.
        # This will slowly reduce the number of pieces until there are only two.
        return joinpath(joinpath(path_pieces[0], path_pieces[1]), *path_pieces[2:])

    first_paths = ensure_in_list(path_pieces[0])
    second_paths = ensure_in_list(path_pieces[1])

    joined_paths = _cartesian_product_join_paths(first_paths, second_paths)

    if len(joined_paths) == 1:
        return joined_paths[0]

    return joined_paths


def _cartesian_product_join_paths(
    first_path_piece: list[str], second_path_piece: list[str]
) -> list[str]:
    """Compute the cartesian product of two lists of paths.

    The output list will contain the concatenation of each element of the first
    list with each element of the second list.

    Returns
    -------
    list[str]
        List of length len(first_path_piece) * len(second_path_piece) that
        contains the concatenated path.
    """
    results = [""] * len(first_path_piece) * len(second_path_piece)
    count = 0
    for first_path in first_path_piece:
        for second_path in second_path_piece:
            results[count] = first_path.rstrip("/") + os.sep + second_path.lstrip("/")
            count += 1

    return results


T = TypeVar("T")


def ensure_in_list(value: T | list[T]) -> list[T]:
    """Put in a list any scalar value that is not None.

    If it is already a list, do nothing.
    """
    if value is not None and not isinstance(value, list):
        value = [value]

    return value
