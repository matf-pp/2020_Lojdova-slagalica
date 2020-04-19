from src.Field import Field


class Puzzle:

    def __init__(self, list_of_states, x, y, size):
        r"""
        Arguments:
            list_of_states (list): List of all puzzle states.
            x, y (int): Upper left point of puzzle.
            size (int): Size of puzzle in pixels."""

        self._list_of_states = list_of_states
        self._x, self._y = x, y
        self._size = size  # size of puzzle. Can be 4,3 or 2
        self._n = size * size  # number of fields. Can be 16,9 or 4
        self._field_size = 100  # agreement by group
        self._dimension = self._field_size * self._size  # edge of puzzle in pixels

        self._current_state_index = 0
        self._number_of_states = len(list_of_states)
        self._fields = self.initialize_fields()

    def current_puzzle_state(self):
        tmp_state = self._list_of_states[self._current_state_index]
        only_num = tmp_state.split(":")

        tmp_state_list = []
        for i in range(self._n):
            tmp_state_list.append(int(only_num[i]))

        return tmp_state_list

    def next_puzzle_state(self):
        if self.is_last_state():
            return None

        next_state = self._list_of_states[self._current_state_index + 1]
        only_num = next_state.split(":")

        next_state_list = []
        for i in range(self._n):
            next_state_list.append(int(only_num[i]))

        return next_state_list

    def is_last_state(self):
        if(self._current_state_index == self._number_of_states - 1):
            return True

    def get_field_size(self):
        return self._field_size

    def get_puzzle_size(self):
        return self._size

    def get_puzzle_coordinates(self):
        return (self._x, self._y)

    def get_all_coordinates(self):
        r"""Count fields coordinates realtive to puzzle coordinates and field
        size."""

        coords_list = []
        field_size = self.get_field_size()

        row, col = 1, 0
        for i in range(self._n):
            tmp_x = self._x + col * field_size
            tmp_y = self._y + (row - 1) * field_size

            coords_list.append((tmp_x, tmp_y))

            if (i + 1) % self._size == 0:
                row += 1
                col = -1

            col += 1

        return coords_list

    def initialize_fields(self):
        r"""Schedule of fields in puzzle:

        [0]  [1]  [2]  [3]          [0]  [1]  [2]       [0]  [1]
        [4]  [5]  [6]  [7]          [3]  [4]  [5]       [2]  [3]
        [8]  [9]  [10] [11]         [6]  [7]  [8]
        [12] [13] [14] [15]

        Note: Field on position [3]
                    => It doesn't mean that field has value equals to number 3!

        Field with value 0 is the field that is moving all the time."""

        tmp_state = self.current_puzzle_state()
        coords_list = self.get_all_coordinates()

        fields = []
        for i in range(0, self._n):
            tmp_x, tmp_y = coords_list[i]
            tmp_val = tmp_state[i]

            fields.append(Field(tmp_x, tmp_y, tmp_val))

        return fields

    def states_difference(self, current_st, next_st):
        r'''index1 and index2 are indexes of fields in list self._fields
            that have changed between two puzzle states.
            new_val1 and new_val2 are values of these fields.'''

        for i in range(self._n):
            if current_st[i] != next_st[i]:
                # first changed field(index1, new_val1)
                index1 = i
                new_val1 = next_st[i]

                # second changed field(index2, new_val2)
                for j in range(i + 1, self._n):
                    if current_st[j] != next_st[j]:
                        index2 = j
                        new_val2 = next_st[j]
                        break
                break

        # Function returns variables in this order because of function
        # solve_puzzle in the file where we draw puzzle
        return index2, new_val1, index1, new_val2

    def states_change(self):
        r"""Function only changes values of two fields."""

        if self.is_last_state():
            return None
        else:
            index1, new_val1, index2, new_val2 = self.states_difference(
                self.current_puzzle_state(),
                self.next_puzzle_state())

            self._current_state_index += 1
            self._fields[index1].change_value(new_val1)
            self._fields[index2].change_value(new_val2)
            self._fields = self.initialize_fields()
