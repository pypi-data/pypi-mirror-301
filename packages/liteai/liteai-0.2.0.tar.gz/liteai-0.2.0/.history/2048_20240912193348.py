import random
import tkinter as tk
from tkinter import messagebox

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
    def move_row(row, co):

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

class Game2048(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.master.title('2048')
        self.main_grid = tk.Frame(self, bg='#92877d', bd=3, width=400, height=400)
        self.main_grid.grid(pady=(80, 0))
        self.create_widgets()
        self.board = initialize_game()
        self.cells = []
        self.init_matrix()
        self.update_GUI()
        self.mainloop()

    def create_widgets(self):
        # Create score header
        self.score_frame = tk.Frame(self)
        self.score_frame.place(relx=0.5, y=40, anchor="center")
        self.score_label = tk.Label(self.score_frame, text="Score")
        self.score_label.grid(row=0)
        self.score_value = tk.Label(self.score_frame, text="0")
        self.score_value.grid(row=1)

        # Create grid
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg='#9e948a',
                    width=100,
                    height=100
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg='#9e948a')
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # Bind arrow keys
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

    def init_matrix(self):
        add_new_tile(self.board)
        add_new_tile(self.board)

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.board[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg='#9e948a')
                    self.cells[i][j]["number"].configure(bg='#9e948a', text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=self.get_cell_color(cell_value))
                    self.cells[i][j]["number"].configure(
                        bg=self.get_cell_color(cell_value),
                        fg=self.get_number_color(cell_value),
                        font=("Helvetica", 20, "bold"),
                        text=str(cell_value)
                    )
        self.update_idletasks()

    def get_cell_color(self, value):
        cell_colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
            128: "#edcf72", 256: "#edcc61", 512: "#edc850",
            1024: "#edc53f", 2048: "#edc22e"
        }
        return cell_colors.get(value, "#3c3a32")

    def get_number_color(self, value):
        return "#776e65" if value <= 4 else "#f9f6f2"

    def left(self, event):
        self.board = move(self.board, 'l')
        self.update_game()

    def right(self, event):
        self.board = move(self.board, 'r')
        self.update_game()

    def up(self, event):
        self.board = move(self.board, 'u')
        self.update_game()

    def down(self, event):
        self.board = move(self.board, 'd')
        self.update_game()

    def update_game(self):
        add_new_tile(self.board)
        self.update_GUI()
        if self.is_game_over():
            messagebox.showinfo("Game Over", "Game Over!")

    def is_game_over(self):
        return all(all(tile != 0 for tile in row) for row in self.board)

if __name__ == "__main__":
    root = tk.Tk()
    Game2048(root)
