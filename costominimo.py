import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd



def metodo_costo_minimo_gui(oferta, demanda, costos):
    """
    Implementa el Método de Costo Mínimo mostrando los pasos en una ventana de resultados de tkinter.
    """
    oferta = oferta.copy()
    demanda = demanda.copy()
    filas = len(oferta)
    columnas = len(demanda)
    asignaciones = np.zeros((filas, columnas), dtype=int)
    resultados = []

    while np.sum(oferta) > 0 and np.sum(demanda) > 0:
        # Encontrar la celda con el costo mínimo
        min_val = float('inf')
        fila, columna = -1, -1
        for i in range(filas):
            for j in range(columnas):
                if oferta[i] > 0 and demanda[j] > 0 and costos[i][j] < min_val:
                    min_val = costos[i][j]
                    fila, columna = i, j
        
        # Determinar la cantidad a asignar
        cantidad = min(oferta[fila], demanda[columna])
        asignaciones[fila][columna] = cantidad
        
        # Actualizar oferta y demanda
        oferta[fila] -= cantidad
        demanda[columna] -= cantidad

        # Registrar el estado actual
        resultados.append((oferta.copy(), demanda.copy(), asignaciones.copy()))

    # Calcular el costo total
    costo_total = np.sum(asignaciones * costos)
    return resultados, costo_total


def mostrar_resultados(resultados, costos, costo_total, menu_inicio):
    """
    Muestra los resultados paso a paso en una ventana gráfica usando tkinter.
    """
    result_window = tk.Toplevel()
    result_window.title("Resultados del Método de Costo Mínimo")
    result_window.geometry("800x600")

    text_widget = tk.Text(result_window, wrap="word", font=("Courier New", 12))
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    for i, (oferta, demanda, asignaciones) in enumerate(resultados):
        text_widget.insert("end", f"=== Paso {i + 1} ===\n")
        df = pd.DataFrame(costos, columns=[f"D{i+1}" for i in range(costos.shape[1])], 
                          index=[f"F{i+1}" for i in range(costos.shape[0])])
        df.loc[:, "Oferta"] = oferta
        df.loc["Demanda"] = demanda + [""]

        text_widget.insert("end", f"{df}\n")
        text_widget.insert("end", "Asignaciones:\n")
        text_widget.insert("end", f"{pd.DataFrame(asignaciones)}\n")
        text_widget.insert("end", "-" * 40 + "\n\n")

    text_widget.insert("end", f"Costo total mínimo: {costo_total}\n")
    text_widget.configure(state="disabled")
    back_button = tk.Button(result_window, text="Volver al Menú", command=lambda: [result_window.destroy(), menu_inicio()])
    back_button.pack(pady=10)

def ejecutar_metodo_costo_minimo(datos, menu_inicio):
    """
    Ejecuta el Método de Costo Mínimo con los datos ingresados por el usuario.
    """
    try:
        demanda = [int(x) for x in datos[-1][:-1]]
        oferta = [int(row[-1]) for row in datos[:-1] if row]
        costos = [[int(x) for x in row[:-1]] for row in datos[:-1]]

        resultados, costo_total = metodo_costo_minimo_gui(oferta, demanda, np.array(costos))
        mostrar_resultados(resultados, np.array(costos), costo_total, menu_inicio)
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {e}")


# Conectar esta función al menú principal
def show_inputs_costo_minimo():
    """
    Configura la ventana de inputs para el Método de Costo Mínimo.
    """
    show_inputs("Metodo del Costo Minimo")

