import re
import itertools
import os
import matplotlib.pyplot as plt

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def Formula(oracion):    
    operadores = {
        " y ": "∧", 
        " o ": "∨", 
        "∧no ": "∧¬",
        "∨no ": "∨¬",
        "No ": "¬",
        " pero ": "∧", 
        " además, ": "∧", 
        " Además, ": "∧",
    }   
  
    for conector, simbolo in operadores.items():
        oracion = oracion.replace(conector, simbolo)
    frase = Separador(oracion)

    frases_vistas = {}
    contador = 1
    def reemplazar_por_variable(match):
        nonlocal contador
        frase = match.group(0)
        if frase in frases_vistas:
            return frases_vistas[frase]
        else:
            resultado = f"X{contador}"
            frases_vistas[frase] = resultado 
            contador += 1
            return resultado
    formula = re.sub(r"[^∧∨¬]+", reemplazar_por_variable, oracion)
    formula = Separador(formula)
    return formula, frase

def Separador(oracion):
    separacion = oracion.replace("∧", "☺∧☺")
    separacion = separacion.replace("∨", "☺∨☺")
    separacion = separacion.replace("¬", "☺¬☺")
    separacion = re.split(r"☺", separacion)
    separacion = [elemento for elemento in separacion if elemento != '']
    return separacion

def Unir(frase):
    union = ""
    for i in range(len(frase)):
        union = union + frase[i]
    return union

def Tabla_Atomos(formula, frase):
    res_formula = Unir(formula)
    res_frase = Unir(frase)
    res_frase = re.split(r'[∧∨¬]', res_frase)
    res_frase = [elemento for elemento in res_frase if elemento != '']
    res_formula = re.split(r'[∧∨¬]', res_formula)
    res_formula = [elemento for elemento in res_formula if elemento != '']
    array_var = []
    vistos = set()
    for elemento in res_formula:
        if elemento not in vistos:
            vistos.add(elemento)
            array_var.append(elemento)
    array_frase = []
    vistos2 = set()
    for elemento in res_frase:
        if elemento not in vistos2:
            vistos2.add(elemento)
            array_frase.append(elemento)
    print("Tabla de Átomos")
    print("____________________________")
    for i in range(len(array_frase)):
        print("____________________________\n")
        print(array_var[i] + ":" + array_frase[i])
        print("____________________________")
    print("____________________________")
    return 

def Tabla_Booleana(oracion):
    formula = Unir(oracion)
    print(formula)
    formula_python = formula.replace("∧", " and ").replace("∨", " or ").replace("¬", " not ")
    variables = sorted(set(re.findall(r'X\d+', formula)))
    valores = [True, False]
    combinaciones = list(itertools.product(valores, repeat=len(variables)))

    encabezado = "\t".join(variables) + "\tResultado"
    print(encabezado)
    print("-" * (len(encabezado) + 1))
    
    for combinacion in combinaciones:
        contexto = dict(zip(variables, combinacion))
        try:
            resultado = eval(formula_python, {}, contexto)
        except Exception as e:
            resultado = f"Error: {e}"
        valores_str = "\t".join(str(contexto[var]) for var in variables)
        print(f"{valores_str}\t{resultado}")
    return

def Guardar(oracion):
    formula = Unir(oracion)
    if not os.path.exists("Reglas.txt"):
        with open("Reglas.txt", 'w', encoding='utf-8') as archivo:
            print("Archivo Reglas.txt creado.")

    with open("Reglas.txt", 'a', encoding='utf-8') as archivo:
        archivo.write(formula + ".\n")
        print("Nueva información agregada exitosamente.")
    return 

def Cargar():
    if os.path.exists("Reglas.txt"):
        with open("Reglas.txt", 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            return contenido
    else:
        print("No se ha generado ningún archivo")
        return

def Asignar(oracion):
    formula, _ = Formula(oracion)
    variables = sorted(set(re.findall(r'X\d+', Unir(formula))))
    valores_asignados = {}
    
    print("Asignación de valores:")
    for var in variables:
        while True:
            valor = input(f"Ingrese el valor de verdad para {var} (True/False): ")
            if valor.lower() in ['true', 'false']:
                valores_asignados[var] = valor.lower() == 'true'
                break
            else:
                print("Valor inválido. Ingrese 'True' o 'False'.")
    return valores_asignados

def Ver(oracion, valores_asignados):
    formula, _ = Formula(oracion)
    formula_str = Unir(formula)
    
    formula_evaluada = formula_str
    for var, valor in valores_asignados.items():
        formula_evaluada = formula_evaluada.replace(var, str(valor))
    
    formula_python = formula_evaluada.replace("∧", " and ").replace("∨", " or ").replace("¬", " not ")

    try:
        resultado = eval(formula_python)
    except Exception as e:
        resultado = f"Error: {e}"
    
    print("Expresión:", formula_str)
    print("Con valores asignados:", formula_evaluada)
    print("Resultado final:", resultado)
    return resultado

def construir_arbol(variables):
    if not variables:
        return None

    lista_variables = list(variables.keys())
    raiz = Nodo(lista_variables[0])
    cola = [(raiz, 1)]

    while cola:
        padre, idx = cola.pop(0)

        if idx < len(lista_variables):
            var_actual = lista_variables[idx]

            p_nodo_true = Nodo(f"{var_actual} = True")
            p_nodo_false = Nodo(f"{var_actual} = False")

            padre.derecha = p_nodo_true
            padre.izquierda = p_nodo_false

            cola.append((p_nodo_false, idx + 1))
            cola.append((p_nodo_true, idx + 1))

    return raiz

def construir_arbol_global(reglas):
    if not reglas:
        return None

    raiz = Nodo(reglas[0])
    cola = [(raiz, 1)]

    while cola:
        padre, idx = cola.pop(0)

        if idx < len(reglas):
            regla_actual = reglas[idx]

            p_nodo_true = Nodo(f"{regla_actual} = True")
            p_nodo_false = Nodo(f"{regla_actual} = False")

            padre.derecha = p_nodo_true
            padre.izquierda = p_nodo_false

            cola.append((p_nodo_false, idx + 1))
            cola.append((p_nodo_true, idx + 1))

    return raiz

def dibujar_arbol(nodo, x=0, y=0, dx=1.5, dy=1, ax=None, nivel=0, max_nivel=5):
    if nodo is None or nivel > max_nivel:
        return

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')

    ax.text(x, y, nodo.valor, ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", ec="black", lw=1))

    if nodo.izquierda:
        ax.plot([x, x - dx], [y, y - dy], 'k-')
        dibujar_arbol(nodo.izquierda, x - dx, y - dy, dx * 0.6, dy, ax, nivel + 1, max_nivel)

    if nodo.derecha:
        ax.plot([x, x + dx], [y, y - dy], 'k-')
        dibujar_arbol(nodo.derecha, x + dx, y - dy, dx * 0.6, dy, ax, nivel + 1, max_nivel)

    if nivel == 0:
        plt.show()

def Arbol_binario(oracion):
    formula, _ = Formula(oracion)
    variables = sorted(set(re.findall(r'X\d+', Unir(formula))))
    variables_asignadas = {var: False for var in variables}
    
    print(f"Dibujando árbol binario para la fórmula: {Unir(formula)}")
    raiz = construir_arbol(variables_asignadas)
    dibujar_arbol(raiz)

def Arbol_binario_global():
    reglas_texto = Cargar()
    if reglas_texto:
        reglas = [linea.strip()[:-1] for linea in reglas_texto.splitlines() if linea.strip()]  # Quitar el punto final
        print("Construyendo árbol binario global con las reglas:")
        for regla in reglas:
            print(f"Regla: {regla}")

        raiz_global = construir_arbol_global(reglas)
        dibujar_arbol(raiz_global)
    else:
        print("No hay reglas cargadas para construir el árbol.")
def Horn():
    # Cargar las reglas desde el archivo
    reglas_texto = Cargar()
    if reglas_texto:
        reglas = [linea.strip()[:-1] for linea in reglas_texto.splitlines() if linea.strip()]  # Quitar el punto final
        clausulas_horn = []

        for regla in reglas:
            # Reemplazar todos los ∧ por ∨
            regla = regla.replace('∧', '∨')
            
            # Separar los literales en la regla
            literales = regla.split("∨")
            # Negar todos los literales excepto el último, y no negar si ya está negado
            clausula_horn = []
            for literal in literales[:-1]:
                literal = literal.strip()
                # Verificar si ya está negado
                if not literal.startswith('¬'):
                    clausula_horn.append(f"¬{literal}")
                else:
                    clausula_horn.append(literal)  # Mantener el literal ya negado

            # Agregar el último literal sin negación
            ultimo_literal = literales[-1].strip()
            if ultimo_literal.startswith('¬'):
                # Si el último literal está negado, lo quitamos
                clausula_horn.append(ultimo_literal[1:])  # Quitar la negación
            else:
                clausula_horn.append(ultimo_literal)

            # Unir la cláusula en una cadena
            clausulas_horn.append("∨".join(clausula_horn))

        # Guardar las cláusulas de Horn en un nuevo archivo
        with open("Clausulas_Horn.txt", 'w', encoding='utf-8') as archivo:
            for clausula in clausulas_horn:
                archivo.write(clausula + ".\n")
        print("Cláusulas de Horn guardadas en Clausulas_Horn.txt.")
    else:
        print("No hay reglas cargadas para convertir a cláusulas de Horn.")


def Menu():
    print("        MENU")
    print("=" * 60)
    print("1.  Introducir una fórmula")
    print("2.  Tabla de átomos")
    print("3.  Tabla de verdad")
    print("4.  Guardar regla")
    print("5.  Cargar regla")
    print("6.  Asignar valores de verdad")
    print("7.  Ver resultado")
    print("8.  Dibujar árbol binario")
    print("9.  Dibujar árbol binario global")
    print("10. Convertir las reglas a cláusulas de Horn")
    print("11. Salir")
    opcion = input("Elija una opción: ")
    return opcion

cont=0
while True:
    opcion = Menu()
    
    if opcion == "1":
        oracion = input("Ingresa la frase \n")
        formula, frase = Formula(oracion)
        formula = Unir(formula)
        cont += 1
        print('El resultado es: ', formula + '\n')
    elif opcion == "2":
        if cont > 0:
            Tabla_Atomos(formula, frase)
        else:
            print('Crea una fórmula antes')
    elif opcion == "3":
        if cont > 0:
            Tabla_Booleana(formula)
        else:
            print('Crea una fórmula antes')
    elif opcion == "4":
        if cont > 0:
            Guardar(formula)
        else:
            print('Crea una fórmula antes')
    elif opcion == "5":
        BD = Cargar()
        print('El resultado es: \n', BD)
    elif opcion == "6":
        if cont>0:
            valores_asignados= Asignar(formula)
        else:
            print('Crea una fórmula antes')
    elif opcion == "7":
        if valores_asignados:
            Ver(oracion, valores_asignados)
        else:
                print('Asigna valores primero.')
    elif opcion == "8":
        if cont > 0:
            Arbol_binario(oracion)
                
        else:print('Crea una fórmula antes')
        
    elif opcion == "9":
        Arbol_binario_global()
    elif opcion == "10":
        Horn()
    elif opcion == "11":
        print("Adios")
        break
    else:
        print("Opción inválida. Por favor, elija una opción válida.")