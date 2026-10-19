import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import re

class BisectionSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Метод половинного ділення (Бісекцій)")
        self.root.geometry("1000x700")
        
        # --- Ліва панель: Керування ---
        left_panel = tk.Frame(root, width=350, bg="#f0f0f0")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Заголовок
        tk.Label(left_panel, text="Метод бісекцій", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(10, 5), anchor="w")
        
        # Ввід рівняння
        tk.Label(left_panel, text="Рівняння f(x) = 0:", font=("Arial", 10), bg="#f0f0f0").pack(pady=(15, 0), anchor="w")
        tk.Label(left_panel, text="(Використовуйте 'x', 'sin(x)', 'cos(x)' тощо)", font=("Arial", 8, "italic"), bg="#f0f0f0", fg="gray").pack(anchor="w")
        self.eq_entry = tk.Entry(left_panel, width=40, font=("Consolas", 11))
        # Ваше рівняння
        self.eq_entry.insert(0, "x - sin(x + 2) - 0.25")
        self.eq_entry.pack(pady=5)
        
        # Параметри
        param_frame = tk.Frame(left_panel, bg="#f0f0f0")
        param_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(param_frame, text="a (початок):", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.a_entry = tk.Entry(param_frame, width=10)
        self.a_entry.insert(0, "0")
        self.a_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(param_frame, text="b (кінець):", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        self.b_entry = tk.Entry(param_frame, width=10)
        self.b_entry.insert(0, "2")
        self.b_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(param_frame, text="Точність (eps):", bg="#f0f0f0").grid(row=2, column=0, sticky="w")
        self.eps_entry = tk.Entry(param_frame, width=10)
        self.eps_entry.insert(0, "0.0001")
        self.eps_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Кнопка
        btn_solve = tk.Button(left_panel, text="Розв'язати", command=self.solve, 
                              bg="#2196F3", fg="white", font=("Arial", 12, "bold"), pady=8)
        btn_solve.pack(pady=20, fill=tk.X)
        
        # Результати (текст)
        tk.Label(left_panel, text="Результати:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.result_text = tk.Text(left_panel, height=15, width=40, font=("Consolas", 10))
        self.result_text.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # --- Права панель: Графік ---
        right_panel = tk.Frame(root)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.figure, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Підпис автора
        footer_frame = tk.Frame(root)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        tk.Label(footer_frame, text="Виконав студент групи 4М Бачок Микола", 
                 font=("Arial", 9, "italic"), fg="gray").pack(side=tk.RIGHT)

    def prepare_expression(self, expr_str):
        """Автоматично додає math. до математичних функцій"""
        math_funcs = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                      'exp', 'log', 'log10', 'sqrt', 'ceil', 'floor', 'fabs', 'pi', 'e']
        
        expr_str = expr_str.replace('^', '**')
        
        for func in math_funcs:
            pattern = r'(?<![\w.])' + func + r'\b'
            expr_str = re.sub(pattern, f'math.{func}', expr_str)
            
        return expr_str

    def get_f(self, x_val):
        """Обчислення значення функції з введеного рядка"""
        try:
            # Створюємо словник з усіма математичними функціями
            safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            safe_dict.update({'abs': abs, 'min': min, 'max': max})
            # ВАЖЛИВО: Додаємо сам модуль math у словник, щоб eval бачив "math.sin"
            safe_dict['math'] = math
            safe_dict['x'] = x_val
            
            # Підготовлюємо вираз
            expr = self.prepare_expression(self.eq_entry.get())
            
            # Обчислюємо
            return eval(expr, {"__builtins__": None}, safe_dict)
        except Exception as e:
            raise ValueError(f"Помилка у рівнянні: {e}")

    def solve(self):
        self.result_text.delete(1.0, tk.END)
        
        # Зчитування параметрів
        try:
            a = float(self.a_entry.get().replace(',', '.'))
            b = float(self.b_entry.get().replace(',', '.'))
            eps = float(self.eps_entry.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Помилка", "Перевірте правильність введення чисел.")
            return

        self.result_text.insert(tk.END, f"Метод: Половинного ділення\n")
        self.result_text.insert(tk.END, f"Рівняння: {self.eq_entry.get()} = 0\n")
        self.result_text.insert(tk.END, f"Інтервал: [{a}, {b}], Точність: {eps}\n")
        self.result_text.insert(tk.END, "-"*40 + "\n")

        # Перевірка знаків на кінцях
        try:
            fa = self.get_f(a)
            fb = self.get_f(b)
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))
            return

        if fa * fb > 0:
            self.result_text.insert(tk.END, "Помилка: Функція не змінює знак на кінцях інтервалу!\n")
            self.result_text.insert(tk.END, f"f({a}) = {fa:.4f}\n")
            self.result_text.insert(tk.END, f"f({b}) = {fb:.4f}\n")
            return

        # --- Реалізація методу бісекцій ---
        iter_count = 0
        c = a
        while (b - a) / 2 > eps:
            c = (a + b) / 2
            fc = self.get_f(c)
            
            self.result_text.insert(tk.END, f"Ітерація {iter_count+1}: c = {c:.6f}, f(c) = {fc:.6f}\n")
            
            if fc == 0:
                break
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
            iter_count += 1
            
            if iter_count > 1000:
                self.result_text.insert(tk.END, "Перевищено ліміт ітерацій.\n")
                break

        root_val = (a + b) / 2
        self.result_text.insert(tk.END, "-"*40 + "\n")
        self.result_text.insert(tk.END, f"Знайдений корінь: x = {root_val:.6f}\n")
        self.result_text.insert(tk.END, f"Кількість ітерацій: {iter_count}\n")
        self.result_text.insert(tk.END, f"Значення f(x): {self.get_f(root_val):.2e}\n")
        
        self.plot_graph(a, b, root_val)

    def plot_graph(self, a, b, root=None):
        self.ax.clear()
        x_vals = np.linspace(a - 1, b + 1, 400)
        y_vals = []
        
        for val in x_vals:
            try:
                y_vals.append(self.get_f(val))
            except:
                y_vals.append(0)
        
        self.ax.plot(x_vals, y_vals, label="f(x)")
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        
        self.ax.axvline(a, color='gray', linestyle='--', alpha=0.5)
        self.ax.axvline(b, color='gray', linestyle='--', alpha=0.5)
        
        if root is not None:
            self.ax.plot(root, self.get_f(root), 'ro', label=f"Корінь: {root:.4f}")
            self.ax.annotate(f"{root:.4f}", (root, self.get_f(root)), 
                             textcoords="offset points", xytext=(0,10), ha='center')
            
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Графік функції")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = BisectionSolverApp(root)
    root.mainloop()