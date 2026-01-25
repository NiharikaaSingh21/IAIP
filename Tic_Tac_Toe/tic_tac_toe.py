import tkinter as tk
import random

BG = "#7180a6"
CARD = "#ba9191"
BORDER = "#303a48"
RED = "#771414"
BLUE = "#0e326d"
TEXT = "#0f172a"
MUTED = "#6b7280"
HOVER = "#f1f5f9"

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("440x600")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.mode = None
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False

        self.mode_screen()

    def mode_screen(self):
        self.clear()

        card = self.glass_card(80, 140, 280, 300)

        tk.Label(card, text="TIC TAC TOE",
                 font=("Segoe UI", 22, "bold"),
                 bg=CARD, fg=TEXT).pack(pady=(20, 5))

        tk.Label(card, text="Choose Game Mode",
                 font=("Segoe UI", 11),
                 bg=CARD, fg=MUTED).pack(pady=10)

        self.action_button(card, "👥 Multiplayer", lambda: self.start("multi")).pack(pady=15)
        self.action_button(card, "🤖 Single Player vs AI", lambda: self.start("ai")).pack()

    def game_ui(self):
        self.clear()
        self.game_over = False

        self.status_card = self.glass_card(30, 20, 380, 100)

        self.status_label = tk.Label(
            self.status_card,
            text="👤 Player ❌ Turn",
            font=("Segoe UI", 14, "bold"),
            bg=CARD,
            fg=RED
        )
        self.status_label.pack(pady=25)

        board_frame = tk.Frame(self.root, bg=BG)
        board_frame.place(relx=0.5, rely=0.55, anchor="center")

        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI", 30, "bold"),
                width=3,
                height=1,
                bg=CARD,
                relief="solid",
                bd=1,
                highlightbackground=BORDER,
                cursor="hand2",
                command=lambda i=i: self.move(i)
            )
            btn.grid(row=i//3, column=i%3, padx=6, pady=6)
            self.add_hover(btn)
            self.buttons.append(btn)

        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(side="bottom", pady=30)

        self.action_button(bottom, "🔄 Restart", self.reset).pack(side="left", padx=10)
        self.action_button(bottom, "⬅ Change Mode", self.mode_screen).pack(side="left")

    def start(self, mode):
        self.mode = mode
        self.board = [""] * 9
        self.current_player = "X"
        self.game_ui()

    def move(self, idx):
        if self.board[idx] or self.game_over:
            return

        self.place(idx)

        if self.check_winner():
            self.show_winner()
            return

        if "" not in self.board:
            self.show_tie()
            return

        self.switch_player()

        if self.mode == "ai" and self.current_player == "O":
            self.root.after(500, self.ai_move)

    def place(self, idx):
        self.board[idx] = self.current_player
        if self.current_player == "X":
            self.buttons[idx].config(text="❌", fg=RED)
        else:
            self.buttons[idx].config(text="⭕", fg=BLUE)

    def ai_move(self):
        empty = [i for i, v in enumerate(self.board) if v == ""]
        idx = random.choice(empty)
        self.place(idx)

        if self.check_winner():
            self.status_label.config(
                text="🤖 AI Wins!",
                fg=BLUE
            )
            self.end_game()
            return

        if "" not in self.board:
            self.show_tie()
            return

        self.switch_player()

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
            self.status_label.config(text="👤 Player ⭕ Turn", fg=BLUE)
        else:
            self.current_player = "X"
            self.status_label.config(text="👤 Player ❌ Turn", fg=RED)

    def check_winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(self.board[a] == self.board[b] == self.board[c] != "" for a,b,c in wins)

    def show_winner(self):
        text = "👤 Player 1❌ Wins!" if self.current_player == "X" else "👤 Player2 ⭕ Wins!"
        color = RED if self.current_player == "X" else BLUE
        self.status_label.config(text=text, fg=color)
        self.end_game()

    def show_tie(self):
        self.status_label.config(text="🤝 It's a Tie", fg=MUTED)
        self.end_game()

    def end_game(self):
        self.game_over = True
        for b in self.buttons:
            b.config(state="disabled")

    def glass_card(self, x, y, w, h):
        shadow = tk.Frame(self.root, bg="#e5e7eb")
        shadow.place(x=x+4, y=y+4, width=w, height=h)

        card = tk.Frame(self.root, bg=CARD)
        card.place(x=x, y=y, width=w, height=h)
        return card

    def action_button(self, parent, text, cmd):
        btn = tk.Button(parent,text=text,font=("Segoe UI", 11, "bold"),bg=CARD,fg=TEXT,relief="solid",bd=1,padx=15,pady=8,cursor="hand2",command=cmd
        )
        self.add_hover(btn)
        return btn

    def add_hover(self, widget):
        widget.bind("<Enter>", lambda e: widget.config(bg=HOVER))
        widget.bind("<Leave>", lambda e: widget.config(bg=CARD))

    def reset(self):
        self.start(self.mode)

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()
