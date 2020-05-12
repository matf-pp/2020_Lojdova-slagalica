# standard modules
import multiprocessing
import pygame
import os

from tkinter import *
from argparse import Namespace
from functools import partial

from src.Astar import Astar
from src.IDAstar import IDAstar
from src.WAstar import WAstar
from src.Puzzle import Puzzle
from utils.utils import serialize, generate_state

# font related
FONT_COLOR = (31, 33, 43)
FONT_SIZE = 24
FONT = "Courier"

# user menu related
PADDING_X = 40
PADDING_Y = 5

# scene related
N_PUZZLES = 2
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


class Direction:

    r"""Enum class for all possible directions of field movement."""

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4


class Solvers:

    r"""Enum class for all available solvers."""

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


class ProcessSolver(multiprocessing.Process):
    r"""Processes are used for solving puzzles.
    
    Each is runned as daemon
    process and saves data on shared queue."""

    def __init__(self, solver, queue, args=None):
        r"""Base constructor.

        Arguments:
            solver (BaseSolver): Puzzle solver.
            queue (Queue): ...
            args (dict): ... """

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


class UserMenu():

    r"""Wrapper class for tkinter user menu."""
    def _parse_solvers(self):
        r"""Based on selected items fetch `solvers` and `puzzle_size`."""

        self._is_destroyed = False
        self._puzzle_data = dict()

        solvers = []
        if self._tk_var_wastar_dynamic.get():
            solvers.append(Solvers.WASTAR_D)
        if self._tk_var_wastar_static.get():
            solvers.append(Solvers.WASTAR_S)
        if self._tk_var_idastar.get():
            solvers.append(Solvers.IDASTAR)
        if self._tk_var_astar.get():
            solvers.append(Solvers.ASTAR)
        self._puzzle_data["solvers"] = solvers

        # fetching solvers
        if len(solvers) != 2:
            solvers_popup = Tk()
            solvers_popup.wm_title("!")

            tk_lbl_solvers = Label(solvers_popup,
                                   text="Select 2 algorithms",
                                   padx=PADDING_X,
                                   pady=PADDING_Y)
            tk_lbl_solvers.pack(side="top", anchor="center")
            tk_btn_solvers = Button(solvers_popup,
                                    text="OK",
                                    command=solvers_popup.destroy,
                                    padx=PADDING_X)
            tk_btn_solvers.pack()

            solvers_popup.mainloop()

        # fetching puzzle size
        if self._tk_var_puzzle_size.get() == 3:
            self._puzzle_data["size"] = 3
        elif self._tk_var_puzzle_size.get() == 4:
            self._puzzle_data["size"] = 4
        else:
            puzzle_size_popup = Tk()
            puzzle_size_popup.wm_title("!")

            tk_lbl_puzzle_size = Label(puzzle_size_popup,
                                       text="Select puzzle size",
                                       padx=PADDING_X,
                                       pady=PADDING_Y)
            tk_lbl_puzzle_size.pack(side="top", anchor="center")
            tk_btn_puzzle_size = Button(puzzle_size_popup,
                                        text="OK",
                                        command=puzzle_size_popup.destroy,
                                        padx=PADDING_X)
            tk_btn_puzzle_size.pack()

            puzzle_size_popup.mainloop()

        # if everything is selected, we close user window
        if len(solvers) == 2 and self._puzzle_data.get("size") is not None:
            if not self._is_destroyed:
                self._is_destroyed = True
                self._root.destroy()

    def _setup_cb(self):
        r"""Setup all checkboxes in the user menu."""
        cb_shared_params = {
            "onvalue": True,
            "offvalue": False,
            "padx": PADDING_X,
            "pady": PADDING_Y
        }
        self._tk_cb_wastar_dynamic = Checkbutton(
            self._tk_frame_cb,
            text="Dynamic weighted A*",
            variable=self._tk_var_wastar_dynamic,
            **cb_shared_params)
        self._tk_cb_wastar_dynamic.pack(side=TOP, anchor=W)
        self._tk_cb_wastar_static = Checkbutton(
            self._tk_frame_cb,
            text="Static weighted A*",
            variable=self._tk_var_wastar_static,
            **cb_shared_params)
        self._tk_cb_wastar_static.pack(side=TOP, anchor=W)
        self._tk_cb_idastar = Checkbutton(
            self._tk_frame_cb,
            text="Iterative deepening A*",
            variable=self._tk_var_idastar,
            **cb_shared_params)
        self._tk_cb_idastar.pack(side=TOP, anchor=W)
        self._tk_cb_astar = Checkbutton(
            self._tk_frame_cb,
            text="Standard A*",
            variable=self._tk_var_astar,
            **cb_shared_params)
        self._tk_cb_astar.pack(side=TOP, anchor=W)

    def _setup_rb(self):
        r"""Setup all radio buttons in the user menu."""
        rb_shared_params = {
            "padx": PADDING_X,
            "pady": PADDING_Y
        }
        self._tk_rb_3x3 = Radiobutton(self._tk_frame_rb,
                                      text="3x3",
                                      variable=self._tk_var_puzzle_size,
                                      value=3,
                                      **rb_shared_params)
        self._tk_rb_3x3.pack(side=TOP, anchor=W)
        self._tk_rb_4x4 = Radiobutton(self._tk_frame_rb,
                                      text="4x4",
                                      variable=self._tk_var_puzzle_size,
                                      value=4,
                                      **rb_shared_params)
        self._tk_rb_4x4.pack(side=TOP, anchor=W)

    def _setup_submit(self):
        self._tk_btn_submit = Button(self._tk_frame_btn,
                                     text="Submit",
                                     command=self._parse_solvers)
        self._tk_btn_submit.pack(side=TOP, anchor=CENTER)

    def __init__(self):
        r"""Tkinter constructor."""
        self._root = Tk()
        self._root.wm_title("Loyd Puzzle A* Solvers")

        path = os.path.join(IMAGES_PATH, "icon.png")
        self._root.iconphoto(True, PhotoImage(file=path))
        self._root.resizable(False, False)
        self._root.config(background="white")

        self._tk_frame_btn = Frame(self._root)

        # three separate containers for content of the menu
        self._tk_frame_btn.pack(side="bottom", fill="both", expand=False)
        self._tk_frame_cb = Frame(self._root)
        self._tk_frame_cb.pack(side="left", fill="both", expand=False)
        self._tk_frame_rb = Frame(self._root)
        self._tk_frame_rb.pack(side="right", fill="both", expand=False)

        # special tkinter variables that contains informations from checkboxes
        self._tk_var_wastar_dynamic = BooleanVar()
        self._tk_var_wastar_static = BooleanVar()
        self._tk_var_idastar = BooleanVar()
        self._tk_var_astar = BooleanVar()
        self._tk_var_puzzle_size = IntVar()

    def show(self):
        self._setup_rb()
        self._setup_cb()
        self._setup_submit()

        self._root.mainloop()
        self._puzzle_data = Namespace(**self._puzzle_data)

    def get_puzzle_data(self):
        return self._puzzle_data


class PuzzleManipulation:

    r"""Abstract class for puzzle manipulation. Should not be initialized."""

    @staticmethod
    def get_zero_and_exchange_field(exchange_index, zero_index, value,
                                    current_state):
        r"""Finding indices of exchange and empty (zero) fields.
        
        Function defines which index corresponds to exchange and which
        corresponds to empty (zero) field.

        If the value of first field is zero, then zero field stands in position
        of the first index in current state and exchange field belongs to other
        index.

        In other case exchange field is at the first and zero field at the
        second index position."""

        if value != 0:
            exchange_index, zero_index = zero_index, exchange_index

        return current_state[zero_index], current_state[exchange_index]

    @staticmethod
    def define_move_direction(puzzle_size, index_src, value_src,
                              index_dest, value_dest):
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


class MainScene():

    r"""Wrapper class for Pygame main scene."""

    def __init__(self, state, puzzle_data, num_puzzles=2):
        r"""MainScene constructor"""
        self._N = len(state)
        self._scene_width = HORIZONTAL_OFFSET + \
            num_puzzles * self._N * FIELD_SIZE + PUZZLE_DIST
        self._scene_height = VERTICAL_OFFSET + \
            self._N * FIELD_SIZE + FONT_SIZE

        self._solvers = puzzle_data.solvers
        pygame.init()

    def _move_field(self, current_state, zero_field, exchange_field, target,
                    move_direction, puzzle_x, puzzle_y):
        r"""Function determines direction in which empty field is seted to be moved.

        Then, function swaps fields by increasing/decresaing coordinates
        of either empty and exchange field. If the move direction is up or down
        only `y` coordinate should be changed (in other case only `x`
        coordinate should be changed for both fields). It is enough to check
        only one field coordinate (in our case we check empty field
        coordinate).

        If zero field should move up, its `y` coordinate should decrease, and
        the sign variable is set to be negative number. With same logic we
        define sign variable for other directions.

        When we define target coordinate, its value and direction of move,
        main loop of this function changes both coordinates of empty and
        exchange field by increasing/decreasing them for the value of sign
        variable."""

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
                        path = os.path.join(IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT)
                        img = pygame.image.load(path)

                        pygame.draw.rect(self._screen,
                                         BACKGROUND_COLOR,
                                         (field_x, field_y,
                                          FIELD_SIZE, FIELD_SIZE))

                        self._screen.blit(img, (exchange_field._x,
                                                exchange_field._y))
                    else:
                        path = os.path.join(IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT)
                        img = pygame.image.load(path)
                        self._screen.blit(img, (field_x, field_y))
        else:
            while zero_field_variable < target:
                pygame.display.update()
                for field in current_state:
                    value = field._value
                    field_x, field_y = field._x, field._y

                    pygame.draw.rect(self._screen,
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
                        path = os.path.join(IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT)
                        img = pygame.image.load(path)
                        self._screen.blit(img, (exchange_field._x,
                                                exchange_field._y))
                    else:
                        path = os.path.join(IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT)
                        img = pygame.image.load(path)
                        self._screen.blit(img, (field_x, field_y))

    def _setup_text(self):
        font = pygame.font.Font("./src/fonts/calibri.ttf", FONT_SIZE)
        shared_params = [True, FONT_COLOR, BACKGROUND_COLOR]

        solver_left = Solvers.get_solver_name(self._solvers[0])
        text_left = font.render(solver_left, *shared_params)
        textrect_left = text_left.get_rect()

        left_x = LEFT_OFFSET + self._N * FIELD_SIZE // 2
        left_y = TOP_OFFSET + self._N * FIELD_SIZE + FONT_SIZE // 2
        textrect_left.center = (left_x, left_y)
        self._screen.blit(text_left, textrect_left)

        solver_right = Solvers.get_solver_name(self._solvers[1])
        text_right = font.render(solver_right, *shared_params)
        textrect_right = text_right.get_rect()

        right_x = self._scene_width - RIGHT_OFFSET - self._N * FIELD_SIZE // 2
        right_y = TOP_OFFSET + self._N * FIELD_SIZE + FONT_SIZE // 2
        textrect_right.center = (right_x, right_y)
        self._screen.blit(text_right, textrect_right)

    def _draw_puzzle(self, current_state, puzzle_solvability):
        r"""Function iterates through current state of the puzzle.

        Draws all fields as a images.

        In the place of empty(zero) field nothing should be draw so we
        skip the field with value 0."""

        for field in current_state:
            value = field._value
            field_x, field_y = field._x, field._y

            if value == 0:
                continue

            path = os.path.join(IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT)
            img = pygame.image.load(path)
            self._screen.blit(img, (field_x, field_y))

        # when puzzle doesn't have solution
        if not puzzle_solvability:
            img = pygame.image.load(os.path.join(IMAGES_PATH, "stop.png"))
            img_width, img_height = img.get_size()
            self._screen.blit(img, (self._scene_width // 2 - img_width // 2,
                                    self._scene_height // 2 - img_height // 2))

    def solve_puzzle(self, puzzle, puzzle_solvability):
        r"""Function gets current state of puzzle, draws puzzle, gets
        difference between current and the next state of the puzzle, and makes
        transition from current to the next state."""

        current_state = puzzle._fields
        puzzle_x, puzzle_y = puzzle.get_puzzle_coordinates()

        # draw state without animation
        self._draw_puzzle(current_state, puzzle_solvability)

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
        move_direction = PuzzleManipulation.define_move_direction(
            puzzle.get_puzzle_size(),
            index_cur,
            value_cur,
            index_next,
            value_next)

        # get fields for animation
        exchange_field, zero_field = \
            PuzzleManipulation.get_zero_and_exchange_field(index_cur,
                                                           index_next,
                                                           value_cur,
                                                           current_state)

        # define stop targets for animation
        target_x, target_y = exchange_field._x, exchange_field._y

        # move zero field to seted direction
        if move_direction == Direction.UP:
            self._move_field(current_state, zero_field, exchange_field,
                             target_y, Direction.UP, puzzle_x, puzzle_y)
        elif move_direction == Direction.DOWN:
            self._move_field(current_state, zero_field, exchange_field,
                             target_y, Direction.DOWN, puzzle_x, puzzle_y)
        elif move_direction == Direction.RIGHT:
            self._move_field(current_state, zero_field, exchange_field,
                             target_x, Direction.RIGHT, puzzle_x, puzzle_y)
        elif move_direction == Direction.LEFT:
            self._move_field(current_state, zero_field, exchange_field,
                             target_x, Direction.LEFT, puzzle_x, puzzle_y)
        else:
            raise ValueError("Invalid move_direction")  # should never happen

        puzzle.states_change()

        return True  # valid move has happened

    def _setup_scene(self):
        pygame.display.set_caption("Loyd Puzzle A* Solvers")
        icon = pygame.image.load(os.path.join(IMAGES_PATH, "icon.png"))
        pygame.display.set_icon(icon)
        self._screen.fill(BACKGROUND_COLOR)

    def show(self):
        r"""Initializing scene and returning Pygame's `Surface` object. Scene
        contains:
            (1) text boxes -- done here
            (2) proper background color -- done here
            (3) puzzles -- done separately

        Arguments:
            scene_width, scene_height (ints): Dimension of scene window in
            pixels.

        Returns:
            screen (Surface): Object for scene manipulation."""

        pygame.init()
        self._screen = pygame.display.set_mode((self._scene_width,
                                                self._scene_height))
        self._setup_scene()
        self._setup_text()


if __name__ == "__main__":
    # showing user menu
    user_menu = UserMenu()
    user_menu.show()
    puzzle_data = user_menu.get_puzzle_data()

    # generating puzzle's initial state
    state, puzzle_solvability = generate_state(puzzle_data.size)

    # showing main scene
    main_scene = MainScene(state, puzzle_data)
    main_scene.show()

    # necessary arguments for each processing
    multiprocessing_data = [
        (Solvers.get_solver_instance(puzzle_data.solvers[0])(puzzle_data.size),
         state,
         LEFT_OFFSET, TOP_OFFSET),
        (Solvers.get_solver_instance(puzzle_data.solvers[1])(puzzle_data.size),
         state,
         LEFT_OFFSET + puzzle_data.size * FIELD_SIZE + PUZZLE_DIST, TOP_OFFSET)
    ]

    # running daemon processes for each algorithm
    results_queue = multiprocessing.Queue()
    for solver, state, offset_x, offset_y in multiprocessing_data:
        args = (state, puzzle_solvability, offset_x, offset_y)
        cur_process = ProcessSolver(solver, results_queue, args=args)
        cur_process.start()

    # Pygame main loop
    loop_active = True
    while loop_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_active = False

        cur_qsize = results_queue.qsize()
        while cur_qsize > 0:
            cur_qsize -= 1
            cur_puzzle = results_queue.get()
            flag = main_scene.solve_puzzle(cur_puzzle, puzzle_solvability)

            if flag:
                results_queue.put(cur_puzzle)

        # redisplay and wait for next iteration
        pygame.display.update()
