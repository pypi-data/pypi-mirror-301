"""
These tests, as beautiful as they might be, are not perfect. The biggest
limitation is that the file sotrage tested can only be the local one since
tempfile is used. It relies on OS specification to create and remove
temporary files / folders. Unfortunately, it cannot be extended to every
file system support in fsspec.

Tests of read/write methods are not isolated, and they rely on each other
to pass. If the tests fails, one of them (or both) is the culprit.
"""

import os
from tempfile import NamedTemporaryFile, TemporaryDirectory

import fsspec
import pytest


@pytest.fixture()
def fs():
    return fsspec.filesystem("file", auto_mkdir=False)


def test_dataframe_io_parquet(fs):
    import pandas as pd

    from papai_unified_storage import (
        read_dataset_from_parquet,
        write_dataframe_to_parquet,
    )

    df = pd.DataFrame(
        {
            "one": [-1, 1, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    with NamedTemporaryFile(mode="wb+") as file:
        write_dataframe_to_parquet(fs, file.name, df)
        df_wrote_read = read_dataset_from_parquet(fs, file.name)

    assert df.equals(df_wrote_read)


def test_get_file(fs):
    from papai_unified_storage import get_file

    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        get_file(fs, f"{d}/f1", f"{d}/f2")

        with open(f"{d}/f2") as f:
            assert f.read() == "content"


def test_get_file_folder_creation(fs):
    from papai_unified_storage import get_file

    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        get_file(fs, f"{d}/f1", f"{d}/a/b/c/f2")

        with open(f"{d}/a/b/c/f2") as f:
            assert f.read() == "content"


def test_list_files(fs):
    from papai_unified_storage import list_files

    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        os.mkdir(f"{d}/d")
        with open(f"{d}/d/f2", "w") as f:
            f.write("content")

        assert set(list_files(fs, d, recursive=True)) == {f"{d}/f1", f"{d}/d/f2"}
        assert set(list_files(fs, d)) == {f"{d}/f1"}


def test_remove_files(fs):
    from papai_unified_storage import remove_files

    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        os.mkdir(f"{d}/d")
        with open(f"{d}/d/f2", "w") as f:
            f.write("content")

        remove_files(fs, [f"{d}/f1", f"{d}/d/f2"])

        assert not os.path.exists(f"{d}/f1")
        assert not os.path.exists(f"{d}/d/f2")


def test_open_read_write(fs):
    from papai_unified_storage import open_for_reading, open_for_writing

    with NamedTemporaryFile(mode="wb+") as file:
        with open_for_writing(fs, file.name) as f:
            f.write(b"content")

        with open_for_reading(fs, file.name) as f:
            assert f.read() == b"content"


def test_move(fs):
    from papai_unified_storage import move

    with TemporaryDirectory() as d:
        # create a file
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        move(fs, f"{d}/f1", f"{d}/f2")

        assert not os.path.exists(f"{d}/f1")
        assert os.path.exists(f"{d}/f2")


def test_put(fs):
    from papai_unified_storage import put

    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        put(fs, f"{d}/f1", f"{d}/f2")

        with open(f"{d}/f2") as f:
            assert f.read() == "content"


def test_bytes_to_file(fs):
    from papai_unified_storage import write_to_file

    with TemporaryDirectory() as d:
        file_path = f"{d}/file"
        write_to_file(fs, file_path, b"content")

        with open(file_path, "rb") as f:
            assert f.read() == b"content"


def test_str_to_file(fs):
    from papai_unified_storage import write_to_file

    with TemporaryDirectory() as d:
        file_path = f"{d}/file"
        write_to_file(fs, file_path, "content")

        with open(file_path) as f:
            assert f.read() == "content"


@pytest.fixture
def json_data():
    return {"a": 1, "b": 2, "c": 3}


def test_loader(fs, json_data: dict):
    import json

    from papai_unified_storage import loader

    with TemporaryDirectory() as d:
        with open(f"{d}/json", "w") as file:
            json.dump(json_data, file)

        out_model: dict = loader(fs, file.name, json.load, mode="r")

        for key_item_1, key_item_2 in zip(json_data.items(), out_model.items()):
            if key_item_1[1] != key_item_2[1]:
                assert False
