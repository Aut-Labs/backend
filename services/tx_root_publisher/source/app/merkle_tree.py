import abc
import typing as t

class NodeMeta(metaclass=abc.ABCMeta):
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

    __slots__ = (
        'hash_value',
        'orig_value',
        'l_node',
        'r_node'
    )

    def __init__(self):
        self.orig_value = None
        self.hash_value = None
        self.l_node = None
        self.r_node = None

    @property
    def value(self) -> str:
        return "" if self.orig_value is None else self.orig_value

    @value.setter
    def value(self, x: str):
        if not self.__class__.is_valid(x):
            raise ValueError()
        self.orig_value = x
        self.hash_value = self.__class__.hash_func(self.orig_value)

    def __repr__(self):
        return f"[hash: 0x{self.hash_value.hex()}, orig: {self.orig_value}]"


def build(node_class: NodeMeta, values_: list[str]) -> t.Optional[NodeMeta]:

    def _build_tree(values: list[str]) -> t.Optional[NodeMeta]:
        if len(values) > 1:
            split: int = len(values) // 2
            node = node_class()
            node.l_node = _build_tree(values[0:split])
            node.r_node = _build_tree(values[split:len(values)])
            node.value = node.l_node.value + node_class.delim + node.r_node.value
            print(node)
            return node
        elif len(values) == 1:
            node = node_class()
            node.value = values[0]
            print(node, "<leaf>")
            return node
        else:
            return None

    return _build_tree(values_)


def test_node_meta():
    import hashlib
    class TestNode(NodeMeta):
        hash_func: t.Callable[[str], bytes] = lambda _: hashlib.sha256(_.encode()).digest()
        is_valid: t.Callable[[str], bool] = lambda _: True
        delim: str = ":"

    test_values: list[str] = ["a", "b", "c", "d", "e", "f", "g"]
    root_node: TestNode = build(TestNode, test_values)

    assert root_node.hash_value.hex() == 'c4a27b10cbb215a99a7696a5a2c4df82350f20223c7c7678a87dbf7c9e7eabf1'
    assert root_node.orig_value == 'a:b:c:d:e:f:g'


__all__ = (NodeMeta, build)
