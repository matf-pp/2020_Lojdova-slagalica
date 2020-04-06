import pygame
import time
from src.Astar import *
from src.IDAstar import *
from src.BaseSolver import *
from src.WAstar import *
from src.klase_final import *



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

def draw_puzzle(current_state):

    border = 5
    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1

    for field in current_state:
        value = field.vrednost
        field_x = field.x
        field_y = field.y

        if value == 0:
            color = white
        else:
            color = colors[value % 4]
        pygame.draw.rect(screen, color, [width+field_x, height+field_y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])

        if fields_in_row == 4:
            fields_in_row = 1
        else:
            fields_in_row = fields_in_row + 1

def draw_puzzle_without_animation_fields(current_state, exchange_field):

    border = 5
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
            color = colors[value % 4]
            pygame.draw.rect(screen, color, [width+field_x, height+field_y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])

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

    draw_puzzle(current_state)

    (index1, value1, index2, value2) = puzzle.razlike_stanja(puzzle.trenutno_stanje(), puzzle.sledece_stanje())

    move_direction = up
    exchange_field = current_state[0]
    zero_field = current_state[0]
    if abs(index1-index2) == 4:
        if (value1 == 0 and index1 < index2) or (value2 == 0 and index2 < index1):
            move_direction = down
        else:
            move_direction = up
    else:
        if (value1 == 0 and index1 < index2) or (value2 == 0 and index2 < index1):
            move_direction = right
        else:
            move_direction = left

    if value1 == 0:
        exchange_field = current_state[index2]
        zero_field = current_state[index1]
    else:
        exchange_field = current_state[index1]
        zero_field = current_state[index2]

    target_x = exchange_field.x
    target_y = exchange_field.y
    border = 5
    width = puzzle_x
    height = puzzle_y
    fields_in_row = 1



    if move_direction == up:
        while zero_field.y > target_y:
            pygame.display.update()
            time.sleep(0.023)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    color = gray
                    zero_field.y -= 2
                    pygame.draw.rect(screen, color, [width+zero_field.x, height+zero_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                elif value == exchange_field.vrednost:
                    color = colors[exchange_field.vrednost % 4]
                    exchange_field.y += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state,exchange_field)
                    pygame.draw.rect(screen, color, [width+exchange_field.x, height+exchange_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                else:
                    color = colors[value % 4]
                    pygame.draw.rect(screen, color, [width+field_x, height+field_y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1


    if move_direction == down:
        while zero_field.y < target_y:
            pygame.display.update()
            time.sleep(0.023)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    color = gray
                    zero_field.y += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state,exchange_field)
                    pygame.draw.rect(screen, color, [width+zero_field.x, height+zero_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                elif value == exchange_field.vrednost:
                    color = colors[exchange_field.vrednost % 4]
                    exchange_field.y -= 2
                    pygame.draw.rect(screen, color, [width+exchange_field.x, height+exchange_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                else:
                    color = colors[value % 4]
                    pygame.draw.rect(screen, color, [width+field_x, height+field_y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1


    if move_direction == right:
        while zero_field.x < target_x:
            pygame.display.update()
            time.sleep(0.023)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    color = gray
                    zero_field.x += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state,exchange_field)
                    pygame.draw.rect(screen, color, [width+zero_field.x, height+zero_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                elif value == exchange_field.vrednost:
                    color = colors[exchange_field.vrednost % 4]
                    exchange_field.x -= 2
                    pygame.draw.rect(screen, color, [width+exchange_field.x, height+exchange_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                else:
                    color = colors[value % 4]
                    pygame.draw.rect(screen, color, [width+field_x, height+field_y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1


    if move_direction == left:
        while zero_field.x > target_x:
            pygame.display.update()
            time.sleep(0.023)
            for field in current_state:
                value = field.vrednost
                field_x = field.x
                field_y = field.y

                if value == 0:
                    color = gray
                    zero_field.x -= 2
                    pygame.draw.rect(screen, color, [width+zero_field.x, height+zero_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                elif value == exchange_field.vrednost:
                    color = colors[exchange_field.vrednost % 4]
                    exchange_field.x += 2
                    screen.fill(white)
                    draw_puzzle_without_animation_fields(current_state,exchange_field)
                    pygame.draw.rect(screen, color, [width+exchange_field.x, height+exchange_field.y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])
                else:
                    color = colors[value % 4]
                    pygame.draw.rect(screen, color, [width+field_x, height+field_y, puzzle_dimension/4 - border, puzzle_dimension/4 - border])

                if fields_in_row == 4:
                    fields_in_row = 1
                else:
                    fields_in_row = fields_in_row + 1



    pygame.display.update()
    time.sleep(0.3)
    puzzle.promena_stanja()
    current_state = puzzle.polja_slagalice
