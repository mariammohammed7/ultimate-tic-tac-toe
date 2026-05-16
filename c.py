import tkinter as tk
from tkinter import messagebox, font

class UltimateTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Tic Tac Toe")
        self.root.geometry("900x1000")
        self.root.configure(bg="#1a1a2e")

        # Game state
        self.board = [[None for i in range(9)] for j in range(9)]  # 9 small boards of 9 cells
        self.small_board_winners = [None] * 9  # Track winner of each small board
        self.current_player = 'X'
        self.active_small_board = None  # None means player can play anywhere
        self.game_over = False
        self.game_winner = None

        # UI Elements storage
        self.buttons = []  # All game buttons
        self.board_frames = []  # Frames for each small board

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Create the UI"""
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title = tk.Label(self.root, text="ULTIMATE TIC TAC TOE", font=title_font,
                         bg="#1a1a2e", fg="#00d4ff")
        title.pack(pady=10)

        # Status bar
        self.status_frame = tk.Frame(self.root, bg="#16213e", height=50)
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_label = tk.Label(self.status_frame, text="", font=("Arial", 14, "bold"),
                                     bg="#16213e", fg="#00ff00")
        self.status_label.pack(pady=5)

        # Main game board
        self.game_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.game_frame.pack(padx=10, pady=10)

        self.create_board_ui()

        # Control buttons
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(pady=10)

        reset_btn = tk.Button(button_frame, text="Reset Game", command=self.reset_game,
                              bg="#ff006e", fg="white", font=("Arial", 12, "bold"),
                              padx=10, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=5)

        instructions_btn = tk.Button(button_frame, text="Instructions", command=self.show_instructions,
                                     bg="#8338ec", fg="white", font=("Arial", 12, "bold"),
                                     padx=10, pady=5)
        instructions_btn.pack(side=tk.LEFT, padx=5)

        self.update_status()

    def create_board_ui(self):
        """Create the 3x3 grid of small boards"""
        self.buttons = []
        self.board_frames = []

        for big_idx in range(9):
            # Create frame for each small board
            board_frame = tk.Frame(self.game_frame, bg="#0f3460", relief=tk.RAISED,
                                   borderwidth=2)
            board_frame.grid(row=big_idx // 3, column=big_idx % 3, padx=2, pady=2)
            self.board_frames.append(board_frame)

            board_buttons = []
            for cell_idx in range(9):
                btn = tk.Button(board_frame, text="", font=("Arial", 16, "bold"),
                                width=4, height=2, bg="#16213e", fg="white",
                                command=lambda big=big_idx, cell=cell_idx: self.on_cell_click(big, cell),
                                activebackground="#2a3f5f")
                btn.grid(row=cell_idx // 3, column=cell_idx % 3, padx=1, pady=1)
                board_buttons.append(btn)

            self.buttons.append(board_buttons)

    def on_cell_click(self, big_board_idx, cell_idx):
        """Handle cell click"""
        if self.game_over:
            messagebox.showinfo("Game Over", f"Game is over! {self.game_winner} wins!")
            return

        # Check if move is valid
        if not self.is_valid_move(big_board_idx, cell_idx):
            messagebox.showwarning("Invalid Move", "You cannot play in this board!")
            return

        # Apply move
        self.apply_move(big_board_idx, cell_idx)

        # Check small board winner
        small_winner = self.check_small_board(big_board_idx)
        if small_winner:
            self.small_board_winners[big_board_idx] = small_winner
            self.update_small_board_display(big_board_idx)

        # Check big board winner
        big_winner, strike = self.check_big_board()
        if big_winner:
            self.game_over = True
            self.game_winner = big_winner
            if big_winner != 'Draw':
                # Note: draw_big_strike might not be implemented, check if it exists
                if hasattr(self, 'draw_big_strike'):
                    self.draw_big_strike(strike)
                messagebox.showinfo("Game Over!", f"Player {big_winner} wins the game!")
            else:
                messagebox.showinfo("Game Over!", "The game is a Draw!")
            return

        # Determine next active board
        if self.small_board_winners[cell_idx] is None:
            self.active_small_board = cell_idx
        else:
            self.active_small_board = None  # Can play anywhere

        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

        self.update_display()

    def is_valid_move(self, big_board_idx, cell_idx):
        """Check if move is valid"""
        # Cell must be empty
        if self.board[big_board_idx][cell_idx] is not None:
            return False

        # Small board must not be won
        if self.small_board_winners[big_board_idx] is not None:
            return False

        # If active board is set, must play there
        if self.active_small_board is not None:
            return big_board_idx == self.active_small_board

        return True

    def apply_move(self, big_board_idx, cell_idx):
        """Apply a move to the board"""
        self.board[big_board_idx][cell_idx] = self.current_player
        self.buttons[big_board_idx][cell_idx].config(text=self.current_player)

        # Update button color based on player
        if self.current_player == 'X':
            self.buttons[big_board_idx][cell_idx].config(fg="#38bdf8")
        else:
            self.buttons[big_board_idx][cell_idx].config(fg="#e879f9")

    def check_small_board(self, board_idx):
        """Check if small board has a winner"""
        cells = self.board[board_idx]

        # Check rows
        for i in range(0, 9, 3):
            if cells[i] and cells[i] == cells[i + 1] == cells[i + 2]:
                return cells[i]

        # Check columns
        for i in range(3):
            if cells[i] and cells[i] == cells[i + 3] == cells[i + 6]:
                return cells[i]

        # Check diagonals
        if cells[0] and cells[0] == cells[4] == cells[8]:
            return cells[0]
        if cells[2] and cells[2] == cells[4] == cells[6]:
            return cells[2]

        # Check for draw
        if all(cell is not None for cell in cells):
            return 'Draw'

        return None

    def check_big_board(self):
        w = self.small_board_winners

        wins = [
            (0, 1, 2, "row0"), (3, 4, 5, "row1"), (6, 7, 8, "row2"),
            (0, 3, 6, "col0"), (1, 4, 7, "col1"), (2, 5, 8, "col2"),
            (0, 4, 8, "diag1"), (2, 4, 6, "diag2")
        ]

        for a, b, c, kind in wins:
            if w[a] and w[a] != 'Draw' and w[a] == w[b] == w[c]:
                return w[a], kind

        if all(x is not None for x in w):
            return 'Draw', None

        return None, None

    def update_small_board_display(self, board_idx):
        frame = self.board_frames[board_idx]
        winner = self.small_board_winners[board_idx]

        # Disable all buttons in this small board
        for btn in self.buttons[board_idx]:
            btn.config(state=tk.DISABLED, bg="#1a1a2e")

        if winner == 'Draw':
            frame.config(bg="#333333")
            return

        # Color & symbol
        color = "#38bdf8" if winner == 'X' else "#e879f9"

        # Big symbol overlay
        big_label = tk.Label(
            frame,
            text=winner,
            font=("Arial", 80, "bold"),
            fg=color,
            bg="#1a1a2e"
        )

        # Place in center over the board
        big_label.place(relx=0.5, rely=0.5, anchor="center")

    def update_status(self):
        """Update status label"""
        if self.game_over:
            if self.game_winner == 'Draw':
                status = "Game Over! It's a Draw!"
            else:
                status = f"Player {self.game_winner} Wins!"
            self.status_label.config(text=status, fg="#ff00ff")
        else:
            if self.active_small_board is not None:
                status = f"Current Player: {self.current_player} | Play in Board {self.active_small_board + 1}"
            else:
                status = f"Current Player: {self.current_player} | Play Anywhere!"

            color = "#38bdf8" if self.current_player == 'X' else "#e879f9"
            self.status_label.config(text=status, fg=color)

    def update_display(self):
        """Update the entire display"""
        # Update highlighting for active board
        for i in range(len(self.board_frames)):
            frame = self.board_frames[i]
            if self.active_small_board is None or self.small_board_winners[i] is not None:
                if self.small_board_winners[i] is None:
                    frame.config(relief=tk.RAISED, bg="#0f3460")
            elif i == self.active_small_board:
                frame.config(relief=tk.SUNKEN, bg="#2a5f4a")
            else:
                frame.config(relief=tk.RAISED, bg="#0f3460")

        self.update_status()

    def reset_game(self):
        """Reset the game"""
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.small_board_winners = [None] * 9
        self.current_player = 'X'
        self.active_small_board = None
        self.game_over = False
        self.game_winner = None

        for big_idx in range(9):
            #delete labels
            for widget in self.board_frames[big_idx].winfo_children():
                if isinstance(widget, tk.Label):
                    widget.destroy()

            for cell_idx in range(9):
                self.buttons[big_idx][cell_idx].config(
                    text="",
                    fg="white",
                    bg="#16213e",
                    state=tk.NORMAL
                )

            self.board_frames[big_idx].config(bg="#0f3460", relief=tk.RAISED)

        self.update_display()

    def show_instructions(self):
        """Show game instructions"""
        instructions = """
ULTIMATE TIC TAC TOE - HOW TO PLAY

1. The game is played on a large 3x3 grid, where each cell contains a smaller 3x3 Tic-Tac-Toe board.

2. Your move determines where your opponent must play next.
   - If you place an X in the TOP-RIGHT square of a small board, the opponent must play in the TOP-RIGHT small board of the big grid.

3. If a small board is already won or full, and you are sent there, you can play anywhere on the big board.

4. Win a small board by getting 3 in a row (horizontally, vertically, or diagonally).

5. To win the game, you must win three small boards in a row (horizontally, vertically, or diagonally).

Good luck!
        """
        messagebox.showinfo("How to Play", instructions)


if __name__ == "__main__":
    root = tk.Tk()
    game = UltimateTicTacToe(root)
    root.mainloop()
