class Field:

    def __init__(self, x, y, value):
        r"""(x,y)     - upper left point of field
            value     - value(number) in that field"""

        self._x = x
        self._y = y
        self._value = value

    def change_value(self, new_value):
        self._value = new_value

    def current_value(self):
        return (self._value, self._x, self._y)
