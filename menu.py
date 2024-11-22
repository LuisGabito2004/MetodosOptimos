import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

def create_table(rows, cols):
    def show_table():
        for widget in root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(root)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        for r in range(rows):
            for c in range(cols):
                entry = tk.Entry(frame)
                entry.grid(row=r, column=c)
        
        button = tk.Button(frame, text="Siguiente", command=show_final)
        button.grid(row=rows, columnspan=cols)

    return show_table

def show_final():
    for widget in root.winfo_children():
        widget.destroy()
    
    frame = tk.Frame(root, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    button1 = tk.Button(frame, text="Metodo del Paso Secuencial", command=show_new_window)
    button1.pack(side=tk.TOP, pady=10)
    
    button2 = tk.Button(frame, text="Metodo de Distribución Modificada", command=show_new_window)
    button2.pack(side=tk.TOP, pady=10)
    
    text = tk.Text(frame, height=15, width=70, font=("Arial", 12))
    text.pack(fill=tk.BOTH, expand=True)

def show_new_window():
    for widget in root.winfo_children():
        widget.destroy()
    
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    button = tk.Button(frame, text="Atrás", width=20, command=menu_inicio)
    button.pack(pady=10)

    text = tk.Text(frame, height=15, width=70, font=("Arial", 12))
    text.pack(fill=tk.BOTH, expand=True)

def show_inputs():
    for widget in root.winfo_children():
        widget.destroy()
    
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    title_label = tk.Label(root, text="Agrega los datos", font=("Arial", 24))
    title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    label1 = tk.Label(frame, text="Numero de columnas de la tabla:")
    label1.grid(row=0, column=0)
    entry1 = tk.Entry(frame)
    entry1.grid(row=0, column=1)
    
    label2 = tk.Label(frame, text="Numero de filas de la tabla:")
    label2.grid(row=1, column=0)
    entry2 = tk.Entry(frame)
    entry2.grid(row=1, column=1)
    
    def generate_table():
        cols = int(entry1.get())
        rows = int(entry2.get())
        create_table(rows, cols)()
    
    button = tk.Button(frame, text="Generar Tabla del problema", bg="#2196F3", width=20, command=generate_table)
    button.grid(row=2, columnspan=2)

root = tk.Tk()
root.title("Main Window")

# Set the aspect ratio and size of the window
aspect_ratio = 16 / 9
width = 800
height = int(width / aspect_ratio)
root.geometry(f"{width}x{height}")

def menu_inicio():
    for widget in root.winfo_children():
        widget.destroy()    
    
    # Load the background image
    bg_image = Image.open("aaaaa.jpeg")
    bg_image = bg_image.resize((width, height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label to hold the background image
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = tk.Label(root, text="Menu de Metodos", font=("Arial", 24), bg='#1B1D50', fg="white")
    title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    frame = tk.Frame(root, bg="#1B1D50")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    frame.lift()  # Bring the frame to the front
    

    buttons_texts = ["Metodo Esquina Noroeste", "Metodo por Aproximación de Vogel", "Metodo del Costo Minimo"]
    
    for i in range(3):
        button = tk.Button(frame, text=buttons_texts[i], width=50, font=("Arial", 12), command=show_inputs)
        button.lift()
        button.pack(pady=10)
menu_inicio()
root.mainloop()








