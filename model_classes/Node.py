class Node:
    id = 0

    def __init__(self):
        self.id = Node.update_id()

    @classmethod
    def update_id(cls):
        cls.id += 1
        return cls.id
