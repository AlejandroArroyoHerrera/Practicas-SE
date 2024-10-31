import itertools
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph
import sympy as sp

def procesar_expresiones():
    # Ingresar una única oración
    oracion = input("Ingrese una oración: ")
    
    # Procesar la oración para obtener proposiciones y la expresión lógica
    oraciones, expresion_comb = procesar_oracion(oracion)
    
    # Definir las variables simbólicas
    variables = sp.symbols(' '.join(oraciones.keys()))
    
    # Mostrar las proposiciones y la expresión lógica en la terminal
    print("\nProposiciones:")
    for letra, frase in oraciones.items():
        print(f"{letra}: {frase}")
    print("\nFórmula combinada:", expresion_comb)
    print("Generando tablas e imágenes...")

    # Generar tabla de verdad para la expresión combinada
    combinaciones, resultados = generar_tabla_verdad(oraciones, expresion_comb)

    # Generar y mostrar la tabla de átomos
    generar_tabla_atomos(oraciones)

    # Generar árbol de decisiones
    generar_arbol(oraciones, combinaciones, resultados)

def procesar_oracion(oracion):
    # Separar la oración en proposiciones
    oracion = oracion.replace("es", "es").strip()
    proposiciones = []
    
    # Separar primero por " y " y " o "
    partes_y = oracion.split(' y ')
    for parte in partes_y:
        sub_partes = parte.split(' o ')
        proposiciones.extend(sub_partes)
    
    # Asignar letras a cada proposición y eliminar espacios en blanco
    proposiciones = [p.strip() for p in proposiciones if p.strip()]
    oraciones = {chr(65 + i): p for i, p in enumerate(proposiciones)}
    
    # Crear la expresión lógica combinada
    expresion_comb = sp.Or(*[sp.symbols(chr(65 + i)) for i in range(len(proposiciones))]) if len(proposiciones) > 1 else sp.symbols('A')
    
    # Conectar 'y' como conjunción
    if ' y ' in oracion:
        expresion_comb = sp.And(*[sp.symbols(chr(65 + i)) for i in range(len(proposiciones))])
    
    return oraciones, expresion_comb

def generar_tabla_verdad(oraciones, expresion):
    variables = list(oraciones.keys())
    combinaciones = list(itertools.product([False, True], repeat=len(variables)))

    # Evaluación de la expresión para cada combinación
    resultados = []
    for combinacion in combinaciones:
        contexto = dict(zip(variables, combinacion))
        resultado = expresion.subs(contexto).simplify()
        resultados.append(1 if bool(resultado) else 0)

    return combinaciones, resultados

def generar_tabla_atomos(oraciones):
    # Crear la tabla de átomos como imagen
    atomos = [(f"Átomo {i + 1}", oraciones[letra]) for i, letra in enumerate(oraciones.keys())]
    
    # Convertir a DataFrame para mejor visualización
    df_atom = pd.DataFrame(atomos, columns=["Átomo", "Proposición"])
    
    # Crear la figura y la tabla
    fig, ax = plt.subplots(figsize=(6, len(atomos) * 0.5))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df_atom.values, colLabels=df_atom.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    # Guardar la imagen
    plt.savefig("tabla_atom.png", bbox_inches='tight')
    plt.close(fig)
    print("Imagen de la tabla de átomos guardada como 'tabla_atom.png'.")

def generar_arbol(oraciones, combinaciones, resultados):
    dot = Digraph()
    dot.attr(rankdir='TB')  # Cambiar la dirección del gráfico
    nodos = list(oraciones.keys())

    # Crear un nodo raíz
    dot.node('Raiz', 'Decisiones')

    # Generar nodos y conexiones según las combinaciones
    for i, combinacion in enumerate(combinaciones):
        for j, var in enumerate(nodos):
            # Crear nodo solo con la letra
            dot.node(f"{var}_{i}", var)  # Nodo con letra
            if j == 0:
                dot.edge('Raiz', f"{var}_{i}", label=str(1 if combinacion[j] else 0))  # Etiqueta en la rama
            else:
                dot.edge(f"{nodos[j-1]}_{i}", f"{var}_{i}", label=str(1 if combinacion[j] else 0))  # Etiqueta en la rama

        # Colorear el último nodo según el resultado
        estado_color = 'green' if resultados[i] == 1 else 'red'
        dot.node(f"Estado_{i}", str(resultados[i]), color=estado_color)
        dot.edge(f"{nodos[-1]}_{i}", f"Estado_{i}", label=str(resultados[i]))

    dot.render('arbol_decisiones_actualizado', format='png', cleanup=True)
    print("Árbol de decisiones generado y guardado como 'arbol_decisiones_actualizado.png'.")

# Ejemplo de uso
procesar_expresiones()

