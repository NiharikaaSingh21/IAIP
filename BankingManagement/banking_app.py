import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

DATA_FILE = "users.txt"
users = {}

# ========= FILE HANDLING =========
def load_users():
    if not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split("|")
            u, p, b = parts[:3]
            h = parts[3] if len(parts) > 3 else ""
            users[u] = {
                "password": p,
                "balance": float(b),
                "history": h.split(",") if h else []
            }

def save_users():
    with open(DATA_FILE, "w") as f:
        for u, data in users.items():
            history = ",".join(data["history"])
            f.write(f"{u}|{data['password']}|{data['balance']}|{history}\n")

# =========  LOGIN WINDOW =========
class LoginApp:
    def __init__(self, root):
        self.root = root
        root.title("Online Banking System")
        root.geometry("600x400")
        root.resizable(False, False)

        try:
            self.bg_img = ImageTk.PhotoImage(
                Image.open("login.jpg").resize((600, 400))
            )
        except:
            self.bg_img = None

        canvas = tk.Canvas(root, width=600, height=400)
        canvas.pack(fill="both", expand=True)
        if self.bg_img:
            canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        self.card = tk.Frame(root, bg="#000000")
        self.card.place(relx=0.5, rely=0.5, anchor="center",
                        width=300, height=260)

        tk.Label(self.card, text="🏦 Secure Login",
                 fg="white", bg="#000000",
                 font=("Segoe UI", 16, "bold")).pack(pady=15)

        self.username = tk.Entry(self.card, font=("Segoe UI", 11))
        self.username.pack(pady=8)

        self.password = tk.Entry(self.card, font=("Segoe UI", 11), show="*")
        self.password.pack(pady=8)

        tk.Button(self.card, text="Login",
                  bg="#1f6aa5", fg="white",
                  width=18, command=self.login).pack(pady=10)

        tk.Button(self.card, text="Register",
                  bg="#2ecc71", fg="white",
                  width=18, command=self.register).pack()

    def login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()

        if u in users and users[u]["password"] == p:
            self.root.destroy()
            root = tk.Tk()
            Dashboard(root, u)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        win = tk.Toplevel(self.root)
        win.title("Register")
        win.geometry("300x230")
        win.resizable(False, False)

        tk.Label(win, text="Create Account",
                 font=("Segoe UI", 14, "bold")).pack(pady=10)

        user = tk.Entry(win)
        user.pack(pady=8)

        pwd = tk.Entry(win, show="*")
        pwd.pack(pady=8)

        def create():
            u = user.get().strip()
            p = pwd.get().strip()

            if not u or not p:
                messagebox.showerror("Error", "All fields required")
                return
            if u in users:
                messagebox.showerror("Error", "User already exists")
                return

            users[u] = {"password": p, "balance": 0.0, "history": []}
            save_users()
            messagebox.showinfo("Success", "Account created")
            win.destroy()

        tk.Button(win, text="Register",
                  bg="#1f6aa5", fg="white",
                  command=create).pack(pady=15)

#========= DASHBOARD =========
class Dashboard:
    def __init__(self, root, user):
        self.root = root
        self.user = user

        root.title("Bank Dashboard")
        root.geometry("800x500")
        root.resizable(False, False)

        try:
            self.bg_img = ImageTk.PhotoImage(
                Image.open("bg.jpeg").resize((800, 500))
            )
        except:
            self.bg_img = None

        canvas = tk.Canvas(root, width=800, height=500)
        canvas.pack(fill="both", expand=True)
        if self.bg_img:
            canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        self.main = tk.Frame(root, bg="#000000", highlightbackground="#444",
                             highlightthickness=1)
        self.main.place(relx=0.5, rely=0.5, anchor="center",
                        width=720, height=440)

        # Sidebar
        self.sidebar = tk.Frame(self.main, bg="#111111", width=200)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text=f"👤 {user}",
                 fg="white", bg="#111111",
                 font=("Segoe UI", 14, "bold")).pack(pady=20)

        self.nav_btn("Balance", self.show_balance)
        self.nav_btn("Deposit", self.deposit_view)
        self.nav_btn("Withdraw", self.withdraw_view)
        self.nav_btn("History", self.history_view)

        tk.Button(self.sidebar, text="Logout",
                  bg="#e74c3c", fg="white",
                  command=self.logout).pack(pady=20)

        # Content
        self.content = tk.Frame(self.main, bg="#222222")
        self.content.pack(side="right", expand=True, fill="both")

        self.show_balance()

    def nav_btn(self, text, cmd):
        tk.Button(self.sidebar, text=text,
                  bg="#1f6aa5", fg="white",
                  width=18, command=cmd).pack(pady=6)

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ========= BALANCE =========
    def show_balance(self):
        self.clear()
        bal = users[self.user]["balance"]

        tk.Label(self.content, text="Account Balance",
                 fg="white", bg="#222222",
                 font=("Segoe UI", 18, "bold")).pack(pady=30)

        tk.Label(self.content, text=f"₹ {bal:.2f}",
                 fg="#2ecc71", bg="#222222",
                 font=("Segoe UI", 32, "bold")).pack()

    # =========TRANSACTIONS =========
    def deposit_view(self):
        self.transaction_view("Deposit", True)

    def withdraw_view(self):
        self.transaction_view("Withdraw", False)

    def transaction_view(self, title, is_deposit):
        self.clear()

        tk.Label(self.content, text=title,
                 fg="white", bg="#222222",
                 font=("Segoe UI", 18, "bold")).pack(pady=20)

        entry = tk.Entry(self.content, font=("Segoe UI", 14))
        entry.pack(pady=10)

        def submit():
            try:
                amt = float(entry.get())
                if amt <= 0:
                    raise ValueError

                if not is_deposit and amt > users[self.user]["balance"]:
                    messagebox.showerror("Error", "Insufficient funds")
                    return

                users[self.user]["balance"] += amt if is_deposit else -amt
                action = "Deposited" if is_deposit else "Withdrawn"
                users[self.user]["history"].append(f"{action} ₹{amt:.2f}")
                save_users()
                self.show_balance()

            except ValueError:
                messagebox.showerror("Transaction Successful",
                                    "Check History for the further clarifications  ")

        tk.Button(self.content, text="Submit",
                  bg="#2ecc71", fg="white",
                  command=submit).pack(pady=15)

    # ========= HISTORY =========
    def history_view(self):
        self.clear()

        tk.Label(self.content, text="Transaction History",
                 fg="white", bg="#222222",
                 font=("Segoe UI", 18, "bold")).pack(pady=10)

        text = tk.Text(self.content, height=15, width=45,
                       bg="#121212", fg="white",
                       font=("Consolas", 11))
        text.pack(pady=10)

        history = users[self.user]["history"]
        if history:
            for h in history:
                text.insert(tk.END, h + "\n")
        else:
            text.insert(tk.END, "No transactions yet")

        text.config(state="disabled")

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginApp(root)
        root.mainloop()

load_users()
root = tk.Tk()
LoginApp(root)
root.mainloop()
