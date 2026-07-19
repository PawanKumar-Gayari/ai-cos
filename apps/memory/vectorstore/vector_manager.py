"""
Vector storage manager.
"""


class VectorManager:

    def __init__(self):

        self.vectors = []

    def add_vector(
        self,
        item_id,
        embedding,
        metadata=None,
    ):

        vector_item = {

            "id": item_id,

            "embedding": embedding,

            "metadata": metadata or {},
        }

        self.vectors.append(
            vector_item
        )

        return vector_item

    def get_all_vectors(self):

        return self.vectors

    def count(self):

        return len(
            self.vectors
        )

    def clear(self):

        self.vectors.clear()

        return True

    def search_by_id(
        self,
        item_id,
    ):

        for item in self.vectors:

            if item["id"] == item_id:

                return item

        return None