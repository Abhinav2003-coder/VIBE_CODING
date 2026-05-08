import tkinter as tk

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x450")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        
        # Turn Label
        self.turn_label = tk.Label(root, text="Player X's Turn", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333333")
        self.turn_label.pack(pady=10)
        
        # Grid Frame
        self.grid_frame = tk.Frame(root, bg="#333333")
        self.grid_frame.pack()
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        for row in range(3):
            for col in range(3):
                btn = tk.Button(self.grid_frame, text="", font=("Helvetica", 24, "bold"), width=5, height=2,
                                command=lambda r=row, c=col: self.on_click(r, c),
                                bg="#ffffff", fg="#333333", relief="raised", bd=2)
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[row][col] = btn
                
        # Reset Button
        self.reset_btn = tk.Button(root, text="Restart Game", font=("Helvetica", 14, "bold"), command=self.reset_game, bg="#4CAF50", fg="white", relief="raised", bd=2)
        self.reset_btn.pack(pady=20)
        
    def on_click(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            
            if self.current_player == "X":
                self.buttons[row][col].config(fg="#2196F3") # Blue for X
            else:
                self.buttons[row][col].config(fg="#f44336") # Red for O
                
            if self.check_winner():
                self.show_result_screen(f"Player {self.current_player} Wins!")
                self.turn_label.config(text=f"Player {self.current_player} Wins!")
            elif self.check_draw():
                self.show_result_screen("It's a Draw!")
                self.turn_label.config(text="It's a Draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(text=f"Player {self.current_player}'s Turn")
                
    def show_result_screen(self, message):
        result_window = tk.Toplevel(self.root)
        result_window.title("Game Over")
        result_window.geometry("300x200")
        result_window.configure(bg="#2b2b2b")
        result_window.resizable(False, False)
        
        # Make the result window modal
        result_window.transient(self.root)
        result_window.grab_set()
        
        # Center the window relative to the main window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (300 // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (200 // 2)
        result_window.geometry(f"+{x}+{y}")
        
        lbl = tk.Label(result_window, text=message, font=("Helvetica", 20, "bold"), bg="#2b2b2b", fg="#ffffff")
        lbl.pack(expand=True)
        
        def play_again():
            self.reset_game()
            result_window.destroy()
            
        btn_frame = tk.Frame(result_window, bg="#2b2b2b")
        btn_frame.pack(pady=20)
        
        play_btn = tk.Button(btn_frame, text="Play Again", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=play_again, width=10, relief="raised", bd=2)
        play_btn.pack(side="left", padx=10)
        
        close_btn = tk.Button(btn_frame, text="Close", font=("Helvetica", 12, "bold"), bg="#f44336", fg="white", command=result_window.destroy, width=10, relief="raised", bd=2)
        close_btn.pack(side="right", padx=10)
        
    def check_winner(self):
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                return True
        # Check cols
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False
        
    def check_draw(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "":
                    return False
        return True
        
    def reset_game(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.turn_label.config(text="Player X's Turn")
        
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", fg="#333333")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
