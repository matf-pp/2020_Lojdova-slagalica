import multiprocessing
import pygame
import time
import sys
import os

import numpy as np

from argparse import Namespace
from functools import partial

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
SCENE_FONT_SIZE = 24
USER_MENU_FONT_SIZE = 14
FONT = "Courier"

# user menu related
PADDING_X = 40
PADDING_Y = 5

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
IMAGES_PATH = os.path.join(".", "src", "images")
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
            # if puzzle has solution we need to find one
            result = self._solver.solve(state)
            puzzle = Puzzle(result[1][1],
                            puzzle_x, puzzle_y,
                            len(state))
        else:
            # there is no solution - list of states has length 1
            puzzle = Puzzle([serialize(state)],
                            puzzle_x, puzzle_y,
                            len(state))

        self._queue.put(puzzle)


class Solvers:
    r"""Enum class for algorithms."""

    ASTAR, IDASTAR, WASTAR_S, WASTAR_D = 1, 2, 3, 4

    @staticmethod
    def get_solver_name(idx):
        if idx == Solvers.ASTAR:
            return "A*"
        elif idx == Solvers.IDASTAR:
            return "IDA*"
        elif idx == Solvers.WASTAR_D:
            return "Dynamic WA*"
        elif idx == Solvers.WASTAR_S:
            return "Static WA*"

    @staticmethod
    def get_solver_instance(idx):
        if idx == Solvers.ASTAR:
            return Astar
        elif idx == Solvers.IDASTAR:
            return IDAstar
        elif idx == Solvers.WASTAR_D:
            return partial(WAstar, weight=4, mode="dynamic")
        elif idx == Solvers.WASTAR_S:
            return partial(WAstar, weight=4, mode="static")


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
                    img = pygame.image.load(os.path.join(IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))

                    pygame.draw.rect(screen,
                                     BACKGROUND_COLOR,
                                     (field_x, field_y,
                                      FIELD_SIZE, FIELD_SIZE))

                    screen.blit(img, (exchange_field._x, exchange_field._y))
                else:
                    img = pygame.image.load(os.path.join(IMAGES_PATH,
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
                    img = pygame.image.load(os.path.join(IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (exchange_field._x, exchange_field._y))
                else:
                    img = pygame.image.load(os.path.join(IMAGES_PATH,
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

        img = pygame.image.load(os.path.join(IMAGES_PATH,
                                             str(value) + PUZZLE_IMAGES_EXT))
        screen.blit(img, (field_x, field_y))

    # when puzzle doesn't have solution
    if not puzzle_solvability:
        img = pygame.image.load(os.path.join(IMAGES_PATH, "stop.png"))
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
    # in new puzzle state we will have value_cur in field with index_cur
    # and value_next in field with index_next
    if puzzle.next_puzzle_state() is not None:
        index_cur, value_cur, index_next, value_next = \
            puzzle.states_difference(
                puzzle.current_puzzle_state(),
                puzzle.next_puzzle_state())
    else:
        return False  # no further moves

    # define direction of field movement
    move_direction = define_move_direction(puzzle.get_puzzle_size(),
                                           index_cur,
                                           index_next,
                                           value_cur,
                                           value_next)

    # get fields for animation
    exchange_field, zero_field = \
        get_zero_and_exchange_field(index_cur, index_next,
                                    value_cur, current_state)

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


def show_scene(scene_width, scene_height):
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

    icon = pygame.image.load(os.path.join(IMAGES_PATH, "icon.png"))
    pygame.display.set_icon(icon)
    screen.fill(BACKGROUND_COLOR)

    # font = pygame.font.Font("./src/fonts/calibri.ttf", SCENE_FONT_SIZE)  # test font 1
    # font = pygame.font.Font("./src/fonts/Pacifico.ttf", SCENE_FONT_SIZE)  # test font 2
    # font = pygame.font.Font("./src/fonts/Xcelsion Italic.ttf", SCENE_FONT_SIZE)  # test font 3
    # font = pygame.font.Font("./src/fonts/XpressiveBlack Regular.ttf", SCENE_FONT_SIZE)  # test font 4
    # font = pygame.font.Font("./src/fonts/Yes_Union.ttf", SCENE_FONT_SIZE)  # test font 5
    font = pygame.font.Font("./src/fonts/y.n.w.u.a.y.ttf", SCENE_FONT_SIZE)  # test font 6
    text_upper_left = font.render(Solvers.get_solver_name(puzzle_data.solvers[0]),
                                  True,
                                  FONT_COLOR,
                                  BACKGROUND_COLOR)
    textrect_upper_left = text_upper_left.get_rect()
    textrect_upper_left.center = (LEFT_OFFSET + len(state) * FIELD_SIZE // 2,
                                  TOP_OFFSET + (len(state)) * FIELD_SIZE + SCENE_FONT_SIZE // 2)
    screen.blit(text_upper_left, textrect_upper_left)

    text_upper_right = font.render(Solvers.get_solver_name(puzzle_data.solvers[1]),
                                   True,
                                   FONT_COLOR,
                                   BACKGROUND_COLOR)
    textrect_upper_right = text_upper_right.get_rect()
    textrect_upper_right.center = (scene_width - RIGHT_OFFSET - len(state) * FIELD_SIZE // 2,
                                   TOP_OFFSET + (len(state)) * FIELD_SIZE + SCENE_FONT_SIZE // 2)
    screen.blit(text_upper_right, textrect_upper_right)

    return screen


def show_user_menu():
    r"""function draws basic tkinter window that allows user to select
    which algorithms dose he wants to compare"""

    puzzle_data = dict()

    def parse_solvers():
        solvers = []
        if tk_var_wastar_dynamic.get():
            solvers.append(Solvers.WASTAR_D)
        if tk_var_wastar_static.get():
            solvers.append(Solvers.WASTAR_S)
        if tk_var_idastar.get():
            solvers.append(Solvers.IDASTAR)
        if tk_var_astar.get():
            solvers.append(Solvers.ASTAR)
        puzzle_data["solvers"] = solvers

        # get size of puzzle that user wants to use
        if tk_var_puzzle_size.get() == 3:
            puzzle_data["size"] = 3
        elif tk_var_puzzle_size.get() == 4:
            puzzle_data["size"] = 4
        else:
            popup = Tk()
            popup.wm_title("!")

            tk_lbl_condition = Label(popup,
                                     text="Select puzzle size",
                                     padx=PADDING_X,
                                     pady=PADDING_Y)
            tk_lbl_condition.pack(side="top", anchor="center")
            tk_btn_okay = Button(popup,
                                 text="OK",
                                 command=popup.destroy,
                                 padx=PADDING_X)
            tk_btn_okay.pack()

            popup.mainloop()

        if len(solvers) != 2:
            popup = Tk()
            popup.wm_title("!")

            tk_lbl_condition = Label(popup,
                                     text="Select 2 algorithms",
                                     padx=PADDING_X,
                                     pady=PADDING_Y)
            tk_lbl_condition.pack(side="top", anchor="center")
            tk_btn_okay = Button(popup,
                                 text="OK",
                                 command=popup.destroy,
                                 padx=PADDING_X)
            tk_btn_okay.pack()

            popup.mainloop()
        else:
            root.destroy()

    # tkinter window init
    root = Tk()
    root.wm_title("Loyd Puzzle A* Solvers")
    root.iconphoto(True,
                   PhotoImage(file=os.path.join(IMAGES_PATH, "icon.png")))
    root.resizable(False, False)
    root.config(background="white")

    tk_frame_btn = Frame(root)

    # three separate containers for content of the menu
    tk_frame_btn.pack(side="bottom", fill="both", expand=False)
    tk_frame_cb = Frame(root)
    tk_frame_cb.pack(side="left", fill="both", expand=False)
    tk_frame_rb = Frame(root)
    tk_frame_rb.pack(side="right", fill="both", expand=False)

    # special tkinter variables that contains informations from checkboxes
    tk_var_wastar_dynamic = BooleanVar()
    tk_var_wastar_static = BooleanVar()
    tk_var_idastar = BooleanVar()
    tk_var_astar = BooleanVar()
    tk_var_puzzle_size = IntVar()

    # creating checkboxes
    tk_cb_wastar_dynamic = Checkbutton(tk_frame_cb,
                                       text="Dynamic weighted A*",
                                       variable=tk_var_wastar_dynamic,
                                       onvalue=True,
                                       offvalue=False,
                                       padx=PADDING_X,
                                       pady=PADDING_Y)
    tk_cb_wastar_dynamic.pack(side=TOP, anchor=W)

    tk_cb_wastar_static = Checkbutton(tk_frame_cb,
                                      text="Static weighted A*",
                                      variable=tk_var_wastar_static,
                                      onvalue=True,
                                      offvalue=False,
                                      padx=PADDING_X,
                                      pady=PADDING_Y)
    tk_cb_wastar_static.pack(side=TOP, anchor=W)

    tk_cb_idastar = Checkbutton(tk_frame_cb,
                                text="Iterative deepening A*",
                                variable=tk_var_idastar,
                                onvalue=True,
                                offvalue=False,
                                padx=PADDING_X,
                                pady=PADDING_Y)
    tk_cb_idastar.pack(side=TOP, anchor=W)

    tk_cb_astar = Checkbutton(tk_frame_cb,
                              text="Standard A*",
                              variable=tk_var_astar,
                              onvalue=True,
                              offvalue=False,
                              padx=PADDING_X,
                              pady=PADDING_Y)
    tk_cb_astar.pack(side=TOP, anchor=W)

    # creating radiobuttons
    tk_rb_3x3 = Radiobutton(tk_frame_rb,
                            text="3x3",
                            variable=tk_var_puzzle_size,
                            value=3,
                            padx=PADDING_X,
                            pady=PADDING_Y)
    tk_rb_3x3.pack(side=TOP, anchor=W)

    tk_rb_4x4 = Radiobutton(tk_frame_rb,
                            text="4x4",
                            variable=tk_var_puzzle_size,
                            value=4,
                            padx=PADDING_X,
                            pady=PADDING_Y)
    tk_rb_4x4.pack(side=TOP, anchor=W)

    # creating submit button
    tk_btn_submit = Button(tk_frame_btn,
                           text="Submit",
                           command=parse_solvers)
    tk_btn_submit.pack(side=TOP, anchor=CENTER)

    # active tkinter main loop
    root.mainloop()

    return Namespace(**puzzle_data)


def generate_state(N):
    state = np.arange(N * N)

    timestamp = int(time.time())
    np.random.seed(timestamp)
    np.random.shuffle(state)
    state = state.reshape((N, N))

    return state.tolist()


if __name__ == "__main__":
    # variable algorithms contains all algorithms that user wants to compare
    algorithms = []
    puzzle_size = 0

    # call of user window
    puzzle_data = show_user_menu()

    # generating puzzle's initial state
    state = generate_state(puzzle_data.size)

    # TODO: numer 2 is hardcoded because there are exactly 2 puzzles
    scene_width = HORIZONTAL_OFFSET + 2 * len(state) * FIELD_SIZE + PUZZLE_DIST
    scene_height = VERTICAL_OFFSET + len(state) * FIELD_SIZE + SCENE_FONT_SIZE

    puzzle_solvability = is_solvable(state)

    screen = show_scene(scene_width, scene_height)

    multiprocessing_data = [
        (Solvers.get_solver_instance(puzzle_data.solvers[0])(len(state)),
         state,
         LEFT_OFFSET, TOP_OFFSET),
        (Solvers.get_solver_instance(puzzle_data.solvers[1])(len(state)),
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
