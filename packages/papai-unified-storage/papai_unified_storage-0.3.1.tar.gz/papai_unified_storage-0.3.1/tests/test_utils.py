import os
from tempfile import TemporaryDirectory


def test_joinpath():
    from papai_unified_storage import joinpath

    assert joinpath("a", "b", "c") == "a/b/c"
    assert joinpath("a/", "/b/", "//c") == "a/b/c"
    assert joinpath("a/", "/b/", "//c/") == "a/b/c/"
    assert joinpath("a", ["b", "c"]) == ["a/b", "a/c"]
    assert joinpath(["a", "b"], ["c", "d"]) == ["a/c", "a/d", "b/c", "b/d"]
    assert joinpath(["a", "b"], "c") == ["a/c", "b/c"]
    assert joinpath("a", ["b", "c"], "d") == ["a/b/d", "a/c/d"]


def test_create_local_dir_tree_folder():
    from papai_unified_storage.utils import create_local_dir_tree

    with TemporaryDirectory() as d:
        create_local_dir_tree(f"{d}/a/b/c/")

        assert os.path.exists(f"{d}/a/b/c/")
