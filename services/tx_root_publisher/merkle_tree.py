import hashlib
import typing as t

class Node:
    hash_value: t.Optional[bytes]
    source_value: t.Optional[str]
    left_node: t.Optional['Node']
    right_node: t.Optional['Node']

    def __init__(self):
        self.source_value = None
        self.hash_value = None
        self.left_node = None
        self.right_node = None

    def set_value(self, value: str):
        self.source_value = value
        self.hash_value = hashlib.sha256(value.encode()).digest()

    def get_value(self):
        return "" if self.source_value is None else self.source_value

    def __repr__(self):
        return f"[hash: {self.hash_value.hex()}, orig: {self.source_value}]"

def build_tree(values: list[str]):
    node = Node()
    if len(values) > 1:
        mid_point = len(values) // 2
        node = Node()
        node.left_node = build_tree(values[0:mid_point])
        node.right_node = build_tree(values[mid_point:len(values)])
        print("left", node.left_node)
        print("rifght", node.right_node)
        node.set_value(node.left_node.get_value() + ":" + node.right_node.get_value())
        return node
    elif len(values) == 1:
        node = Node()
        node.set_value(values[0])
        return node
    else:
        return None

def main():
    test_values = ["a", "b", "c", "d"]
    root_node = build_tree(test_values)
    print(root_node)


if __name__ == '__main__':
    main()
