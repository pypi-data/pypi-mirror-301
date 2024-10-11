from collections.abc import Callable

import fsspec
import pandas as pd
import pyarrow
import pyarrow.parquet

from .utils import create_local_dir_tree


def get_file(fs: fsspec.AbstractFileSystem, remote_path: str, local_path: str):
    """Transfer a file from remote to local file system."""
    create_local_dir_tree(local_path)
    fs.get_file(remote_path, local_path)


def put(fs: fsspec.AbstractFileSystem, local_path: str, remote_path: str):
    """Transfer a file from local to remote file system."""
    fs.put(local_path, remote_path)


def open_for_writing(fs: fsspec.AbstractFileSystem, path: str, mode: str = "wb"):
    return fs.open(path, mode)


def open_for_reading(fs: fsspec.AbstractFileSystem, path: str, mode: str = "rb"):
    return fs.open(path, mode)


def move(fs: fsspec.AbstractFileSystem, source_path: str, destination_path: str):
    """
    This fails if the target file system is not capable of creating the
    directory, for example if it is write-only or if auto_mkdir=False. There is
    no command line equivalent of this scenario without an explicit mkdir to
    create the new directory.
    See https://filesystem-spec.readthedocs.io/en/latest/copying.html for more
    information.
    """
    fs.mv(source_path, destination_path)


def list_files(
    fs: fsspec.AbstractFileSystem, path: str, recursive: bool = False
) -> list[str]:
    if recursive is True:
        maxdepth = None
    else:
        maxdepth = 1

    return fs.find(path, maxdepth)


def remove_files(
    fs: fsspec.AbstractFileSystem, paths: str | list[str], recursive: bool = False
):
    fs.rm(paths, recursive)


def read_dataset_from_parquet(fs: fsspec.AbstractFileSystem, path: str) -> pd.DataFrame:
    df = pyarrow.parquet.ParquetDataset(path, filesystem=fs).read_pandas().to_pandas()
    return df


def write_dataframe_to_parquet(
    fs: fsspec.AbstractFileSystem, path: str, df: pd.DataFrame
):
    table = pyarrow.Table.from_pandas(df)
    pyarrow.parquet.write_table(table, path, filesystem=fs)


def loader(
    fs: fsspec.AbstractFileSystem, path: str, load_method: Callable, mode: str = "rb"
):
    """load the object from the path using the specified load_method.

    Parameters
    ----------
    path : str
        load the object from this path.
    load_method : Callable
        the method to use to load the object.

    Returns
    -------
    the object loaded from the path.
    """
    with open_for_reading(fs, path, mode) as f:
        return load_method(f)


def write_to_file(fs: fsspec.AbstractFileSystem, path: str, content: str | bytes):
    if isinstance(content, str):
        mode = "w"
    else:
        mode = "wb"

    with open_for_writing(fs, path, mode) as f:
        f.write(content)
