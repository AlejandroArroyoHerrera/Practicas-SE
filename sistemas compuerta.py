# -*- coding: utf-8 -*-

import re
import string
import itertools
import pandas as pd
import matplotlib.pyplot as plt

from graphviz import Digraph  # Asegúrate de tener instalado graphviz

def procesar_texto(texto):
    # Operadores booleanos
    operador = {
        'y': '^',
        'o': 'v',
        'no': '~',
        '-': ' '
    }

    partes = re.split(r'\s+(y|o|no|-)\s+', texto)

    oraciones = {}
    variable_index = 0
    for parte in partes:
        if parte not in operador:
            oracion = parte.strip()
            if oracion:
                variable = string.ascii_lowercase[variable_index]
                oraciones[variable] = oracion
                variable_index += 1

    # Construir la fórmula lógica
    expres = ""
    variable_index = 0
    for parte in partes:
        if parte in operador:
            if parte == "y":
                expres += " ^ "
            elif parte == "o":
                expres += " v "
        else:
            if parte.strip():
                variable = string.ascii_lowercase[variable_index]
                expres += variable
                variable_index += 1

    # Mostrar las proposiciones y ecuación
    for letra, frase in oraciones.items():
        print(f"{letra}: {frase}")
    
    print("\nEcuación:")
    print(expres)

    # Crear tabla de verdad con visualización gráfica
    combinaciones, resultados = generar_tabla_verdad(oraciones, expres)

    # Crear el árbol de nodos basado en la tabla de verdad
    generar_arbol_de_nodos(combinaciones, resultados, list(oraciones.keys()))


def generar_tabla_verdad(oraciones, expres):
    variables = list(oraciones.keys())
    combinaciones = list(itertools.product([False, True], repeat=len(variables)))

    # Evaluación de la expresión para cada combinación
    resultados = []
    for combinacion in combinaciones:
        contexto = dict(zip(variables, combinacion))

        # Reemplazar variables en la expresión con sus valores en 'contexto'
        expresi_eval = expres
        for var, val in contexto.items():
            expresi_eval = expresi_eval.replace(var, str(val))

        # Evaluar la expresión lógica
        resultado = eval(expresi_eval.replace('^', ' and ').replace('v', ' or '))
        resultados.append(resultado)

    # Crear un DataFrame de pandas para la tabla de verdad
    tabla_v = pd.DataFrame(combinaciones, columns=variables)
    tabla_v[expres] = resultados  # Usar la fórmula como título de la columna de resultado

    # Graficar la tabla de estados como imagen
    fig, ax = plt.subplots(figsize=(8, 4))  # Ajustar tamaño si es necesario
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=tabla_v.values,
                     colLabels=tabla_v.columns,
                     cellLoc='center', loc='center')
    tabla.scale(1.2, 1.2)  # Ajustar escala si es necesario
    plt.show()

    return combinaciones, resultados


def generar_arbol_de_nodos(combinaciones, resultados, variables):
    # Crear el gráfico del árbol usando graphviz
    arbol = Digraph(format='png', graph_attr={'rankdir': 'TB'})  # Orientación de arriba hacia abajo

    # Crear un nodo raíz
    arbol.node('Raiz', 'Combinaciones')

    # Conectamos el primer nivel basado en el valor de la primera variable
    for i in range(len(variables)):
        var = variables[i]
        arbol.node(var, f"{var}")
        arbol.edge('Raiz', var)

        # Agregar los nodos de las combinaciones para el valor verdadero
        for comb in combinaciones:
            if comb[i]:  # Si la variable es True
                idx = combinaciones.index(comb)
                arbol.node(f"Estado_{idx + 1}", 'y', color='green')  # Palomita verde
                arbol.edge(var, f"Estado_{idx + 1}")

        # Agregar los nodos de las combinaciones para el valor falso
        for comb in combinaciones:
            if not comb[i]:  # Si la variable es False
                idx = combinaciones.index(comb)
                arbol.node(f"Estado_{idx + 1}", 'x', color='red')  # Equis roja
                arbol.edge(var, f"Estado_{idx + 1}")

    # Renderizar y mostrar el árbol
    arbol.render('arbol_de_nodos', view=True)  # Esto genera y abre el archivo PNG del árbol


# Ejemplo de uso
texto_in = "Hoy es lunes y está lloviendo, o voy al trabajo. y hay tráfico en la carretera"
print(texto_in, "\n")
procesar_texto(texto_in)

