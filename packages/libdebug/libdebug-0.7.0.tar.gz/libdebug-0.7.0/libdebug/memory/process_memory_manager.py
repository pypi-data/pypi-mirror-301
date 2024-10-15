#
# This file is part of libdebug Python library (https://github.com/libdebug/libdebug).
# Copyright (c) 2024 Roberto Alessandro Bertolini. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for details.
#

from __future__ import annotations


class ProcessMemoryManager:
    """A class that provides accessors to the memory of a process, through /proc/pid/mem."""

    def open(self: ProcessMemoryManager, process_id: int) -> None:
        """Initializes the ProcessMemoryManager."""
        self.process_id = process_id
        self._mem_file = None

    def _open(self: ProcessMemoryManager) -> None:
        self._mem_file = open(f"/proc/{self.process_id}/mem", "r+b", buffering=0)

    def read(self: ProcessMemoryManager, address: int, size: int) -> bytes:
        """Reads memory from the target process.

        Args:
            address (int): The address to read from.
            size (int): The number of bytes to read.

        Returns:
            bytes: The read bytes.
        """
        if not self._mem_file:
            self._open()

        self._mem_file.seek(address)
        return self._mem_file.read(size)

    def write(self: ProcessMemoryManager, address: int, data: bytes) -> None:
        """Writes memory to the target process.

        Args:
            address (int): The address to write to.
            data (bytes): The data to write.
        """
        if not self._mem_file:
            self._open()

        self._mem_file.seek(address)
        self._mem_file.write(data)

    def close(self: ProcessMemoryManager) -> None:
        """Closes the memory file."""
        if self._mem_file:
            self._mem_file.close()
            self._mem_file = None
