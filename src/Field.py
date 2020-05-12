class Field:

    def __init__(self, x, y, value):
        """
        Base constructor.

        Arguments:
            x (int): X coordinate of upper left corner of field.
            y (int): Y coordinate of upper left corner of field.
            value (int): Value (number) in that field.
        """

        self._x = x
        self._y = y
        self._value = value

    def change_value(self, new_value):
        """Setter."""
        self._value = new_value

    def current_value(self):
        """Getter."""
        return (self._value, self._x, self._y)
