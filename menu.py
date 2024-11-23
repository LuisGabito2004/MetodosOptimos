import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
#from metodos import MetodoEsquinaNoroeste, MetodoAproximacionVogel, MetodoCostoMinimo 

def create_table(rows, cols, metodo):
    def show_table():
        for widget in root.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(root, bg='white')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        entries = []
        for r in range(rows):
            row_entries = []
            for c in range(cols):
                entry = tk.Entry(frame)
                entry.grid(row=r, column=c)
                row_entries.append(entry)
            entries.append(row_entries)
        
        def get_data():
            data = []
            for row_entries in entries:
                row_data = [entry.get() for entry in row_entries]
                data.append(row_data)
            return data
        
        def siguiente():
            datos = get_data()
            print(datos)
            if metodo == "Metodo Esquina Noroeste":
                # = MetodoEsquinaNoroeste().resolver(datos)
                return
            elif metodo == "Metodo por Aproximación de Vogel":
                #resultado = MetodoAproximacionVogel().resolver(datos)
                return
            elif metodo == "Metodo del Costo Minimo":
                #resultado = MetodoCostoMinimo().resolver(datos)
                return
            
            show_final() #resultado
        
        button = tk.Button(frame, text="Siguiente", command=siguiente)
        button.grid(row=rows, columnspan=cols)

    return show_table

def show_final(resultado):
    for widget in root.winfo_children():
        widget.destroy()
    
    frame = tk.Frame(root, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    label = tk.Label(frame, text=resultado, font=("Arial", 12), bg='white')
    label.pack(pady=10)
    
    button = tk.Button(frame, text="Back", width=20, command=menu_inicio)
    button.pack(pady=10)

def show_inputs(metodo):
    for widget in root.winfo_children():
        widget.destroy()
    
    frame = tk.Frame(root, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    label1 = tk.Label(frame, text="Number of columns:", bg='white')
    label1.grid(row=0, column=0)
    entry1 = tk.Entry(frame)
    entry1.grid(row=0, column=1)
    
    label2 = tk.Label(frame, text="Number of rows:", bg='white')
    label2.grid(row=1, column=0)
    entry2 = tk.Entry(frame)
    entry2.grid(row=1, column=1)
    
    def generate_table():
        cols = int(entry1.get())
        rows = int(entry2.get())
        create_table(rows, cols, metodo)()
    
    button = tk.Button(frame, text="Generar Tabla del problema", bg="#2196F3", width=20, command=generate_table)
    button.grid(row=2, columnspan=2)

root = tk.Tk()
root.title("Main Window")

#tamaño de la ventana
aspect_ratio = 16 / 9
width = 800
height = int(width / aspect_ratio)
root.geometry(f"{width}x{height}")

def menu_inicio():
    for widget in root.winfo_children():
        widget.destroy()    
    
    # cargar imagen
    bg_image = Image.open("aaaaa.jpeg")
    bg_image = bg_image.resize((width, height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # label tiene la imagen
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # titulo en el centro
    title_label = tk.Label(root, text="Menu de Metodos", font=("Arial", 24), bg='white')
    title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    frame = tk.Frame(root, bg="#1B1D50")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    frame.lift()  # Trae el frame al frente de todo

    buttons_texts = ["Metodo Esquina Noroeste", "Metodo por Aproximación de Vogel", "Metodo del Costo Minimo"]
    
    for i in range(3):
        button = tk.Button(frame, text=buttons_texts[i], width=50, font=("Arial", 12), command=lambda i=i: show_inputs(buttons_texts[i]))
        button.lift()
        button.pack(pady=10)

menu_inicio()
root.mainloop()





