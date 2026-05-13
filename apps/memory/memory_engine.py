"""
Main memory orchestration engine.
"""


class MemoryEngine:

    def __init__(self):

        self.memory_store = {}

    def save(
        self,
        key,
        value,
    ):

        """
        Save value into memory.
        """

        self.memory_store[key] = value

        return True

    def get(
        self,
        key,
        default=None,
    ):

        """
        Retrieve value from memory.
        """

        return self.memory_store.get(
            key,
            default,
        )

    def exists(
        self,
        key,
    ):

        """
        Check if key exists.
        """

        return key in self.memory_store

    def delete(
        self,
        key,
    ):

        """
        Delete memory key.
        """

        if key in self.memory_store:

            del self.memory_store[key]

            return True

        return False

    def keys(self):

        """
        Return all memory keys.
        """

        return list(
            self.memory_store.keys()
        )

    def values(self):

        """
        Return all memory values.
        """

        return list(
            self.memory_store.values()
        )

    def all(self):

        """
        Return complete memory store.
        """

        return self.memory_store

    def clear(self):

        """
        Clear all memory.
        """

        self.memory_store.clear()

        return True

    def count(self):

        """
        Return total memory items.
        """

        return len(
            self.memory_store
        )