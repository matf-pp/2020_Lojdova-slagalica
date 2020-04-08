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


PUZZLE_IMAGES_PATH = os.path.join(".", "src", "Numbers")
PUZZLE_IMAGES_EXT = ".png"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 640
BACKGROUND_COLOR = (255, 255, 255)
SLEEP_DURATION = 0.0001
PUZZLE_X, PUZZLE_Y = 30, 0
PUZZLE_SIZE = 400
PUZZLE_DIMENSION = 4


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
        sign = -1
    elif move_direction == Direction.DOWN:
        zero_field_variable = zero_field._y
        sign = 1
    elif move_direction == Direction.LEFT:
        zero_field_variable = zero_field._x
        sign = -1
    else:
        zero_field_variable = zero_field._x
        sign = 1

    if move_direction in [Direction.UP, Direction.LEFT]:
        while zero_field_variable > target:
            pygame.display.update()
            time.sleep(SLEEP_DURATION)
            for field in current_state:
                value = field._value
                field_x, field_y = field._x, field._y

                if value == 0:
                    zero_field_variable += sign * 2
                elif value == exchange_field._value:
                    if move_direction in [Direction.UP, Direction.DOWN]:
                        exchange_field._y += (-sign) * 2
                    else:
                        exchange_field._x += (-sign) * 2
                    screen.fill(BACKGROUND_COLOR)
                    draw_puzzle_without_animation_fields(current_state,
                                                         exchange_field)
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
    else:
        while zero_field_variable < target:
            pygame.display.update()
            time.sleep(SLEEP_DURATION)
            for field in current_state:
                value = field._value
                field_x, field_y = field._x, field._y

                if value == 0:
                    zero_field_variable += sign * 2
                elif value == exchange_field._value:
                    if move_direction in [Direction.UP, Direction.DOWN]:
                        exchange_field._y += (-sign) * 2
                    else:
                        exchange_field._x += (-sign) * 2
                    screen.fill(BACKGROUND_COLOR)
                    draw_puzzle_without_animation_fields(current_state,
                                                         exchange_field)
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

    puzzle = Puzzle(states_list,
                    PUZZLE_X, PUZZLE_Y,
                    "plava",
                    PUZZLE_SIZE, PUZZLE_DIMENSION)

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
        return

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


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    starting_states = [
        # [[7, 1, 2], [0, 8, 3], [6, 4, 5]],
        [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]],
    ]

    puzzleWastar = init_puzzle(ValidAlgorithms.WASTAR_S)

    loop_active = True
    while loop_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_active = False

        solve_puzzle(puzzleWastar)

        # redisplay and wait for next iteration
        pygame.display.update()
        time.sleep(SLEEP_DURATION)
