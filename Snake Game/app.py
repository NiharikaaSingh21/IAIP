import tkinter as tk
import random
import os
from PIL import Image, ImageTk

# ---------------- CONFIG ---------------- #
WIDTH, HEIGHT = 800, 550
BOX = 20
SPEED = 120
BUSH = 40
HIGH_SCORE_FILE = "highscore.txt"

SNAKE_BODY = "#2f855a"
SNAKE_HEAD = "#14532d"
FOOD_COLOR = "#b91c1c"
BUSH_COLOR = "#166534"
MAZE_COLOR = "#3f6212"


# ================= START WINDOW ================= #
class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Courtyard Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()

        bg = Image.open("front.jpg").resize((WIDTH, HEIGHT))
        self.bg_img = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        self.canvas.create_text(
            WIDTH // 2, 100,
            text="COURTYARD SNAKE",
            font=("Segoe UI", 28, "bold"),
            fill="white"
        )

        self.create_btn("▶ START GAME", 220, self.start_game)
        self.create_btn("🏆 HIGHEST SCORE", 280, self.show_score)
        self.create_btn("❌ EXIT", 340, root.destroy)

    def create_btn(self, text, y, cmd):
        btn = tk.Button(
            self.root, text=text, command=cmd,
            font=("Segoe UI", 12, "bold"),
            bg="#ca8a04", fg="white",
            relief="flat", width=18
        )
        self.canvas.create_window(WIDTH // 2, y, window=btn)

    def start_game(self):
        self.canvas.destroy()
        CourtyardSnake(self.root)

    def show_score(self):
        top = tk.Toplevel(self.root)
        top.title("🏆 Highest Score")
        top.resizable(False, False)

        score = 0
        if os.path.exists(HIGH_SCORE_FILE):
            score = int(open(HIGH_SCORE_FILE).read())

        tk.Label(
            top, text=f"🏆 Highest Score\n\n{score}",
            font=("Segoe UI", 18, "bold"),
            padx=40, pady=30
        ).pack()


# ================= GAME ================= #
class CourtyardSnake:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack()

        bg = Image.open("courtyard.png").resize((WIDTH, HEIGHT))
        self.bg_img = ImageTk.PhotoImage(bg)

        self.high_score = self.load_high_score()

        self.root.bind("<Up>", lambda e: self.set_dir(0, -1))
        self.root.bind("<Down>", lambda e: self.set_dir(0, 1))
        self.root.bind("<Left>", lambda e: self.set_dir(-1, 0))
        self.root.bind("<Right>", lambda e: self.set_dir(1, 0))

        self.start_game()

    def start_game(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        self.snake = [(200, 200), (180, 200), (160, 200)]
        self.direction = (1, 0)
        self.score = 0
        self.running = True
        self.food = self.spawn_food()

        self.draw_bushes()
        self.draw_maze()
        self.game_loop()

    # -------- BUSHES -------- #
    def draw_bushes(self):
        self.bush_zones = []
        for x in range(0, WIDTH, BUSH):
            self.bush_zones.append((x, 0, x + BUSH, BUSH))
            self.bush_zones.append((x, HEIGHT - BUSH, x + BUSH, HEIGHT))
        for y in range(BUSH, HEIGHT - BUSH, BUSH):
            self.bush_zones.append((0, y, BUSH, y + BUSH))
            self.bush_zones.append((WIDTH - BUSH, y, WIDTH, y + BUSH))

        for z in self.bush_zones:
            self.canvas.create_rectangle(*z, fill=BUSH_COLOR, outline="")

    # -------- MAZE (ONE BARRIER REMOVED) -------- #
    def draw_maze(self):
        self.maze = [
            (300, 120, 320, 420),
            (500, 160, 520, 460)
        ]
        for m in self.maze:
            self.canvas.create_rectangle(*m, fill=MAZE_COLOR, outline="")

    def set_dir(self, x, y):
        if (-x, -y) != self.direction:
            self.direction = (x, y)

    def spawn_food(self):
        x = random.randint(3, (WIDTH - 60) // BOX) * BOX
        y = random.randint(3, (HEIGHT - 60) // BOX) * BOX
        return x, y

    def game_loop(self):
        if not self.running:
            return

        hx, hy = self.snake[0]
        dx, dy = self.direction
        new = (hx + dx * BOX, hy + dy * BOX)

        if new in self.snake or self.hit_wall(new):
            self.game_over()
            return

        self.snake.insert(0, new)

        if new == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(SPEED, self.game_loop)

    def hit_wall(self, pos):
        x, y = pos
        for a in self.bush_zones + self.maze:
            if a[0] <= x < a[2] and a[1] <= y < a[3]:
                return True
        return False

    def draw(self):
        self.canvas.delete("snake", "food", "text")

        for i, (x, y) in enumerate(self.snake):
            c = SNAKE_HEAD if i == 0 else SNAKE_BODY
            self.canvas.create_oval(x+2, y+2, x+18, y+18, fill=c, outline="", tag="snake")

        fx, fy = self.food
        self.canvas.create_oval(fx+3, fy+3, fx+17, fy+17, fill=FOOD_COLOR, outline="", tag="food")

        self.canvas.create_text(
            WIDTH//2, 15,
            text=f"Score: {self.score} | High Score: {self.high_score}",
            font=("Segoe UI", 14, "bold"),
            tag="text"
        )

    def game_over(self):
        self.running = False

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        self.canvas.create_rectangle(260, 200, 540, 350, fill="#f5f5f4", outline="")
        self.canvas.create_text(WIDTH//2, 230, text="GAME OVER", font=("Segoe UI", 22, "bold"), fill="red")
        self.canvas.create_text(WIDTH//2, 270, text=f"Score: {self.score}", font=("Segoe UI", 14))

        tk.Button(self.root, text="▶ Play Again", command=self.start_game).place(x=350, y=300)

    def load_high_score(self):
        return int(open(HIGH_SCORE_FILE).read()) if os.path.exists(HIGH_SCORE_FILE) else 0

    def save_high_score(self):
        open(HIGH_SCORE_FILE, "w").write(str(self.high_score))


# ================= RUN ================= #
if __name__ == "__main__":
    root = tk.Tk()
    StartWindow(root)
    root.mainloop()
