import itertools
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph
import sympy as sp

def procesar_expresiones():
    # Proposiciones
    oraciones = {
        'A': "Recibo ayuda",
        'B': "Me siento bien",
        'C': "Puedo salir de vacaciones"
    }

    # Definir las variables simbólicas
    A, B, C = sp.symbols('A B C')

    # Expresión lógica combinada
    expresion_comb = (sp.Not(A) | sp.Not(B)) & sp.Not(C)

    # Mostrar las proposiciones y la expresión lógica en la terminal
    print("Proposiciones:")
    for letra, frase in oraciones.items():
        print(f"{letra}: {frase}")
    print("\nFórmula combinada: (¬A ∨ ¬B) ∧ ¬C")
    print("Generando tablas e imágenes...")

    # Generar tabla de verdad para la expresión combinada
    combinaciones, resultados = generar_tabla_verdad(oraciones, expresion_comb)

    # Generar y mostrar la tabla de átomos
    generar_tabla_atomos(oraciones, combinaciones, resultados)

    # Generar árbol de decisiones
    generar_arbol(oraciones, combinaciones, resultados)

def generar_tabla_verdad(oraciones, expresion):
    variables = list(oraciones.keys())
    combinaciones = list(itertools.product([False, True], repeat=len(variables)))

    # Evaluación de la expresión para cada combinación, con 1 para True y 0 para False
    resultados = []
    for combinacion in combinaciones:
        contexto = dict(zip(variables, combinacion))
        resultado = expresion.subs(contexto).simplify()
        resultados.append(1 if bool(resultado) else 0)

    # Crear un DataFrame de pandas para la tabla de verdad
    nombre_formula = "(¬A ∨ ¬B) ∧ ¬C"
    tabla_verdad = pd.DataFrame(combinaciones, columns=variables)
    tabla_verdad = tabla_verdad.replace({True: 1, False: 0})  # Reemplazar True/False por 1/0
    tabla_verdad[nombre_formula] = resultados

    # Guardar la tabla de verdad como imagen
    guardar_tabla_como_imagen(tabla_verdad, "tabla_verdad.png")
    print("Imagen de la tabla de verdad guardada como 'tabla_verdad.png'.")

    return combinaciones, resultados

def generar_tabla_atomos(oraciones, combinaciones, resultados):
    variables = list(oraciones.keys())
    nombre_formula = "(¬A ∨ ¬B) ∧ ¬C"
    tabla_atomos = pd.DataFrame(combinaciones, columns=variables)
    tabla_atomos = tabla_atomos.replace({True: 1, False: 0})  # Reemplazar True/False por 1/0
    tabla_atomos[nombre_formula] = resultados

    # Guardar la tabla de átomos como imagen
    guardar_tabla_como_imagen(tabla_atomos, "tabla_atomos.png")
    print("Imagen de la tabla de átomos guardada como 'tabla_atomos.png'.")

def guardar_tabla_como_imagen(tabla, filename):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=tabla.values, colLabels=tabla.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    
    # Guardar la imagen
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)

def generar_arbol(oraciones, combinaciones, resultados):
    dot = Digraph()
    nodos = list(oraciones.keys())

    dot.node('Raiz', 'A')
    dot.node('A0', '0')
    dot.node('A1', '1')
    dot.edge('Raiz', 'A0', label='0')
    dot.edge('Raiz', 'A1', label='1')

    dot.node('B00', 'B=0')
    dot.node('B01', 'B=1')
    dot.edge('A0', 'B00', label='0')
    dot.edge('A0', 'B01', label='1')
    dot.node('B10', 'B=0')
    dot.node('B11', 'B=1')
    dot.edge('A1', 'B10', label='0')
    dot.edge('A1', 'B11', label='1')

    dot.node('C000', 'C=0')
    dot.node('C001', 'C=1')
    dot.node('C010', 'C=0')
    dot.node('C011', 'C=1')
    dot.node('C100', 'C=0')
    dot.node('C101', 'C=1')
    dot.node('C110', 'C=0')
    dot.node('C111', 'C=1')
    
    dot.edge('B00', 'C000', label='0')
    dot.edge('B00', 'C001', label='1')
    dot.edge('B01', 'C010', label='0')
    dot.edge('B01', 'C011', label='1')
    dot.edge('B10', 'C100', label='0')
    dot.edge('B10', 'C101', label='1')
    dot.edge('B11', 'C110', label='0')
    dot.edge('B11', 'C111', label='1')

    for i, combinacion in enumerate(combinaciones):
        estado_label = '1' if resultados[i] == 1 else '0'
        estado_color = 'green' if resultados[i] == 1 else 'red'
        estado_nombre = f"Estado_{i+1}"
        dot.node(estado_nombre, estado_label, color=estado_color)
        if combinacion == (False, False, False):
            dot.edge('C000', estado_nombre)
        elif combinacion == (False, False, True):
            dot.edge('C001', estado_nombre)
        elif combinacion == (False, True, False):
            dot.edge('C010', estado_nombre)
        elif combinacion == (False, True, True):
            dot.edge('C011', estado_nombre)
        elif combinacion == (True, False, False):
            dot.edge('C100', estado_nombre)
        elif combinacion == (True, False, True):
            dot.edge('C101', estado_nombre)
        elif combinacion == (True, True, False):
            dot.edge('C110', estado_nombre)
        elif combinacion == (True, True, True):
            dot.edge('C111', estado_nombre)

    dot.render('arbol_decisiones_updt', format='png', cleanup=True)
    print("Árbol de decisiones generado y guardado como 'arbol_decisiones_updt.png'.")

# Ejemplo de uso
procesar_expresiones()