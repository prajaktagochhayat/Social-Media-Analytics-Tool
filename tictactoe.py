# Tic-Tac-Toe Game in Python using tkinter for simple graphics
# This code creates a 3x3 Tic-Tac-Toe game with a graphical window.
# It uses tkinter, which is built-in to Python, for buttons, labels, and message boxes.
# The game is two-player, detects wins/draws, and has a restart button.

import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox  # For popup messages

# Global variables for the game state
board = [[' ' for _ in range(3)] for _ in range(3)]  # 3x3 board, ' ' for empty, 'X' or 'O'
current_player = 'X'  # Current player, starts with X
game_over = False  # Flag to check if the game has ended

# Function to check if there's a winner or draw
def check_winner():
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    # Check for draw (all cells filled, no winner)
    if all(cell != ' ' for row in board for cell in row):
        return 'Draw'
    return None  # No winner yet

# Function to handle button clicks (when a player clicks a cell)
def button_click(row, col):
    global current_player, game_over
    if game_over or board[row][col] != ' ':  # If game over or cell not empty, do nothing
        return
    board[row][col] = current_player  # Place X or O
    buttons[row][col].config(text=current_player)  # Update button text
    winner = check_winner()  # Check for winner
    if winner:
        game_over = True
        if winner == 'Draw':
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
    else:
        current_player = 'O' if current_player == 'X' else 'X'  # Switch player
        turn_label.config(text=f"Player {current_player}'s turn")  # Update turn label

# Function to restart the game
def restart_game():
    global board, current_player, game_over
    board = [[' ' for _ in range(3)] for _ in range(3)]  # Reset board
    current_player = 'X'  # Reset to X
    game_over = False  # Reset game over flag
    turn_label.config(text="Player X's turn")  # Reset turn label
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=' ')  # Clear button texts

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")  # Window title

# Create a label to show whose turn it is
turn_label = tk.Label(root, text="Player X's turn", font=('Arial', 14))
turn_label.pack(pady=10)  # Add to window with padding

# Create a frame for the grid
frame = tk.Frame(root)
frame.pack()

# Create 3x3 grid of buttons
buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(frame, text=' ', font=('Arial', 20), width=5, height=2,
                                      command=lambda r=row, c=col: button_click(r, c))
        buttons[row][col].grid(row=row, column=col)

# Create a restart button
restart_button = tk.Button(root, text="Restart Game", font=('Arial', 12), command=restart_game)
restart_button.pack(pady=10)  # Add to window with padding

# Start the GUI event loop
root.mainloop()