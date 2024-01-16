class Point():
    def __init__(self, x: int = 0, y: int = 0):
        self._x = x
        self._y = y

    def x(self) -> int:
        return self._x

    def y(self) -> int:
        return self._y

    def set_x(self, val: int):
        self._x = val

    def set_y(self, val: int):
        self._y = val

    def dist_to(self, other):
        delta = self - other
        return (delta._x ** 2 + delta._y ** 2) ** (1/2)

    def __add__(self, other):
        return Point(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        return Point(self._x - other._x, self._y - other._y)

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y
