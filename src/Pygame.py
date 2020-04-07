import pygame
import time
import os

from src.Astar import *
from src.IDAstar import *
from src.BaseSolver import *
from src.WAstar import *
from src.klase_final import *


PUZZLE_IMAGES_PATH = "./src/Numbers"
PUZZLE_IMAGES_EXT = ".png"

#screen.blit("ime slike", x, y)

#define color values
white = (255, 255, 255)
black = (0, 0, 0)
red = (204, 0, 0)
green = (128, 255, 0)
blue = (0, 204, 204)
yellow = (255, 255, 0)
gray = (100, 100, 100)

colors = (black, red, green, blue, yellow)

#define direction values
up = 1
down = 2
left = 3
right = 4

pygame.init()
screen = pygame.display.set_mode((800, 640))

def define_move_direction(index1, index2, value1, value2):

    if abs(index1-index2) == 4:
        if (value1 == 0 and index1 < index2) or (value2 == 0 and index2 < index1):
            return down
        else:
            return up
    else:
        if (value1 == 0 and index1 < index2) or (value2 == 0 and index2 < index1):
            return right
        else:
            return left


def get_zero_and_exchange_field(index1, index2, value1):
    exchange = None
    zero = None
    if value1 == 0:
        exchange = current_state[index2]
        zero = current_state[index1]
    else:
        exchange = current_state[index1]
        zero = current_state[index2]

    return (exchange, zero)

def move_up(current_state, zero_field, exchange_field, target_y):

    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1

    while zero_field.y > target_y:
            pygame.display.update()
            time.sleep(0.01)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    zero_field.y -= 2
                elif value == exchange_field.vrednost:
                    exchange_field.y += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state, exchange_field)
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width+exchange_field.x, height+exchange_field.y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width+field_x, height+field_y))

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1


def move_down(current_state, zero_field, exchange_field, target_y):

    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1

    while zero_field.y < target_y:
            pygame.display.update()
            time.sleep(0.01)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    zero_field.y += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state,exchange_field)
                elif value == exchange_field.vrednost:
                    exchange_field.y -= 2
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_PATH))
                    screen.blit(img, (width+exchange_field.x, height+exchange_field.y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width+field_x, height+field_y))

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1

def move_right(current_state, zero_field, exchange_field, target_x):

    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1

    while zero_field.x < target_x:
            pygame.display.update()
            time.sleep(0.01)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    zero_field.x += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state,exchange_field)
                elif value == exchange_field.vrednost:
                    exchange_field.x -= 2
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width+exchange_field.x, height+exchange_field.y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width+field_x, height+field_y))

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1

def move_left(current_state, zero_field, exchange_field, target_x):

    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1

    while zero_field.x > target_x:
            pygame.display.update()
            time.sleep(0.01)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    zero_field.x -= 2
                elif value == exchange_field.vrednost:
                    exchange_field.x += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state,exchange_field)
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width+field_x, height+field_y))
                else:
                    img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
                    screen.blit(img, (width+field_x, height+field_y))

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1




def draw_puzzle(current_state):

    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1

    for field in current_state:
        value = field.vrednost
        field_x = field.x
        field_y = field.y

        if value == 0:
            continue

        img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
        screen.blit(img, (width+field_x, height+field_y))


        if fields_in_row == 4:
            fields_in_row = 1
        else:
            fields_in_row = fields_in_row + 1

def draw_puzzle_without_animation_fields(current_state, exchange_field):

    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1

    for field in current_state:
        value = field.vrednost
        field_x = field.x
        field_y = field.y

        if value == 0:
            continue
        elif exchange_field.vrednost == value:
            continue
        else:
            img = pygame.image.load(os.path.join(PUZZLE_IMAGES_PATH, str(value) + PUZZLE_IMAGES_EXT))
            screen.blit(img, (width+field_x, height+field_y))

        if fields_in_row == 4:
            fields_in_row = 1
        else:
            fields_in_row = fields_in_row + 1



starting_states = [
    # [[7, 1, 2], [0, 8, 3], [6, 4, 5]],
    [[8, 5, 9, 11], [7, 12, 10, 4], [0, 15, 13, 14], [1, 2, 6, 3]],
]

states_list = []
for state in starting_states:
    solver = WAstar(len(state), 4, mode="dynamic")
    states_list = solver.solve(state)[1][1]
    print(solver.solve(state))

puzzle_x = 30
puzzle_y = 0
puzzle_dimension = 400
puzzle = Slagalica(states_list, puzzle_x, puzzle_y, "plava", puzzle_dimension)


loop_active = True
current_state = puzzle.polja_slagalice
while loop_active:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop_active = False

    #draw state without animation
    draw_puzzle(current_state)

    #get difference between current and next state
    (index1, value1, index2, value2) = puzzle.razlike_stanja(puzzle.trenutno_stanje(), puzzle.sledece_stanje())

    #define direction of field movement
    move_direction = define_move_direction(index1, index2, value1, value2)

    #get fields for animation
    (exchange_field, zero_field) = get_zero_and_exchange_field(index1, index2, value1)

    #define stop targets for animation
    target_x = exchange_field.x
    target_y = exchange_field.y

    #move zero field to seted direction
    if move_direction == up:
        move_up(current_state, zero_field, exchange_field, target_y)

    if move_direction == down:
        move_down(current_state, zero_field, exchange_field, target_y)

    if move_direction == right:
        move_right(current_state, zero_field, exchange_field, target_x)

    if move_direction == left:
        move_left(current_state, zero_field, exchange_field, target_x)

    #redisplay, wait and iterate through list of statets
    pygame.display.update()
    time.sleep(0.3)
    puzzle.promena_stanja()
    current_state = puzzle.polja_slagalice
