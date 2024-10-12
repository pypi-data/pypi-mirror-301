from __future__ import annotations

import io
import os
from typing import List, Optional, Union
from urllib.parse import urlparse

from typing_extensions import TypedDict

from ..._exceptions import EmptyFileError, InvalidFileURL


class TelaFileOptions(TypedDict, total=False):
    """
    Configuration options for processing the file.
    """

    range: Optional[List[int, int]]
    """
    The range of pages to parse from the file. e.g., [0, 1]
    """
    parser_type: Optional[str]
    """
    Defines the parser provider to be used for the file.
    """


class TelaFile:
    """
    Represents a file with support for various types including URLs, binary data, streams, and IO objects.

    Args:
        file (Union[str, bytes, io.IOBase]): The source of the file. Can be a URL string, bytes, or an open file-like object.
        options (Optional[dict], optional): Configuration options for processing the file. Defaults to None.

    Raises:
        InvalidFileURL: If the provided URL is not valid.
        EmptyFileError: If the provided file is empty.
        ValueError: If the file type is unsupported.
    """

    def __init__(
        self,
        file: Union[str, bytes, "io.IOBase"],
        options: Optional[TelaFileOptions] = None,
    ):
        self._file = file
        self._options = options or {}
        self._size: Optional[int] = None
        self._content_type: Optional[str] = None
        self.validate_file()

    @property
    def options(self) -> dict:
        """
        Retrieves the configuration options provided during instantiation.

        Returns:
            dict: The configuration options.
        """
        return self._options

    @property
    def is_url(self) -> bool:
        """
        Determines whether the file source is a valid URL.

        Returns:
            bool: `True` if the file source is a valid URL string, otherwise `False`.
        """
        return isinstance(self._file, str) and self.is_valid_url(self._file)

    @property
    def size(self) -> Optional[int]:
        """
        Gets the size of the file in bytes.

        Returns:
            Optional[int]: The size of the file if available, otherwise `None`.
        """
        return self._size

    @property
    def content_type(self) -> Optional[str]:
        """
        Gets the content type of the file.

        Returns:
            Optional[str]: The content type if available, otherwise `None`.
        """
        return self._content_type

    def get_uploadable_content(self):
        """
        Retrieves the content of the file in a format suitable for uploading.

        Returns:
            Union[str, io.BytesIO, io.BufferedReader, io.IOBase]: The uploadable content.

        Raises:
            ValueError: If the file type is unsupported.
        """
        if self.is_url and isinstance(self._file, str):
            return self._file

        if isinstance(self._file, bytes):
            return io.BytesIO(self._file)

        if isinstance(self._file, io.BufferedReader):
            self._file.seek(0)
            return self._file

        if isinstance(self._file, io.IOBase):
            if hasattr(self._file, "read"):
                return self._file

        raise ValueError(
            f"Unsupported file type: {type(self._file)}. Use a string with a URL, bytes, or an open file-like object."
        )

    def validate_file(self):
        """
        Validates the provided file based on its type.

        Raises:
            InvalidFileURL: If the file is a string but not a valid URL.
            EmptyFileError: If the file is empty.
            ValueError: If the file type is unsupported.
        """
        self._content_type = "application/octet-stream"

        if isinstance(self._file, str):
            if not self.is_valid_url(self._file):
                raise InvalidFileURL()

        elif isinstance(self._file, bytes):
            if len(self._file) == 0:
                raise EmptyFileError()
            self._size = len(self._file)

        elif isinstance(self._file, io.BufferedReader):
            self._file.seek(0, os.SEEK_END)
            self._size = self._file.tell()
            self._file.seek(0)
            if self._size == 0:
                raise EmptyFileError()

        elif isinstance(self._file, io.IOBase):
            if hasattr(self._file, "read"):
                self._file.seek(0, os.SEEK_END)
                self._size = self._file.tell()
                self._file.seek(0)

            if self._size == 0:
                raise EmptyFileError()
        else:
            raise ValueError(f"Unsupported file type: {type(self._file)}")

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Checks if the provided string is a valid URL.

        Args:
            url (str): The URL string to validate.

        Returns:
            bool: `True` if the URL is valid, otherwise `False`.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


def create_tela_file(file: Union[str, bytes, "io.IOBase"], options: Optional[TelaFileOptions] = None) -> TelaFile:
    """
    Creates a new `TelaFile` instance from the provided file input.

    Args:
        file (Union[str, bytes, io.IOBase]): The file input to create a `TelaFile` instance from.
        options (Optional[TelaFileOptions], optional): Configuration options for processing the file. Defaults to None.

    Returns:
        TelaFile: A new `TelaFile` instance.
    """
    return TelaFile(file, options)
