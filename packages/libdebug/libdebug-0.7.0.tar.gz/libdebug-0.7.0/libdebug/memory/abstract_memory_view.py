#
# This file is part of libdebug Python library (https://github.com/libdebug/libdebug).
# Copyright (c) 2023-2024 Roberto Alessandro Bertolini, Gabriele Digregorio. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from collections.abc import MutableSequence

from libdebug.debugger.internal_debugger_instance_manager import provide_internal_debugger
from libdebug.liblog import liblog
from libdebug.utils.search_utils import find_all_overlapping_occurrences


class AbstractMemoryView(MutableSequence, ABC):
    """An abstract memory interface for the target process.

    An implementation of class must be used to read and write memory of the target process.
    """

    def __init__(self: AbstractMemoryView) -> None:
        """Initializes the MemoryView."""
        self._internal_debugger = provide_internal_debugger(self)

    @abstractmethod
    def read(self: AbstractMemoryView, address: int, size: int) -> bytes:
        """Reads memory from the target process.

        Args:
            address (int): The address to read from.
            size (int): The number of bytes to read.

        Returns:
            bytes: The read bytes.
        """

    @abstractmethod
    def write(self: AbstractMemoryView, address: int, data: bytes) -> None:
        """Writes memory to the target process.

        Args:
            address (int): The address to write to.
            data (bytes): The data to write.
        """

    def find(
        self: AbstractMemoryView,
        value: bytes | str | int,
        file: str = "all",
        start: int | None = None,
        end: int | None = None,
    ) -> list[int]:
        """Searches for the given value in the specified memory maps of the process.

        The start and end addresses can be used to limit the search to a specific range.
        If not specified, the search will be performed on the whole memory map.

        Args:
            value (bytes | str | int): The value to search for.
            file (str): The backing file to search the value in. Defaults to "all", which means all memory.
            start (int | None): The start address of the search. Defaults to None.
            end (int | None): The end address of the search. Defaults to None.

        Returns:
            list[int]: A list of offset where the value was found.
        """
        if isinstance(value, str):
            value = value.encode()
        elif isinstance(value, int):
            value = value.to_bytes(1, sys.byteorder)

        occurrences = []
        if file == "all" and start is None and end is None:
            for vmap in self._internal_debugger.maps:
                liblog.debugger(f"Searching in {vmap.backing_file}...")
                try:
                    memory_content = self.read(vmap.start, vmap.end - vmap.start)
                except (OSError, OverflowError):
                    # There are some memory regions that cannot be read, such as [vvar], [vdso], etc.
                    continue
                occurrences += find_all_overlapping_occurrences(value, memory_content, vmap.start)
        elif file == "all" and start is not None and end is None:
            for vmap in self._internal_debugger.maps:
                if vmap.end > start:
                    liblog.debugger(f"Searching in {vmap.backing_file}...")
                    read_start = max(vmap.start, start)
                    try:
                        memory_content = self.read(read_start, vmap.end - read_start)
                    except (OSError, OverflowError):
                        # There are some memory regions that cannot be read, such as [vvar], [vdso], etc.
                        continue
                    occurrences += find_all_overlapping_occurrences(value, memory_content, read_start)
        elif file == "all" and start is None and end is not None:
            for vmap in self._internal_debugger.maps:
                if vmap.start < end:
                    liblog.debugger(f"Searching in {vmap.backing_file}...")
                    read_end = min(vmap.end, end)
                    try:
                        memory_content = self.read(vmap.start, read_end - vmap.start)
                    except (OSError, OverflowError):
                        # There are some memory regions that cannot be read, such as [vvar], [vdso], etc.
                        continue
                    occurrences += find_all_overlapping_occurrences(value, memory_content, vmap.start)
        elif file == "all" and start is not None and end is not None:
            # Search in the specified range, hybrid mode
            start = self._internal_debugger.resolve_address(start, "hybrid", True)
            end = self._internal_debugger.resolve_address(end, "hybrid", True)
            liblog.debugger(f"Searching in the range {start:#x}-{end:#x}...")
            memory_content = self.read(start, end - start)
            occurrences = find_all_overlapping_occurrences(value, memory_content, start)
        else:
            maps = self._internal_debugger.maps.filter(file)
            start = self._internal_debugger.resolve_address(start, file, True) if start is not None else maps[0].start
            end = self._internal_debugger.resolve_address(end, file, True) if end is not None else maps[-1].end - 1

            liblog.debugger(f"Searching in the range {start:#x}-{end:#x}...")
            memory_content = self.read(start, end - start)

            occurrences = find_all_overlapping_occurrences(value, memory_content, start)

        return occurrences

    def __getitem__(self: AbstractMemoryView, key: int | slice | str | tuple) -> bytes:
        """Read from memory, either a single byte or a byte string.

        Args:
            key (int | slice | str | tuple): The key to read from memory.
        """
        return self._manage_memory_read_type(key)

    def __setitem__(self: AbstractMemoryView, key: int | slice | str | tuple, value: bytes) -> None:
        """Write to memory, either a single byte or a byte string.

        Args:
            key (int | slice | str | tuple): The key to write to memory.
            value (bytes): The value to write.
        """
        if not isinstance(value, bytes):
            raise TypeError("Invalid type for the value to write to memory. Expected bytes.")
        self._manage_memory_write_type(key, value)

    def _manage_memory_read_type(
        self: AbstractMemoryView,
        key: int | slice | str | tuple,
        file: str = "hybrid",
    ) -> bytes:
        """Manage the read from memory, according to the typing.

        Args:
            key (int | slice | str | tuple): The key to read from memory.
            file (str, optional): The user-defined backing file to resolve the address in. Defaults to "hybrid" (libdebug will first try to solve the address as an absolute address, then as a relative address w.r.t. the "binary" map file).
        """
        if isinstance(key, int):
            address = self._internal_debugger.resolve_address(key, file, skip_absolute_address_validation=True)
            try:
                return self.read(address, 1)
            except OSError as e:
                raise ValueError("Invalid address.") from e
        elif isinstance(key, slice):
            if isinstance(key.start, str):
                start = self._internal_debugger.resolve_symbol(key.start, file)
            else:
                start = self._internal_debugger.resolve_address(key.start, file, skip_absolute_address_validation=True)

            if isinstance(key.stop, str):
                stop = self._internal_debugger.resolve_symbol(key.stop, file)
            else:
                stop = self._internal_debugger.resolve_address(key.stop, file, skip_absolute_address_validation=True)

            if stop < start:
                raise ValueError("Invalid slice range.")

            try:
                return self.read(start, stop - start)
            except OSError as e:
                raise ValueError("Invalid address.") from e
        elif isinstance(key, str):
            address = self._internal_debugger.resolve_symbol(key, file)

            return self.read(address, 1)
        elif isinstance(key, tuple):
            return self._manage_memory_read_tuple(key)
        else:
            raise TypeError("Invalid key type.")

    def _manage_memory_read_tuple(self: AbstractMemoryView, key: tuple) -> bytes:
        """Manage the read from memory, when the access is through a tuple.

        Args:
            key (tuple): The key to read from memory.
        """
        if len(key) == 3:
            # It can only be a tuple of the type (address, size, file)
            address, size, file = key
            if not isinstance(file, str):
                raise TypeError("Invalid type for the backing file. Expected string.")
        elif len(key) == 2:
            left, right = key
            if isinstance(right, str):
                # The right element can only be the backing file
                return self._manage_memory_read_type(left, right)
            elif isinstance(right, int):
                # The right element must be the size
                address = left
                size = right
                file = "hybrid"
        else:
            raise TypeError("Tuple must have 2 or 3 elements.")

        if not isinstance(size, int):
            raise TypeError("Invalid type for the size. Expected int.")

        if isinstance(address, str):
            address = self._internal_debugger.resolve_symbol(address, file)
        elif isinstance(address, int):
            address = self._internal_debugger.resolve_address(address, file, skip_absolute_address_validation=True)
        else:
            raise TypeError("Invalid type for the address. Expected int or string.")

        try:
            return self.read(address, size)
        except OSError as e:
            raise ValueError("Invalid address.") from e

    def _manage_memory_write_type(
        self: AbstractMemoryView,
        key: int | slice | str | tuple,
        value: bytes,
        file: str = "hybrid",
    ) -> None:
        """Manage the write to memory, according to the typing.

        Args:
            key (int | slice | str | tuple): The key to read from memory.
            value (bytes): The value to write.
            file (str, optional): The user-defined backing file to resolve the address in. Defaults to "hybrid" (libdebug will first try to solve the address as an absolute address, then as a relative address w.r.t. the "binary" map file).
        """
        if isinstance(key, int):
            address = self._internal_debugger.resolve_address(key, file, skip_absolute_address_validation=True)
            try:
                self.write(address, value)
            except OSError as e:
                raise ValueError("Invalid address.") from e
        elif isinstance(key, slice):
            if isinstance(key.start, str):
                start = self._internal_debugger.resolve_symbol(key.start, file)
            else:
                start = self._internal_debugger.resolve_address(key.start, file, skip_absolute_address_validation=True)

            if key.stop is not None:
                if isinstance(key.stop, str):
                    stop = self._internal_debugger.resolve_symbol(key.stop, file)
                else:
                    stop = self._internal_debugger.resolve_address(
                        key.stop,
                        file,
                        skip_absolute_address_validation=True,
                    )

                if stop < start:
                    raise ValueError("Invalid slice range")

                if len(value) != stop - start:
                    liblog.warning(f"Mismatch between slice width and value size, writing {len(value)} bytes.")

            try:
                self.write(start, value)
            except OSError as e:
                raise ValueError("Invalid address.") from e

        elif isinstance(key, str):
            address = self._internal_debugger.resolve_symbol(key, file)

            self.write(address, value)
        elif isinstance(key, tuple):
            self._manage_memory_write_tuple(key, value)
        else:
            raise TypeError("Invalid key type.")

    def _manage_memory_write_tuple(self: AbstractMemoryView, key: tuple, value: bytes) -> None:
        """Manage the write to memory, when the access is through a tuple.

        Args:
            key (tuple): The key to read from memory.
            value (bytes): The value to write.
        """
        if len(key) == 3:
            # It can only be a tuple of the type (address, size, file)
            address, size, file = key
            if not isinstance(file, str):
                raise TypeError("Invalid type for the backing file. Expected string.")
        elif len(key) == 2:
            left, right = key
            if isinstance(right, str):
                # The right element can only be the backing file
                self._manage_memory_write_type(left, value, right)
                return
            elif isinstance(right, int):
                # The right element must be the size
                address = left
                size = right
                file = "hybrid"
        else:
            raise TypeError("Tuple must have 2 or 3 elements.")

        if not isinstance(size, int):
            raise TypeError("Invalid type for the size. Expected int.")

        if isinstance(address, str):
            address = self._internal_debugger.resolve_symbol(address, file)
        elif isinstance(address, int):
            address = self._internal_debugger.resolve_address(address, file, skip_absolute_address_validation=True)
        else:
            raise TypeError("Invalid type for the address. Expected int or string.")

        if len(value) != size:
            liblog.warning(f"Mismatch between specified size and actual value size, writing {len(value)} bytes.")

        try:
            self.write(address, value)
        except OSError as e:
            raise ValueError("Invalid address.") from e

    def __delitem__(self: AbstractMemoryView, key: int | slice | str | tuple) -> None:
        """MemoryView doesn't support deletion."""
        raise NotImplementedError("MemoryView doesn't support deletion")

    def __len__(self: AbstractMemoryView) -> None:
        """MemoryView doesn't support length."""
        raise NotImplementedError("MemoryView doesn't support length")

    def insert(self: AbstractMemoryView, index: int, value: int) -> None:
        """MemoryView doesn't support insertion."""
        raise NotImplementedError("MemoryView doesn't support insertion")
