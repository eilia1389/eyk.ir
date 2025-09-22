import tkinter as tk
import random
from tkinter import messagebox

ROWS, COLS = 5, 5   # 5x5
CIRCLE_SIZE = 70
PADDING = 30
SHOW_TIME = 2000  # میلی‌ثانیه

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 بازی حافظه رنگی")
        tk.Label(self.root, text="Please wait until the circles turn white ⚪", font=("Arial", 15), fg="#1BC800").pack(pady=13)
        self.canvas = tk.Canvas(root, width=COLS*CIRCLE_SIZE+PADDING*2, 
                                height=ROWS*CIRCLE_SIZE+PADDING*2, bg="white")
        self.canvas.pack()

        self.circles = []
        self.correct_indices = set()
        self.selected_indices = set()
        self.level = 1  # مرحله اول

        self.create_grid()
        self.start_game()

    def create_grid(self):
        """ساخت دایره‌ها و bind کردن کلیک‌ها"""
        for r in range(ROWS):
            for c in range(COLS):
                x1 = PADDING + c*CIRCLE_SIZE
                y1 = PADDING + r*CIRCLE_SIZE
                x2 = x1 + CIRCLE_SIZE - 10
                y2 = y1 + CIRCLE_SIZE - 10
                circle = self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")
                self.circles.append(circle)
                # bind صحیح با استفاده از آرگومان پیش‌فرض
                self.canvas.tag_bind(circle, "<Button-1>", lambda e, idx=len(self.circles)-1: self.on_click(idx))

    def start_game(self):
        """شروع یا مرحله بعد بازی"""
        self.correct_indices.clear()
        self.selected_indices.clear()

        # انتخاب دایره‌های رنگی بر اساس مرحله
        count = min(self.level, len(self.circles))  # اگر level بیشتر از تعداد دایره‌ها شد
        self.correct_indices = set(random.sample(range(len(self.circles)), count))

        for idx in self.correct_indices:
            self.canvas.itemconfig(self.circles[idx], fill="red")
        
        # بعد از SHOW_TIME رنگ‌ها مخفی شوند
        self.root.after(SHOW_TIME, self.hide_colors)

    def hide_colors(self):
        """مخفی کردن رنگ‌ها"""
        for idx in self.correct_indices:
            self.canvas.itemconfig(self.circles[idx], fill="white")

    def on_click(self, idx):
        """کلیک بازیکن"""
        if idx in self.selected_indices:
            return
        self.selected_indices.add(idx)

        if idx in self.correct_indices:
            self.canvas.itemconfig(self.circles[idx], fill="green")
        else:
            self.canvas.itemconfig(self.circles[idx], fill="black")
            messagebox.showerror("باختی 😢", "اشتباه زدی! دوباره تلاش کن.")
            self.level = 1
            self.reset_game()
            return 

        if self.selected_indices == self.correct_indices:
            messagebox.showinfo("بردی 🎉", f"آفرین! مرحله {self.level} رو تموم کردی 🎯")
            self.level += 1
            self.reset_game()

    def reset_game(self):
        """شروع دوباره یا مرحله بعد"""
        for circle in self.circles:
            self.canvas.itemconfig(circle, fill="white")
        self.root.after(1000, self.start_game)


# اجرای بازی
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
