from Field import *


class Puzzle:

    def __init__(self, list_of_states, x, y, color, size):
        r"""list_of_states - list of all puzzle states
            (x,y)          - upper left point of puzzle
            color          - color of fields in puzzle
            size           - size of puzzle in pixels"""

        self._list_of_states = list_of_states
        self._x, self._y = x, y
        self._color = color
        self._size = size

        self._current_state_index = 0
        self._number_of_states = len(list_of_states)

        self._fields = self.initialize_fields()

    def current_puzzle_state(self):
        tmp_state = self._list_of_states[self._current_state_index]
        only_num = tmp_state.split(":")

        tmp_state_list = []
        for i in range(16):
            tmp_state_list.append(int(only_num[i]))

        return tmp_state_list

    def next_puzzle_state(self):
        if self.is_last_state():
            return None

        next_state = self._list_of_states[self._current_state_index + 1]
        only_num = next_state.split(":")

        next_state_list = []
        for i in range(16):
            next_state_list.append(int(only_num[i]))

        return next_state_list

    def is_last_state(self):
        if(self._current_state_index == self._number_of_states - 1):
            return True

    def get_current_color(self):
        return self._color

    def get_field_size(self):
        return self._size / 4

    def get_all_coordinates(self):
        r"""Count fields coordinates realtive to
        puzzle coordinates and field size."""

        coords_list = []
        field_size = self.get_field_size()

        row, col = 1, 0
        for i in range(16):
            tmp_x = self._x + col * field_size
            tmp_y = self._y + row * field_size

            coords_list.append((tmp_x, tmp_y))

            if (i + 1) % 4 == 0:
                row += 1
                col = -1

            col += 1

        return coords_list

    def initialize_fields(self):
        r"""
        Schedule of fields in puzzle:

        [0]  [1]  [2]  [3]
        [4]  [5]  [6]  [7]
        [8]  [9]  [10] [11]
        [12] [13] [14] [15]


        Note: Field on position [5]
                    => It doesn't mean that field has value equals to number 5!

        Field with value 0 is the field that is moving all the time."""

        tmp_state = self.current_puzzle_state()
        coords_list = self.get_all_coordinates()

        fields = []
        for i in range(0, 16):
            tmp_x, tmp_y = coords_list[i]
            tmp_val = tmp_state[i]

            fields.append(Field(tmp_x, tmp_y, tmp_val))

        return fields

    def current_puzzle_look(self):
        r"""This function will return pair:
            (Field,img_name_for_that_field)

            img_name = Field.value + "_" + self.color + '.png' """

        ret_list = []
        tmp_color = self.get_current_color()

        for i in range(16):
            color_name = "_" + tmp_color
            tmp_img_name = str(self._fields[i].vrednost) + color_name + ".png"

            ret_list.append((self._fields[i], tmp_img_name))

        return ret_list

    def states_difference(self, current_st, next_st):
        for i in range(16):
            if current_st[i] != next_st[i]:
                # First changed field
                index1 = i
                new_val1 = next_st[i]

                # Second changed field
                for j in range(i + 1, 16):
                    if current_st[j] != next_st[j]:
                        index2 = j
                        new_val2 = next_st[j]
                        break
                break

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
