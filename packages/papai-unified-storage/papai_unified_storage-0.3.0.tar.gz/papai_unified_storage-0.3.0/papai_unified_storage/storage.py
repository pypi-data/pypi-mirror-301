import fsspec
import pyarrow
import pyarrow.parquet

from .utils import create_local_dir_tree, dummy_fn


def filesystem(protocol, logging_function=dummy_fn, **storage_options):
    """Generate a supercharged fsspec storage instance for a given protocol.

    Parameters
    ----------
    protocol : str
        name of the protocol to use. See options at
        https://filesystem-spec.readthedocs.io/en/latest/api.html#built-in-implementations
    logging_function : Callable, optional
        Function to use to log operations. Must have a `msg` argument, by
        default dummy_fn, which does nothing.

    Returns
    -------
    Storage(fsspec.AbstractFileSystem)
        Supercharged fsspec storage instance.
    """
    fs_class = fsspec.get_filesystem_class(protocol)
    storage_class = _get_storage_instance(fs_class)
    fs = storage_class(logging_function, **storage_options)
    return fs


def _get_storage_instance(fs_class: type[fsspec.AbstractFileSystem]):
    class Storage(fs_class):
        def __init__(self, logging_function=dummy_fn, **storage_options):
            """Create storage proxy to a remote file system.

            Parameters
            ----------
            logging_function : Callable, optional
                Function to use to log operations. Must have a `msg` argument, by
                default dummy_fn, which does nothing.
            """
            self.log_fn = logging_function

            super().__init__(**storage_options)

        def get_file(self, remote_path, local_path):
            """Copy single remote file to local."""
            self.log_fn(
                msg=f"Copying remote file at {remote_path} to local at {local_path}"
            )
            create_local_dir_tree(local_path)
            super().get_file(remote_path, local_path)

        def put(self, local_path, remote_path):
            """Copy file(s) from local to remote.

            Copies a specific file or tree of files (if recursive=True). If
            rpath ends with a "/", it will be assumed to be a directory, and
            target files will go within.

            Calls put_file for each source.
            """
            self.log_fn(
                msg=f"Copying local file(s) at {local_path} to remote at {remote_path}"
            )
            super().put(local_path, remote_path)

        def open_for_writing(self, path, mode="wb"):
            self.log_fn(msg=f"Opening remote file at {path} for writing with {mode=}")
            return self.open(path, mode)

        def open_for_reading(self, path, mode="rb"):
            self.log_fn(msg=f"Opening remote file at {path} for reading with {mode=}")
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
            self.log_fn(
                msg=f"Moving remote file(s) from {source_path} to {destination_path}"
            )
            self.mv(source_path, destination_path)

        def list_files(self, path, recursive=False):
            if recursive is True:
                maxdepth = None
            else:
                maxdepth = 1

            self.log_fn(msg=f"Listing remote files at {path}")
            return self.find(path, maxdepth)

        def remove_files(self, paths, recursive=False):
            self.log_fn(msg=f"Removing remote file(s) at {paths}")
            self.rm(paths, recursive)

        def read_dataset_from_parquet(self, path):
            self.log_fn(msg=f"Reading remote dataset from {path}")
            df = (
                pyarrow.parquet.ParquetDataset(path, filesystem=self)
                .read_pandas()
                .to_pandas()
            )
            return df

        def write_dataframe_to_parquet(self, path, df):
            self.log_fn(msg=f"Writing dataset to remote file at {path}")
            table = pyarrow.Table.from_pandas(df)
            pyarrow.parquet.write_table(table, path, filesystem=self)

        def loader(self, path, load_method, mode="rb"):
            self.log_fn(
                msg=f"Loading object with {load_method.__name__} from remote file at {path}"
            )
            with self.open_for_reading(path, mode) as f:
                return load_method(f)

        def write_to_file(self, path, content):
            if isinstance(content, str):
                mode = "w"
            else:
                mode = "wb"

            self.log_fn(msg=f"Writing content to remote file at {path}")

            with self.open_for_writing(path, mode) as f:
                f.write(content)

    return Storage
