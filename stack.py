class Stack:
    class Vertex:
        def __init__(self, elem, _prev=None):
            self.elem = elem
            self.prev = _prev

    def __init__(self, elem=None):
        self._top = self.Vertex(elem) if elem is not None else None

    def top(self):
        if self._top is None:
            return None
        return self._top.elem

    def next_to_top(self):
        if self._top is None or self._top.prev is None:
            return None
        return self._top.prev.elem

    def push(self, elem):
        self._top = self.Vertex(elem, self._top)

    def pop(self):
        if self._top is None:
            return None
        elem = self._top.elem
        self._top = self._top.prev
        return elem

    def to_list(self):
        current = self._top
        result = []
        while current is not None:
            result.append(current.elem)
            current = current.prev
        return result[::-1]