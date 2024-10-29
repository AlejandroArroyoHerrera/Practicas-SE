import pandas as pd
from graphviz import Digraph

# Definimos la tabla de verdad para las operaciones AND y OR
data = {
    'A': [0, 0, 1, 1],
    'B': [0, 1, 0, 1],
    'A AND B': [0, 0, 0, 1],
    'A OR B': [0, 1, 1, 1]
}

# Convertimos la tabla de verdad a un DataFrame
truth_table = pd.DataFrame(data)

# Función para construir un árbol de decisión
def build_decision_tree(data):
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

# Generamos el árbol de decisión
decision_tree = build_decision_tree(truth_table)

# Guardamos y mostramos el grafo
decision_tree.render('decision_tree', format='png', cleanup=True)
decision_tree.view()
