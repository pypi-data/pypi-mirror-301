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

import pytest

from papai_unified_storage.storage import filesystem


@pytest.fixture()
def fs():
    return filesystem("file", auto_mkdir=False)


def test_dataframe_read_parquet(fs):
    import pandas as pd

    df = pd.DataFrame(
        {
            "one": [-1, 1, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )
    with TemporaryDirectory() as d:
        df.to_parquet(f"{d}/test.parquet")

        df_wrote_read = fs.read_dataset_from_parquet(f"{d}/test.parquet")

    assert df.equals(df_wrote_read)


def test_dataframe_write_parquet(fs):
    import pandas as pd

    df = pd.DataFrame(
        {
            "one": [-1, 1, 2.5],
            "two": ["foo", "bar", "baz"],
            "three": [True, False, True],
        },
        index=list("abc"),
    )

    with TemporaryDirectory() as d:
        fs.write_dataframe_to_parquet(f"{d}/test.parquet", df)

        df_wrote_read = pd.read_parquet(f"{d}/test.parquet")

        assert df.equals(df_wrote_read)


def test_get_file(fs):
    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        fs.get_file(f"{d}/f1", f"{d}/f2")

        with open(f"{d}/f2") as f:
            assert f.read() == "content"


def test_get_file_folder_creation(fs):
    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        fs.get_file(f"{d}/f1", f"{d}/a/b/c/f2")

        with open(f"{d}/a/b/c/f2") as f:
            assert f.read() == "content"


def test_list_files(fs):
    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        os.mkdir(f"{d}/d")
        with open(f"{d}/d/f2", "w") as f:
            f.write("content")

        assert set(fs.list_files(d, recursive=True)) == {f"{d}/f1", f"{d}/d/f2"}
        assert set(fs.list_files(d)) == {f"{d}/f1"}


def test_remove_files(fs):
    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        os.mkdir(f"{d}/d")
        with open(f"{d}/d/f2", "w") as f:
            f.write("content")

        fs.remove_files([f"{d}/f1", f"{d}/d/f2"])

        assert not os.path.exists(f"{d}/f1")
        assert not os.path.exists(f"{d}/d/f2")


def test_open_read_write(fs):
    with NamedTemporaryFile(mode="wb+") as file:
        with fs.open_for_writing(file.name) as f:
            f.write(b"content")

        with fs.open_for_reading(file.name) as f:
            assert f.read() == b"content"


def test_move(fs):
    with TemporaryDirectory() as d:
        # create a file
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        fs.move(f"{d}/f1", f"{d}/f2")

        assert not os.path.exists(f"{d}/f1")
        assert os.path.exists(f"{d}/f2")


def test_put(fs):
    with TemporaryDirectory() as d:
        with open(f"{d}/f1", "w") as f:
            f.write("content")

        fs.put(f"{d}/f1", f"{d}/f2")

        with open(f"{d}/f2") as f:
            assert f.read() == "content"


def test_bytes_to_file(fs):
    with TemporaryDirectory() as d:
        file_path = f"{d}/file"
        fs.write_to_file(file_path, b"content")

        with open(file_path, "rb") as f:
            assert f.read() == b"content"


def test_str_to_file(fs):
    with TemporaryDirectory() as d:
        file_path = f"{d}/file"
        fs.write_to_file(file_path, "content")

        with open(file_path) as f:
            assert f.read() == "content"


@pytest.fixture
def json_data():
    return {"a": 1, "b": 2, "c": 3}


def test_loader(fs, json_data: dict):
    import json

    with TemporaryDirectory() as d:
        with open(f"{d}/json", "w") as file:
            json.dump(json_data, file)

        out_model: dict = fs.loader(file.name, json.load, mode="r")

        for key_item_1, key_item_2 in zip(json_data.items(), out_model.items()):
            if key_item_1[1] != key_item_2[1]:
                assert False
