from collections.abc import Callable

import fsspec
import pyarrow
import pyarrow.parquet

from .utils import create_local_dir_tree


def filesystem(protocol, logging_function=None, **storage_options):
    fs_class = fsspec.get_filesystem_class(protocol)
    storage_class = _get_storage_instance(fs_class)
    fs = storage_class(logging_function, **storage_options)
    return fs


def _get_storage_instance(fs_class: type[fsspec.AbstractFileSystem]):
    class Storage(fs_class):
        def __init__(self, logging_function: Callable | None, **storage_options):
            self.logging_function = logging_function
            super().__init__(**storage_options)

        def get_file(self, remote_path, local_path):
            """Copy single remote file to local."""
            create_local_dir_tree(local_path)
            super().get_file(remote_path, local_path)

        def put(self, local_path, remote_path):
            """Copy file(s) from local to remote.

            Copies a specific file or tree of files (if recursive=True). If
            rpath ends with a "/", it will be assumed to be a directory, and
            target files will go within.

            Calls put_file for each source.
            """
            super().put(local_path, remote_path)

        def open_for_writing(self, path, mode="wb"):
            return self.open(path, mode)

        def open_for_reading(self, path, mode="rb"):
            return self.open(path, mode)

        def move(self, source_path, destination_path):
            """Move file(s) from one location to another.

            This fails if the target file system is not capable of creating the
            directory, for example if it is write-only or if auto_mkdir=False. There is
            no command line equivalent of this scenario without an explicit mkdir to
            create the new directory.
            See https://filesystem-spec.readthedocs.io/en/latest/copying.html for more
            information.
            """
            self.mv(source_path, destination_path)

        def list_files(self, path, recursive=False):
            if recursive is True:
                maxdepth = None
            else:
                maxdepth = 1

            return self.find(path, maxdepth)

        def remove_files(self, paths, recursive=False):
            self.rm(paths, recursive)

        def read_dataset_from_parquet(self, path):
            df = (
                pyarrow.parquet.ParquetDataset(path, filesystem=self)
                .read_pandas()
                .to_pandas()
            )
            return df

        def write_dataframe_to_parquet(self, path, df):
            table = pyarrow.Table.from_pandas(df)
            pyarrow.parquet.write_table(table, path, filesystem=self)

        def loader(self, path, load_method, mode="rb"):
            with self.open_for_reading(path, mode) as f:
                return load_method(f)

        def write_to_file(self, path, content):
            if isinstance(content, str):
                mode = "w"
            else:
                mode = "wb"

            with self.open_for_writing(path, mode) as f:
                f.write(content)

    return Storage
