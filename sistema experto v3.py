import itertools
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph
import sympy as sp

def procesar_expresiones():
    # Solicitar la oración al usuario
    oracion = input("Ingrese la oración lógica: ")
    
    # Procesar la oración para extraer proposiciones y conectores
    proposiciones, expresion_comb = procesar_oracion(oracion)
    
    # Mostrar las proposiciones y la expresión lógica
    print("\nProposiciones:", proposiciones)
    print("\nFórmula combinada:", expresion_comb)
    print("Generando tablas e imágenes...")

    # Generar tabla de verdad para la expresión combinada
    combinaciones, resultados = generar_tabla_verdad(proposiciones, expresion_comb)

    # Generar y mostrar la tabla de átomos
    generar_tabla_atomos(proposiciones, combinaciones, resultados)

    # Generar árbol de decisiones
    generar_arbol(proposiciones, combinaciones, resultados)

def procesar_oracion(oracion):
    # Separar proposiciones por "y" y "o"
    partes = [part.strip() for part in oracion.replace("o", " or ").split("y")]
    proposiciones = []
    expresion = []
    
    for parte in partes:
        subpartes = [p.strip() for p in parte.split("or")]
        proposiciones.extend(subpartes)
        if len(subpartes) > 1:
            expresion.append(sp.Or(*[sp.symbols(p) for p in subpartes]))
        else:
            expresion.append(sp.symbols(subpartes[0]))

    # Combinar expresiones AND
    if expresion:
        return proposiciones, sp.And(*expresion)
    return proposiciones, None

def generar_tabla_verdad(proposiciones, expresion):
    variables = list(set(proposiciones))
    combinaciones = list(itertools.product([False, True], repeat=len(variables)))

    # Evaluación de la expresión para cada combinación
    resultados = []
    for combinacion in combinaciones:
        contexto = dict(zip(variables, combinacion))
        resultado = expresion.subs(contexto).simplify()
        resultados.append(1 if bool(resultado) else 0)

    # Crear un DataFrame de pandas para la tabla de verdad
    nombre_formula = str(expresion)
    tabla_verdad = pd.DataFrame(combinaciones, columns=variables)
    tabla_verdad = tabla_verdad.replace({True: 1, False: 0})  # Reemplazar True/False por 1/0
    tabla_verdad[nombre_formula] = resultados

    # Guardar la tabla de verdad como imagen
    guardar_tabla_como_imagen(tabla_verdad, "tabla_verdad.png")
    print("Imagen de la tabla de verdad guardada como 'tabla_verdad.png'.")

    return combinaciones, resultados

def generar_tabla_atomos(proposiciones, combinaciones, resultados):
    variables = list(set(proposiciones))
    nombre_formula = str(sp.And(*[sp.Not(sp.symbols(var)) for var in variables]))
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

def generar_arbol(proposiciones, combinaciones, resultados):
    dot = Digraph()
    nodos = list(set(proposiciones))

    # Crear nodos de decisiones según el número de proposiciones
    for i, var in enumerate(nodos):
        dot.node(var, var)
        if i > 0:  # Conectar a los nodos anteriores
            for j in range(2):  # 0 y 1
                dot.edge(nodos[i-1], f"{var}{j}", label=str(j))

    # Generar nodos finales según las combinaciones
    for i, combinacion in enumerate(combinaciones):
        estado_label = '1' if resultados[i] == 1 else '0'
        estado_color = 'green' if resultados[i] == 1 else 'red'
        estado_nombre = f"Estado_{i+1}"
        dot.node(estado_nombre, estado_label, color=estado_color)
        
        # Conectar con el nodo correspondiente
        dot.edge(f"{nodos[-1]}{int(combinacion[-1])}", estado_nombre)

    dot.render('arbol_decisiones_actualizado', format='png', cleanup=True)
    print("Árbol de decisiones generado y guardado como 'arbol_decisiones_actualizado.png'.")

# Ejemplo de uso
procesar_expresiones()
