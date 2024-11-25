import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
from NWCM import NWCM
from costominimo import ejecutar_metodo_costo_minimo

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
                entry.grid(row=r+1, column=c+1)  # Ajustar la posición de las entradas
                if r == rows - 1 and c == cols - 1:
                    entry.config(state='disabled')  # Deshabilitar la última celda de la última fila
                row_entries.append(entry)
            entries.append(row_entries)
    
        
        # Añadir labels de "Demanda" y números de fila
        for r in range(rows):
            label = tk.Label(frame, text=str(r), bg='white')
            label.grid(row=r, column=0)  # Ajustar la posición de los labels de fila
        
        demanda_label = tk.Label(frame, text="Demanda", bg='white')
        demanda_label.grid(row=rows, column=0)  # Ajustar la posición del label "Demanda"

        # Añadir labels de "Oferta" y números de columna
        for c in range(cols):
            label = tk.Label(frame, text=str(c), bg='white')
            label.grid(row=0, column=c)  # Ajustar la posición de los labels de columna
        
        oferta_label = tk.Label(frame, text="Oferta", bg='white')
        oferta_label.grid(row=0, column=cols)  # Ajustar la posición del label "Oferta"
        
        def get_data():
            data = []
            for row_entries in entries:
                row_data = []
                for entry in row_entries:
                    if entry is not None:  # Verificar que entry no sea None
                        value = entry.get()
                        if value == "":  # Asignar 0 a celdas vacías
                            value = 0
                        try:
                            value = float(value)
                            if value < 0:
                                raise ValueError("Negative value")
                        except ValueError:
                            messagebox.showerror("Error", "Valor no válido")
                            return None
                        row_data.append(value)
                    else:
                        row_data.append(None)  # Añadir None para mantener la estructura
                data.append(row_data)
            return data

        
        def siguiente():
            datos = get_data()  # Matriz completa
            print(datos)
            try:
                # Lógica de procesamiento común
                demand = [int(x) for x in datos[-1][:-1]]
                supply = [int(row[-1]) for row in datos[:-1] if row]
                cost_matrix = [[int(x) for x in row[:-1]] for row in datos[:-1]]

                if metodo == "Metodo Esquina Noroeste":
                    result = NWCM(cost_matrix, supply, demand).get_result()
                    show_final(result)
                elif metodo == "Metodo por Aproximación de Vogel":
                    # Implementar lógica para Aproximación de Vogel si existe
                    pass
                elif metodo == "Metodo del Costo Minimo":
                    ejecutar_metodo_costo_minimo(datos, menu_inicio)  # Llama al método desde costominimo.py
            except Exception as e:
                messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

        button = tk.Button(frame,pady=5 ,text="Siguiente", font=("Arial", 12), bg="#2196F3", fg='white', width=30, bd=0, command=siguiente)
        button.grid(row=rows+2, columnspan=cols+2)

    return show_table

def show_final(resultado):
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un contenedor
    container = tk.Frame(root, bg='white')
    container.pack(fill="both", expand=True)

    # Canvas y Scroll
    canvas = tk.Canvas(container, bg='white')
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # crear frame 
    content_frame = tk.Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    content_frame.config(width=canvas.winfo_width(), height=canvas.winfo_height() * 2)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Crear un widget Text para mostrar el contenido
    text_widget = tk.Text(content_frame, font=("Helvetica", 12), bg='white', wrap="none")
    text_widget.pack(fill="both", expand=True)

     # Configurar las tabulaciones del widget Text
    tab_width = 4  # Ajusta este valor según sea necesario
    text_widget.config(tabs=(tab_width * 10,))

    # Añadir el resultado al widget Text
    text_widget.insert(tk.END, resultado)
    text_widget.config(state=tk.DISABLED)  # Hacer el widget de solo lectura

    # Boton de regresar
    button = tk.Button(content_frame, text="Regresar", font=("Arial", 12), bg="#2196F3", fg='white', width=40, bd=0, command=menu_inicio)
    button.pack(pady=20)

    # Adjust the canvas scrollregion dynamically
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Enable mouse wheel scrolling
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)


def show_inputs(metodo):
    for widget in root.winfo_children():
        widget.destroy()
    
    frame = tk.Frame(root, bg='white')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    label_font = ("Helvetica", 16)
    entry_font = ("Helvetica", 16)
    button_font = ("Helvetica", 16)
    
    label1 = tk.Label(frame, text="Número de Columnas:", font=label_font, bg='white')
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = tk.Entry(frame, font=entry_font, width=10)
    entry1.grid(row=0, column=1, padx=10, pady=10)
    
    label2 = tk.Label(frame, text="Número de Filas:", font=label_font, bg='white')
    label2.grid(row=1, column=0, padx=10, pady=10)
    entry2 = tk.Entry(frame, font=entry_font, width=10)
    entry2.grid(row=1, column=1, padx=10, pady=10)
    
    def generate_table():
        cols = int(entry1.get())
        rows = int(entry2.get())
        create_table(rows, cols, metodo)()
    
    button = tk.Button(frame,pady=5 ,text="Generar Tabla del problema", font=button_font, bg="#2196F3", fg='white', width=40, command=generate_table, bd=0)
    button.grid(row=2, columnspan=2, pady=20)

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
    title_label = tk.Label(root, text="Menú de Metodos", font=("Arial", 24), bg='white')
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




