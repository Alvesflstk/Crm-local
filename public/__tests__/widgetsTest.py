import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import time


root = tk.Tk()
root.title("Barra de Progresso")

# Variável para armazenar o valor da barra de progresso
progresso = 0

# Barra de progresso
barra_progresso = ctk.CTkProgressBar(root, mode="determinate",determinate_speed=0.1)
barra_progresso.pack(pady=20)

# Iniciar a atualização da barra de progresso
atualizar_progresso()

root.mainloop()
