import pandas as pd
from graphviz import Digraph

# Función para construir un árbol de decisión
def build_decision_tree():
    dot = Digraph()

    # Agregamos nodos y bordes al grafo
    dot.node('A', 'A')
    dot.node('B', 'B')

    # Lógica para AND
    dot.node('AND', 'A AND B')
    dot.edge('A', 'AND', 'A=1')
    dot.edge('B', 'AND', 'B=1')

    # Lógica para OR
    dot.node('OR', 'A OR B')
    dot.edge('A', 'OR', 'A=1')
    dot.edge('B', 'OR', 'B=1')

    return dot

def main():
    # Solicitar la entrada de A y B
    a = int(input("Ingrese el valor de A (0 o 1): "))
    b = int(input("Ingrese el valor de B (0 o 1): "))

    # Validar la entrada
    if a not in (0, 1) or b not in (0, 1):
        print("Por favor, ingrese 0 o 1.")
        return

    # Crear la tabla de verdad
    data = {
        'A': [0, 0, 1, 1],
        'B': [0, 1, 0, 1],
        'A AND B': [(x & y) for x, y in zip([0, 0, 1, 1], [0, 1, 0, 1])],
        'A OR B': [(x | y) for x, y in zip([0, 0, 1, 1], [0, 1, 0, 1])]
    }

    truth_table = pd.DataFrame(data)

    # Mostrar la tabla de verdad
    print("\nTabla de Verdad:")
    print(truth_table)

    # Generar el árbol de decisión
    decision_tree = build_decision_tree()

    # Guardar y mostrar el grafo
    decision_tree.render('decision_tree', format='png', cleanup=True)
    decision_tree.view()

if __name__ == "__main__":
    main()