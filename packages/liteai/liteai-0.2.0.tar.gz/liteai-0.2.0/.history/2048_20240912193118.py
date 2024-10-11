import random

def initialize_game():
    return [[0 for _ in range(4)] for _ in range(4)]

def add_new_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def print_board(board):
    for row in board:
        print(' '.join(f'{tile:4d}' for tile in row))
    print()

def move(board, direction):
    def move_row(row):
        new_row = [tile for tile in row if tile != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [tile for tile in new_row if tile != 0]
        return new_row + [0] * (4 - len(new_row))

    if direction in 'lr':
        board = [move_row(row) if direction == 'r' else move_row(row[::-1])[::-1] for row in board]
    else:
        board = list(map(list, zip(*board)))
        board = [move_row(row) if direction == 'd' else move_row(row[::-1])[::-1] for row in board]
        board = list(map(list, zip(*board)))
    
    return board

def play_game():
    board = initialize_game()
    add_new_tile(board)
    add_new_tile(board)
    
    while True:
        print_board(board)
        direction = input("Enter direction (u/d/l/r) or 'q' to quit: ").lower()
        
        if direction == 'q':
            break
        
        if direction in 'udlr':
            new_board = move(board, direction)
            if new_board != board:
                board = new_board
                add_new_tile(board)
            
            if all(all(tile != 0 for tile in row) for row in board):
                print("Game Over!")
                break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    play_game()
