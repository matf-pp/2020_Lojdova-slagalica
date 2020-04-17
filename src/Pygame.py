import multiprocessing
import pygame
import time
import sys
import os

sys.path.extend([os.path.join(os.getcwd(), "utils")])
from utils import is_solvable, serialize

from Astar import Astar
from IDAstar import IDAstar
from BaseSolver import BaseSolver
from WAstar import WAstar
from Field import Field
from Puzzle import Puzzle
from tkinter import *

# font related
FONT_COLOR = (31, 33, 43)
FONT_SIZE = 24
FONT = "Courier"

# scene related
TOP_OFFSET = 0
RIGHT_OFFSET = 0
BOTTOM_OFFSET = 0
LEFT_OFFSET = 0
VERTICAL_OFFSET = TOP_OFFSET + BOTTOM_OFFSET
HORIZONTAL_OFFSET = LEFT_OFFSET + RIGHT_OFFSET
ANIMATION_FIELD_SPEED = 2
BACKGROUND_COLOR = (255, 255, 255)

# puzzle related
PUZZLE_IMAGES_PATH = os.path.join(".", "src", "Numbers")
PUZZLE_IMAGES_EXT = ".png"
PUZZLE_DIST = 25
FIELD_SIZE = 100


class ProcessSolver(multiprocessing.Process):
    def __init__(self, solver, queue, args=None):
        super().__init__(daemon=True, args=args)

        self._solver = solver
        self._queue = queue

    def run(self):
        state, puzzle_solvability, puzzle_x, puzzle_y = self._args

        if puzzle_solvability:
            result = self._solver.solve(state)
            puzzle = Puzzle(result[1][1],
                            puzzle_x, puzzle_y,
                            len(state))
        else:
            puzzle = Puzzle([serialize(state)],
                            puzzle_x, puzzle_y,
                            len(state))

        self._queue.put(puzzle)


class Direction:
    r"""Enum class for all possible directions of field movement."""

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4


def define_move_direction(puzzle_size, index_src, index_dest, value_src,
                          value_dest):
    r"""Definens in which direction empty field of puzzle should be moved.

    If the difference between source and destinantion fields(in our case
    empty and exchage fields) is equal to puzzle size then our fields are
    one above the other. In other case they are side by side.

    The field with a smaller index is above the other (or on the left side
    if they stands side by side).

    With all of these we can define position of the empty field relative
    to exchange field."""

    if_cond = value_src == 0 and index_src < index_dest
    if_cond = if_cond or (value_dest == 0 and index_dest < index_src)

    if abs(index_src - index_dest) == puzzle_size:
        return Direction.DOWN if if_cond else Direction.UP
    else:
        return Direction.RIGHT if if_cond else Direction.LEFT


def get_zero_and_exchange_field(exchange_index, zero_index, value,
                                current_state):
    r"""Function defines which index corresponds to exchange and which
    corresponds to empty (zero) field.

    If the value of first field is zero, then zero field stands in position
    of the first index in current state and exchange field belongs to other
    index.

    In other case exchange field is at the first and zero field at the second
    index position."""

    if value != 0:
        exchange_index, zero_index = zero_index, exchange_index

    return current_state[zero_index], current_state[exchange_index]


def move_field(current_state, zero_field, exchange_field, target,
               move_direction, puzzle_x, puzzle_y):
    r"""At first, function determines direction in which empty field
    is seted to be moved.

    Then, function swaps fields by increasing/decresaing coordinates
    of either empty and exchange field. If the move direction is up or down
    only `y` coordinate should be changed (in other case only `x` coordinate
    should be changed for both fields). It is enough to check only one field
    coordinate (in our case we check empty field coordinate).

    If zero field should move up, its `y` coordinate should decrease, and the
    sign variable is set to be negative number. With same logic we define sign
    variable for other directions.

    When we define target coordinate, its value and direction of move,
    main loop of this function changes both coordinates of empty and exchange
    field by increasing/decreasing them for the value of sign variable."""

    if move_direction == Direction.UP:
        zero_field_variable = zero_field._y
        sign = -ANIMATION_FIELD_SPEED
    elif move_direction == Direction.DOWN:
        zero_field_variable = zero_field._y
        sign = ANIMATION_FIELD_SPEED
    elif move_direction == Direction.LEFT:
        zero_field_variable = zero_field._x
        sign = -ANIMATION_FIELD_SPEED
    else:
        zero_field_variable = zero_field._x
        sign = ANIMATION_FIELD_SPEED

    if move_direction in [Direction.UP, Direction.LEFT]:
        while zero_field_variable > target:
            pygame.display.update()
            for field in current_state:
                value = field._value
                field_x, field_y = field._x, field._y

                if value == 0:
                    zero_field_variable += sign
                elif value == exchange_field._value:
                    if move_direction in [Direction.UP]:
                        exchange_field._y += (-sign)
                    else:
                        exchange_field._x += (-sign)
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))

                    pygame.draw.rect(screen,
                                     BACKGROUND_COLOR,
                                     (field_x, field_y,
                                      FIELD_SIZE, FIELD_SIZE))

                    screen.blit(img, (exchange_field._x, exchange_field._y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (field_x, field_y))
    else:
        while zero_field_variable < target:
            pygame.display.update()
            for field in current_state:
                value = field._value
                field_x, field_y = field._x, field._y

                pygame.draw.rect(screen,
                                 BACKGROUND_COLOR,
                                 (field_x, field_y,
                                  FIELD_SIZE, FIELD_SIZE))

                if value == 0:
                    zero_field_variable += sign
                elif value == exchange_field._value:
                    if move_direction in [Direction.DOWN]:
                        exchange_field._y += (-sign)
                    else:
                        exchange_field._x += (-sign)
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (exchange_field._x, exchange_field._y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (field_x, field_y))


def draw_puzzle(current_state, puzzle_solvability):
    r"""Function iterates through current state of the puzzle
    and draws all fields as a images.

    In the place of empty(zero) field nothing should be draw so we
    skip the field with value 0."""

    for field in current_state:
        value = field._value
        field_x, field_y = field._x, field._y

        if value == 0:
            continue

        img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                             str(value) + PUZZLE_IMAGES_EXT))
        screen.blit(img, (field_x, field_y))

    # when puzzle doesn't have solution
    if not puzzle_solvability:
        img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, "stop.png"))
        img_width, img_height = img.get_size()
        screen.blit(img, (scene_width // 2 - img_width // 2,
                          scene_height // 2 - img_height // 2))


def solve_puzzle(puzzle, puzzle_solvability):
    r"""Function gets current state of puzzle, draws puzzle, gets difference
    between current and the next state of the puzzle, and makes transition
    from current to the next state."""

    current_state = puzzle._fields
    puzzle_x, puzzle_y = puzzle.get_puzzle_coordinates()

    # draw state without animation
    draw_puzzle(current_state, puzzle_solvability)

    # get difference between current and next state
    if puzzle.next_puzzle_state() is not None:
        index1, value1, index2, value2 = puzzle.states_difference(
            puzzle.current_puzzle_state(),
            puzzle.next_puzzle_state())
    else:
        return False  # no further moves

    # define direction of field movement
    move_direction = define_move_direction(puzzle.get_puzzle_size(),
                                           index1,
                                           index2,
                                           value1,
                                           value2)

    # get fields for animation
    exchange_field, zero_field = \
        get_zero_and_exchange_field(index1, index2, value1, current_state)

    # define stop targets for animation
    target_x, target_y = exchange_field._x, exchange_field._y

    # move zero field to seted direction
    if move_direction == Direction.UP:
        move_field(current_state, zero_field, exchange_field,
                   target_y, Direction.UP, puzzle_x, puzzle_y)
    elif move_direction == Direction.DOWN:
        move_field(current_state, zero_field, exchange_field,
                   target_y, Direction.DOWN, puzzle_x, puzzle_y)
    elif move_direction == Direction.RIGHT:
        move_field(current_state, zero_field, exchange_field,
                   target_x, Direction.RIGHT, puzzle_x, puzzle_y)
    elif move_direction == Direction.LEFT:
        move_field(current_state, zero_field, exchange_field,
                   target_x, Direction.LEFT, puzzle_x, puzzle_y)
    else:
        raise ValueError("Invalid move_direction")  # should never happen

    puzzle.states_change()
    current_state = puzzle._fields

    return True  # valid move has happened


def init_scene(scene_width, scene_height):
    r"""Initializing scene and returning Pygame's `Surface` object. Scene
    contains:
        (1) text boxes -- done here
        (2) proper background color -- done here
        (3) puzzles -- done separately

    Arguments:
        scene_width, scene_height (ints): Dimension of scene window in pixels.

    Returns:
        screen (Surface): Object for scene manipulation."""

    pygame.init()
    screen = pygame.display.set_mode((scene_width, scene_height))
    pygame.display.set_caption("Loyd Puzzle A* Solvers")

    icon = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, "puzzle.png"))
    pygame.display.set_icon(icon)
    screen.fill(BACKGROUND_COLOR)

    # font = pygame.font.Font("./src/fonts/calibri.ttf", FONT_SIZE)  # test font 1
    # font = pygame.font.Font("./src/fonts/Pacifico.ttf", FONT_SIZE)  # test font 2
    # font = pygame.font.Font("./src/fonts/Xcelsion Italic.ttf", FONT_SIZE)  # test font 3
    # font = pygame.font.Font("./src/fonts/XpressiveBlack Regular.ttf", FONT_SIZE)  # test font 4
    # font = pygame.font.Font("./src/fonts/Yes_Union.ttf", FONT_SIZE)  # test font 5
    font = pygame.font.Font("./src/fonts/y.n.w.u.a.y.ttf", FONT_SIZE)  # test font 6
    text_upper_left = font.render("WA* dynamic", True, FONT_COLOR,
                                  BACKGROUND_COLOR)
    textrect_upper_left = text_upper_left.get_rect()
    textrect_upper_left.center = (LEFT_OFFSET + len(state) * FIELD_SIZE // 2,
                                  TOP_OFFSET + (len(state)) * FIELD_SIZE + FONT_SIZE // 2)
    screen.blit(text_upper_left, textrect_upper_left)

    text_upper_right = font.render("WA* static", True, FONT_COLOR,
                                   BACKGROUND_COLOR)
    textrect_upper_right = text_upper_right.get_rect()
    textrect_upper_right.center = (scene_width - RIGHT_OFFSET - len(state) * FIELD_SIZE // 2,
                                   TOP_OFFSET + (len(state)) * FIELD_SIZE + FONT_SIZE // 2)
    screen.blit(text_upper_right, textrect_upper_right)

    return screen


def user_menu():
    r"""function draws basic tkinter window that allows user to select
    which algorithms dose he wants to compare"""

    # this function creates string that contains names of all algorithms that
    # user wants to compare
    def get_algorithms():

        global algorithms

        # special variables in tkinter library can return their value
        # only with get method of the varible
        if WAstar_dynamic_variable.get():
            algorithms += "WAstar_dynamic,"
        if WAstar_static_variable.get():
            algorithms += "WAstar_static,"
        if IDAstar_variable.get():
            algorithms += "IDAstar,"
        if Astar_variable.get():
            algorithms += "Astar,"

        algorithms = algorithms[0:len(algorithms)-1]

    # this part creates tkinter window
    root = Tk()
    root.geometry('400x300')

    # special tkinter variables that contains informations from checkboxes
    WAstar_dynamic_variable = BooleanVar()
    WAstar_static_variable = BooleanVar()
    IDAstar_variable = BooleanVar()
    Astar_variable = BooleanVar()

    # create new Checkbutton and its attributes
    WAstar_dynamic_box = Checkbutton(root, text="WAstar dynamic algorithm",
                                     variable=WAstar_dynamic_variable,
                                     onvalue = True,
                                     offvalue = False)
    WAstar_dynamic_box.config(font=(FONT, 14))
    WAstar_dynamic_box.place(relx = 0.01, rely = 0.01)

    WAstar_static_box = Checkbutton(root, text="WAstar static algorithm",
                                     variable=WAstar_static_variable,
                                     onvalue = True,
                                     offvalue = False)
    WAstar_static_box.config(font=(FONT, 14))
    WAstar_static_box.place(relx = 0.01, rely = 0.1)

    IDAstar_box = Checkbutton(root, text="IDAstar algorithm",
                                     variable = IDAstar_variable,
                                     onvalue = True,
                                     offvalue = False)
    IDAstar_box.config(font=(FONT, 14))
    IDAstar_box.place(relx = 0.01, rely = 0.2)

    Astar_box = Checkbutton(root, text="Astar algorithm",
                                     variable=Astar_variable,
                                     onvalue = True,
                                     offvalue = False)
    Astar_box.config(font=(FONT, 14))
    Astar_box.place(relx = 0.01,  rely = 0.3)

    # create new Button and its atributes
    submit = Button(root, text = "Submit",
                    command = get_algorithms)
    submit.config(height = 5, width = 20, background = "red")
    submit.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    # active tkinter main loop
    root.mainloop()


if __name__ == "__main__":

    # variable algorithms contains all algorithms that user wants to compare
    algorithms = ""

    # call of user window
    # user_menu()

    # LOCAL PRINT. SHOULD BE DELETED
    print(algorithms)

    # hardcoded starting states
    # state = [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]]
    # state = [[7, 1, 2], [0, 8, 3], [6, 4, 5]]
    state = [[1, 2, 3], [0, 4, 5], [6, 8, 7]]  # Impossible to solve

    # TODO: numer 2 is hardcoded because there are exactly 2 puzzles
    scene_width = HORIZONTAL_OFFSET + 2 * len(state) * FIELD_SIZE + PUZZLE_DIST
    scene_height = VERTICAL_OFFSET + len(state) * FIELD_SIZE + FONT_SIZE

    puzzle_solvability = is_solvable(state)

    screen = init_scene(scene_width, scene_height)

    # necessary arguments for each process
    multiprocessing_data = [
        (WAstar(len(state), 4, mode="dynamic"),
         state,
         LEFT_OFFSET, TOP_OFFSET),
        (WAstar(len(state), 4, mode="static"),
         state,
         LEFT_OFFSET + len(state) * FIELD_SIZE + PUZZLE_DIST, TOP_OFFSET)
    ]

    # running daemon processes for each algorithm
    results_queue = multiprocessing.Queue()
    for solver, state, offset_x, offset_y in multiprocessing_data:
        args = (state, puzzle_solvability, offset_x, offset_y)
        cur_process = ProcessSolver(solver, results_queue, args=args)
        cur_process.start()

    loop_active = True
    while loop_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_active = False

        cur_qsize = results_queue.qsize()
        while cur_qsize > 0:
            cur_qsize -= 1
            cur_puzzle = results_queue.get()
            flag = solve_puzzle(cur_puzzle, puzzle_solvability)  # TODO
            if flag:
                results_queue.put(cur_puzzle)

        # redisplay and wait for next iteration
        pygame.display.update()
