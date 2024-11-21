import numpy as np
import pandas as pd

def mostrar_tabla(oferta, demanda, costos, asignaciones):
    df = pd.DataFrame(costos, columns=[f"D{i+1}" for i in range(len(demanda))], 
                      index=[f"F{i+1}" for i in range(len(oferta))])
    df.loc[:, "Oferta"] = oferta
    df.loc["Demanda"] = demanda + [""]
    print("\nTabla actual:")
    print(df)
    print("\nAsignaciones:")
    print(asignaciones if np.any(asignaciones > 0) else "Sin asignaciones")
    print("-" * 40)

def metodo_costo_minimo(oferta, demanda, costos):
    oferta = oferta.copy()
    demanda = demanda.copy()
    filas = len(oferta)
    columnas = len(demanda)
    
    asignaciones = np.zeros((filas, columnas), dtype=int)
    
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
        
        # Mostrar tabla paso por paso
        mostrar_tabla(oferta, demanda, costos, asignaciones)
    
    # Calcular el costo total
    costo_total = np.sum(asignaciones * costos)
    return asignaciones, costo_total

# Solicitar datos al usuario
def obtener_datos():
    print("=== Método de Costo Mínimo ===")
    n_fuentes = int(input("Ingrese el número de fuentes: "))
    n_destinos = int(input("Ingrese el número de destinos: "))
    
    print("\nIngrese la oferta para cada fuente:")
    oferta = []
    for i in range(n_fuentes):
        oferta.append(int(input(f"Oferta de F{i+1}: ")))
    
    print("\nIngrese la demanda para cada destino:")
    demanda = []
    for i in range(n_destinos):
        demanda.append(int(input(f"Demanda de D{i+1}: ")))
    
    print("\nIngrese los costos de transporte:")
    costos = []
    for i in range(n_fuentes):
        while True:
            try:
                fila_costos = list(map(int, input(f"Costos de F{i+1} a cada destino separados por espacios: ").split()))
                if len(fila_costos) != n_destinos:
                    print(f"Por favor, ingrese exactamente {n_destinos} costos.")
                    continue
                costos.append(fila_costos)
                break
            except ValueError:
                print("Por favor, ingrese valores numéricos válidos separados por espacios.")
    
    return oferta, demanda, np.array(costos)

# Programa principal
if __name__ == "__main__":
    oferta, demanda, costos = obtener_datos()
    asignaciones, costo_total = metodo_costo_minimo(oferta, demanda, costos)
    
    print("\n=== Resultado Final ===")
    mostrar_tabla([0]*len(oferta), [0]*len(demanda), costos, asignaciones)
    print(f"Costo total mínimo: {costo_total}")

