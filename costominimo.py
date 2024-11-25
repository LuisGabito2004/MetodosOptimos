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

def return_string_results(resultados, costos, costo_total):
    """
    Returns a formatted string containing step-by-step results of the minimum cost method
    using fixed column width formatting.
    """
    result_string = ""
    col_width = 12  # Fixed column width

    for step, (oferta, demanda, asignaciones) in enumerate(resultados):
        # Add step header
        result_string += f"\n{'='*60}\n"
        result_string += f"Paso {step + 1}\n"
        result_string += f"{'='*60}\n\n"

        # Add tableau header
        num_cols = len(costos[0])
        header = "Tableau".center(col_width * (num_cols + 2)) + "\n"
        result_string += header

        # Column headers
        header_row = "".ljust(col_width)
        for j in range(num_cols):
            header_row += f"D{j+1}".ljust(col_width)
        header_row += "Oferta".ljust(col_width)
        result_string += header_row + "\n"

        # Add data rows
        for i in range(len(costos)):
            row = f"F{i+1}".ljust(col_width)
            for j in range(num_cols):
                # Format cost and assignment in one cell
                cost = costos[i][j]
                assigned = asignaciones[i][j]
                cell = f"{cost}({assigned})".ljust(col_width)
                row += cell
            row += str(oferta[i]).ljust(col_width)
            result_string += row + "\n"

        # Add demand row
        demand_row = "Demanda".ljust(col_width)
        for d in demanda:
            demand_row += str(d).ljust(col_width)
        result_string += demand_row + "\n\n"

    # Add total cost
    result_string += f"Costo total mínimo: {costo_total}\n"

    return result_string

def ejecutar_metodo_costo_minimo(datos, menu_inicio):
    """
    Ejecuta el Método de Costo Mínimo con los datos ingresados por el usuario.
    """
    try:
        demanda = [int(x) for x in datos[-1][:-1]]
        oferta = [int(row[-1]) for row in datos[:-1] if row]
        costos = [[int(x) for x in row[:-1]] for row in datos[:-1]]

        resultados, costo_total = metodo_costo_minimo_gui(oferta, demanda, np.array(costos))

        return return_string_results(resultados, np.array(costos), costo_total)
    except Exception as e:
        return f"Error", f"Ha ocurrido un error: {e}"

