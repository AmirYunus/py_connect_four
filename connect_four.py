import numpy as np
import pygame
import math

pygame.init()
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2*0.9)
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
FONT = pygame.font.SysFont("monospace", 75)

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, column, piece):
    board[row][column] = piece

def is_valid_location(board, column):
    return board[ROW_COUNT-1][column] == 0

def get_next_open_row(board, column):
    for row in range(ROW_COUNT):

        if board[row][column] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal
    for column in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column+1] == piece and board [row][column+2] == piece and board [row][column+3] == piece:
                return True

    # Check vertical
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][column] == piece and board[row+1][column] == piece and board [row+2][column] == piece and board [row+3][column] == piece:
                return True

    # Check diagonals
    for column in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][column] == piece and board[row+1][column+1] == piece and board [row+2][column+2] == piece and board [row+3][column+3] == piece:
                return True

    for column in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][column] == piece and board[row-1][column+1] == piece and board [row-2][column+2] == piece and board [row-3][column+3] == piece:
                return True

def draw_board(board):
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (column*SQUARE_SIZE, row*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (column*SQUARE_SIZE+int(SQUARE_SIZE/2), row*SQUARE_SIZE+SQUARE_SIZE+int(SQUARE_SIZE/2)), RADIUS)
    
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][column] == 1:
                pygame.draw.circle(screen, RED, (column*SQUARE_SIZE+int(SQUARE_SIZE/2), HEIGHT-(row*SQUARE_SIZE+int(SQUARE_SIZE/2))), RADIUS)

            elif board[row][column] == 2:
                pygame.draw.circle(screen, YELLOW, (column*SQUARE_SIZE+int(SQUARE_SIZE/2), HEIGHT-(row*SQUARE_SIZE+int(SQUARE_SIZE/2))), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board)
game_over = False
turn = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
draw_board(board)
pygame.display.update()

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARE_SIZE))
            if turn == 0:
                pygame.draw.circle(screen, RED, (event.pos[0], int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (event.pos[0], int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, WIDTH, SQUARE_SIZE))
            # Player 1
            if turn == 0:
                column = int(math.floor(event.pos[0]/SQUARE_SIZE))

                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 1)

                    if winning_move(board, 1):
                        text = "PLAYER 1 Wins!"
                        print(text)
                        label = FONT.render(text, 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

            # Player 2
            else:
                column = int(math.floor(event.pos[0]/SQUARE_SIZE))

                if is_valid_location(board, column):
                    row = get_next_open_row(board, column)
                    drop_piece(board, row, column, 2)

                if winning_move(board, 2):
                        text = "PLAYER 2 Wins!"
                        print(text)
                        label = FONT.render(text, 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)