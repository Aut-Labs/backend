import abc
import hashlib
import typing as t


class _NodeMeta(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def hash_func(_: str) -> bytes:
        ...
    
    @staticmethod
    @abc.abstractmethod
    def is_valid(_: str) -> bool:
        ...

    @staticmethod
    @abc.abstractmethod
    def delim() -> str:
        ...


class TNode(_NodeMeta):
    hash_func: t.Callable[[str], bytes] = lambda _: hashlib.sha256(_.encode()).digest()
    is_valid: t.Callable[[str], bool] = lambda _: True
    delim: str = ":"

    __slots__ = (
        'hash_value',
        'orig_value',
        'l_node',
        'r_node'
    )

    hash_value: t.Optional[bytes]
    orig_value: t.Optional[dict]
    l_node: t.Optional['TNode']
    r_node: t.Optional['TNode']

    def __init__(self):
        self.orig_value = None
        self.hash_value = None
        self.l_node = None
        self.r_node = None

    @property
    def value(self):
        return "" if self.orig_value is None else self.orig_value
    
    @value.setter
    def value(self, x: str):
        self.orig_value = x
        self.hash_value = TNode.hash_func(self.orig_value)

    def __repr__(self):
        return f"[hash: {self.hash_value.hex()}, orig: {self.orig_value}]"


def build_tree(values: list[str]) -> t.Optional['TNode']:
    if len(values) > 1:
        split: int = len(values) // 2
        node = TNode()
        node.l_node = build_tree(values[0:split])
        node.r_node = build_tree(values[split:len(values)])
        print("left:", node.l_node)
        print("rifght:", node.r_node)
        node.value = node.l_node.value + TNode.delim + node.r_node.value
        return node
    elif len(values) == 1:
        node = TNode()
        node.value = values[0]
        return node
    else:
        return None
# todo: compare hashes 


def test():
    test_values: list[str] = ["a", "b", "c", "d", "e", "f", "g"]
    root_node: TNode = build_tree(test_values)
    print(root_node)


if __name__ == '__main__':
    test()
