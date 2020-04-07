class Field:

    '''
    (x,y)     - upper left point of field
    value     - value(number) in that field
    '''
    def __init__(self, x, y, value):
        self._x = x
        self._y = y
        self._value = value

    def change_value(self, new_value):
        self._value = new_value

    def current_value(self):
        return (self._value, self._x, self.y)


# ----------------------------------------------------


class Puzzle:

    '''
    list_of_states - list of all puzzle states
    (x,y)          - upper left point of puzzle
    color          - color of fields in puzzle
    size           - size of puzzle in pixels
    '''

    def __init__(self, list_of_states, x, y, color, size):
        self._list_of_states = list_of_states
        self._x = x
        self._y = y
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
            tmp_state_list.append(int(only_num[i], 10))

        return tmp_state_list

    def next_puzzle_state(self):
        next_state = self._list_of_states[self._current_state_index+1]
        only_num = next_state.split(":")

        next_state_list = []
        for i in range(16):
            next_state_list.append(int(only_num[i], 10))

        return next_state_list

    def is_last_state(self):
        if(self._current_state_index == self._number_of_states-1):
            return True

    def get_current_color(self):
        return self._color

    def get_field_size(self):
        return self._size / 4

    '''
        Count fields coordinates realtive to puzzle coordinates and field size.
    '''
    def get_all_coordinates(self):
        coords_list = []

        a = self.get_field_size()

        row = 1
        colon = 0
        for i in range(16):
            tmp_x = self._x + colon*a
            tmp_y = self._y + row*a

            coords_list.append((tmp_x, tmp_y))

            if (i+1) % 4 == 0:
                row += 1
                colon = -1

            colon += 1

        return coords_list

    '''
        Schedule of fields in puzzle:

        [0]  [1]  [2]  [3]
        [4]  [5]  [6]  [7]
        [8]  [9]  [10] [11]
        [12] [13] [14] [15]


        Note: Field on position [5]
                    => It doesn't mean that field has value equals to number 5!

        Field with value 0 is the field that is moving all the time.
    '''

    def initialize_fields(self):
        tmp_state = self.current_puzzle_state()
        coords_list = self.get_all_coordinates()

        list_of_fields = []
        for i in range(0, 16):
            tmp_x = coords_list[i][0]
            tmp_y = coords_list[i][1]
            tmp_val = tmp_state[i]

            list_of_fields.append(Field(tmp_x, tmp_y, tmp_val))

        return list_of_fields

    '''
        This function will return pair:
            (Field,img_name_for_that_field)

            img_name_for_that_field = Field.value + "_" + self.color + ".png"
    '''
    def current_puzzle_look(self):
        ret_list = []
        tmp_color = self.get_current_color()

        for i in range(16):
            tmp_img_name = str(self._fields[i].vrednost) + "_" + tmp_color + \
                        ".png"

            ret_list.append((self._fields[i], tmp_img_name))

        return ret_list

    def states_difference(self, current, next):
        for i in range(16):
            if current[i] != next[i]:
                # First changed field
                index1 = i
                new_val1 = next[i]

                # Second changed field
                for j in range(i + 1, 16):
                    if current[j] != next[j]:
                        index2 = j
                        new_val2 = next[j]
                        break
                break

        return (index2, new_val1, index1, new_val2)

    '''
        Function only change values of two fields.
    '''
    def promena_stanja(self):

        if(self.is_last_state()):
            return None
        else:
            (index1, nova_vr1, index2, nova_vr2) = \
                self.states_difference(
                    self.current_puzzle_state(), self.next_puzzle_state())

            self.indeks_trenutnog += 1
            self._fields[index1].promeni_vrednost(nova_vr1)
            self._fields[index2].promeni_vrednost(nova_vr2)
            self._fields = self.initialize_fields()
