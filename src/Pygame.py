import multiprocessing
import pygame
import time
import sys
import os

from Astar import Astar
from IDAstar import IDAstar
from BaseSolver import BaseSolver
from WAstar import WAstar
from Field import Field
from Puzzle import Puzzle


FIELD_SIZE = 100

PUZZLE_IMAGES_PATH = os.path.join(".", "src", "Numbers")
PUZZLE_IMAGES_EXT = ".png"
BACKGROUND_COLOR = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
DISTANCE = 100        # Distance between two puzzles
TOP_OFFSET = 0
RIGHT_OFFSET = 50
LEFT_OFFSET = 100
BOTTOM_OFFSET = 250   # This is bigger beceuse we plan text under the puzzle
ANIMATION_FIELD_SPEED = 5  # not every value will properly work
ANIMATION_STATE_DURATION = 0.25
PUZZLE_X, PUZZLE_Y = 30, 0


class ProcessSolver(multiprocessing.Process):
    def __init__(self, solver, queue, process_idx, args=None):
        super().__init__(daemon=True, args=args)

        self._solver = solver
        self._queue = queue
        self._process_idx = process_idx

    def run(self):
        state, offset_x, offset_y = self._args

        if self._process_idx == 0:
            puzzle_x = RIGHT_OFFSET
        elif self._process_idx == 1:
            puzzle_x = RIGHT_OFFSET + len(state) * FIELD_SIZE + DISTANCE

        puzzle_y = TOP_OFFSET  # Both puzzles have the same y-coordinate
        result = self._solver.solve(state)
        puzzle = Puzzle(result[1][1],
                        puzzle_x, puzzle_y,
                        "plava",
                        len(state))
        self._queue.put(puzzle)


class Direction:
    r"""Enum class for all possible directions of field movement."""

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4


class ValidAlgorithms:
    r"""Enum class for all algorithms that can solve puzzle."""

    ASTAR, IDASTAR, WASTAR_D, WASTAR_S = 1, 2, 3, 4


def define_move_direction(index1, index2, value1, value2):
    if_cond = value1 == 0 and index1 < index2
    if_cond = if_cond or (value2 == 0 and index2 < index1)

    if abs(index1 - index2) == 4:
        return Direction.DOWN if if_cond else Direction.UP
    else:
        return Direction.RIGHT if if_cond else Direction.LEFT


def get_zero_and_exchange_field(index1, index2, value1, current_state):
    exchange, zero = None, None

    if value1 == 0:
        exchange = current_state[index2]
        zero = current_state[index1]
    else:
        exchange = current_state[index1]
        zero = current_state[index2]

    return exchange, zero


def move_field(current_state, zero_field, exchange_field, target,
               move_direction):
    width, height = PUZZLE_X, PUZZLE_Y
    fields_in_row = 1

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
                                     (width + field_x, height + field_y,
                                      FIELD_SIZE, FIELD_SIZE))

                    screen.blit(img, (width + exchange_field._x,
                                      height + exchange_field._y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width + field_x,
                                      height + field_y))

                fields_in_row = 1 if fields_in_row == 4 else fields_in_row + 1
    else:
        while zero_field_variable < target:
            pygame.display.update()
            for field in current_state:
                value = field._value
                field_x, field_y = field._x, field._y

                pygame.draw.rect(screen,
                                 BACKGROUND_COLOR,
                                 (width + field_x, height + field_y,
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
                    screen.blit(img, (width + exchange_field._x,
                                      height + exchange_field._y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                            str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width + field_x,
                                      height + field_y))

                fields_in_row = 1 if fields_in_row == 4 else fields_in_row + 1


def draw_puzzle(current_state):
    width, height = PUZZLE_X, PUZZLE_Y
    fields_in_row = 1

    for field in current_state:
        value = field._value
        field_x, field_y = field._x, field._y

        if value == 0:
            continue

        img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                             str(value) + PUZZLE_IMAGES_EXT))
        screen.blit(img, (width + field_x, height + field_y))

        fields_in_row = 1 if fields_in_row == 4 else fields_in_row + 1


def draw_puzzle_without_animation_fields(current_state, exchange_field):
    width, height = PUZZLE_X, PUZZLE_Y
    fields_in_row = 1

    for field in current_state:
        value = field._value
        field_x, field_y = field._x, field._y

        if value == 0:
            continue
        elif exchange_field._value == value:
            continue
        else:
            img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH,
                                    str(value) + PUZZLE_IMAGES_EXT))
            screen.blit(img, (width + field_x,
                              height + field_y))

        fields_in_row = 1 if fields_in_row == 4 else fields_in_row + 1


def init_puzzle(algorithm):
    if algorithm == ValidAlgorithms.WASTAR_D:
        for state in starting_states:
            solver = WAstar(len(state), 4, mode="dynamic")
            states_list = solver.solve(state)[1][1]
            # print(solver.solve(state))
    elif algorithm == ValidAlgorithms.WASTAR_S:
        for state in starting_states:
            solver = WAstar(len(state), 4, mode="static")
            states_list = solver.solve(state)[1][1]
            # print(solver.solve(state))
    elif algorithm == ValidAlgorithms.IDASTAR:
        for state in starting_states:
            solver = IDAstar(len(state))
            states_list = solver.solve(state)[1][1]
            # print(solver.solve(state))
    elif algorithm == ValidAlgorithms.ASTAR:
        for state in starting_states:
            solver = Astar(len(state))
            states_list = solver.solve(state)[1][1]
            # print(solver.solve(state))
    else:
        raise ValueError("Invalid algoritham")  # should never happen

    # puzzle = Puzzle(states_list,
    #               PUZZLE_X, PUZZLE_Y,
    #                "plava",
    #                len(state))

    return puzzle


def solve_puzzle(puzzle):
    current_state = puzzle._fields

    # draw state without animation
    draw_puzzle(current_state)

    # get difference between current and next state
    if puzzle.next_puzzle_state() is not None:
        index1, value1, index2, value2 = puzzle.states_difference(
            puzzle.current_puzzle_state(),
            puzzle.next_puzzle_state())
    else:
        return False  # no further moves

    # define direction of field movement
    move_direction = define_move_direction(index1, index2, value1, value2)

    # get fields for animation
    exchange_field, zero_field = \
        get_zero_and_exchange_field(index1, index2, value1, current_state)

    # define stop targets for animation
    target_x, target_y = exchange_field._x, exchange_field._y

    # move zero field to seted direction
    if move_direction == Direction.UP:
        move_field(current_state, zero_field, exchange_field,
                   target_y, Direction.UP)
    elif move_direction == Direction.DOWN:
        move_field(current_state, zero_field, exchange_field,
                   target_y, Direction.DOWN)
    elif move_direction == Direction.RIGHT:
        move_field(current_state, zero_field, exchange_field,
                   target_x, Direction.RIGHT)
    elif move_direction == Direction.LEFT:
        move_field(current_state, zero_field, exchange_field,
                   target_x, Direction.LEFT)
    else:
        raise ValueError("Invalid move_direction")  # should never happen

    puzzle.states_change()
    current_state = puzzle._fields

    return True  # valid move has happened


if __name__ == "__main__":
    state = [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]]
    # state = [[7, 1, 2], [0, 8, 3], [6, 4, 5]]
    # starting_states = [
    #     # [[7, 1, 2], [0, 8, 3], [6, 4, 5]],
    #     [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]],
    # ]

    # We hardcode this dimensions because we have a deal
    # that window looks like this
    if len(state) == 4:
        window_width = RIGHT_OFFSET + 8 * FIELD_SIZE + DISTANCE + LEFT_OFFSET
        window_height = TOP_OFFSET + 4 * FIELD_SIZE + BOTTOM_OFFSET
    elif len(state) == 3:
        window_width = RIGHT_OFFSET + 6 * FIELD_SIZE + DISTANCE + LEFT_OFFSET
        window_height = TOP_OFFSET + 3 * FIELD_SIZE + BOTTOM_OFFSET
    elif len(state) == 2:
        window_width = RIGHT_OFFSET + 4 * FIELD_SIZE + DISTANCE + LEFT_OFFSET
        window_height = TOP_OFFSET + 2 * FIELD_SIZE + BOTTOM_OFFSET

    # results_queue = Queue()
    results_queue = multiprocessing.Queue()
    processes_data = [
        (WAstar(len(state), 4, mode="dynamic"), state, 0, 0),
        (WAstar(len(state), 4, mode="static"), state, 400, 0)
        # (Astar(len(state)), state, 400, 0)
    ]

    for i, (solver, state, offset_x, offset_y) in enumerate(processes_data):
        args = (state, offset_x, offset_y)
        cur_process = ProcessSolver(solver, results_queue, i, args=args)
        cur_process.start()

    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Loyd Puzzle')

    icon = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, "puzzle.png"))
    pygame.display.set_icon(icon)

    screen.fill(BACKGROUND_COLOR)

    # Text
    font = pygame.font.Font('freesansbold.ttf', 32)
    text1 = font.render('First', True, green, blue)
    text2 = font.render('Second', True, green, blue)

    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect1.center = (RIGHT_OFFSET * 5, 50)
    textRect2.center = (RIGHT_OFFSET * 5 + DISTANCE * 5, 50)

    loop_active = True
    while loop_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_active = False

        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)

        cur_qsize = results_queue.qsize()
        while cur_qsize > 0:
            cur_qsize -= 1
            cur_puzzle = results_queue.get()
            flag = solve_puzzle(cur_puzzle)
            if flag:
                results_queue.put(cur_puzzle)

        # redisplay and wait for next iteration
        pygame.display.update()
