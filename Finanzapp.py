"""Recuerden que tienen que hacer anotaciones docstring después de cada función, explicando qué hace cada una"""
"""Evitar usar funciones globales, todas las funciones deben recibir sus parámetros"""
#=======================================
#=========      FINANZAPP      =========       
#=======================================
def mostrar_menu():
    """Muestra el menu principal y devuelve la opcion elegida"""
    print("\n--- FINANZAPP ---")
    print("1 - Cargar movimiento")
    print("2 - Consultar movimientos")
    print("3 - Ver totales")
    print("4 - Salir")
    opcion = input("Seleccione una opción: ")

    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 4:
        opcion = input("Opción inválida, seleccione un numero entre 1 y 4 ")
    return int(opcion)


def registro_movimientos(tipo):
    """Registra los movimientos en listas, dependiendo el tipo"""
    monto = validacion_de_monto()
    fecha = validacion_de_fecha()
    categoria, clase_movimiento = seleccionar_categoria(tipo)
    movimiento = [monto, fecha, categoria, clase_movimiento]
    return movimiento


def validar_tipo():
    """Valida que el tipo de movimiento sea ingreso o gasto."""
    tipo = input("¿Quiere registrar un ingreso o un gasto? ").strip().lower()
    while tipo != "ingreso" and tipo != "gasto":
        tipo = input("Opción inválida. Elija 'ingreso' o 'gasto': ").strip().lower()
    return tipo


def guardar_movimientos(movimientos, tipo, lista_ingresos, lista_gastos):
    """Guarda los movimientos en lista_ingresos o lista_gastos"""
    if tipo == "ingreso":
        lista_ingresos.append(movimientos)
    else:
        lista_gastos.append(movimientos)


def registro_categoria_nueva(categoria, tipo, clase_movimiento):
    """Agrega una categoria nueva a la lista correspondiente"""
    if tipo == "gasto" and clase_movimiento == "fijo":
        categorias_gastos_fijos.append(categoria)
    elif tipo == "gasto" and clase_movimiento == "variable":
        categorias_gastos_variables.append(categoria)
    elif tipo == "ingreso" and clase_movimiento == "fijo":
        categorias_ingresos_fijos.append(categoria)
    else:
        categorias_ingresos_variables.append(categoria)


def seleccionar_categoria(tipo):
    """Permite elegir una categoría existente o crear una nueva."""
    if tipo == "gasto":
        categorias = categorias_gastos_fijos + categorias_gastos_variables
    else:
        categorias = categorias_ingresos_fijos + categorias_ingresos_variables

    for i in range(len(categorias)):
        print(i + 1, "-", categorias[i])

    print(len(categorias) + 1, "- Crear nueva categoria")

    opcion = input("Seleccione una categoria: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(categorias) + 1:
        opcion = input("Opcion invalida, ingrese un numero: ")
    opcion = int(opcion)

    if opcion == len(categorias) + 1:
        categoria = input("Ingrese el nombre de la nueva categoría: ")
        clase_movimiento = input("¿Fijo o variable? ").strip().lower()
        while clase_movimiento != "fijo" and clase_movimiento != "variable":
            clase_movimiento = input("Opción inválida, ingrese fijo o variable: ").strip().lower()
        registro_categoria_nueva(categoria, tipo, clase_movimiento)
        return categoria, clase_movimiento
    categoria = categorias[opcion - 1]

    if categoria in categorias_gastos_fijos or categoria in categorias_ingresos_fijos:
        clase_movimiento = "fijo"
    else:
        clase_movimiento = "variable"
    return categoria, clase_movimiento


def validacion_de_monto():
    """Pide el monto y controla si es correcto y no es un número negativo"""
    monto_string = input("Monto: ")
    while not monto_string.replace(".", "", 1).isdigit():
        monto_string = input("El monto es inválido, reingrese: ")
    return float(monto_string)


import re
def validacion_de_fecha():
    """Pide la fecha y controla que tenga un formato y valores válidos."""
    fecha = input("Fecha (dd/mm/aaaa): ")
    patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}$"
    while re.match(patron, fecha) == None:
        fecha = input("Fecha no valida, reingrese en formato dd/mm/aaaa: ")
    partes = fecha.split("/")
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])
    while (
        (mes == 2 and dia > 29)
        or (mes in [4, 6, 9, 11] and dia > 30)
    ):
        fecha = input("La fecha no existe, reingrese: ")
        while re.match(patron, fecha) == None:
            fecha = input("Fecha no valida, reingrese en formato dd/mm/aaaa: ")
        partes = fecha.split("/")
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
    return fecha


from functools import reduce
def sumar (x,y):
    return x+y

def calculo_movimientos(lista_ingresos, lista_gastos):
    """Calcula el total de los ingresos y de los gastos"""
    montos_ingresos = map(lambda movimiento : movimiento[0], lista_ingresos)
    montos_gastos = map(lambda movimiento: movimiento[0], lista_gastos)
    suma_ingresos = reduce(sumar, montos_ingresos, 0)
    suma_gastos = reduce(sumar, montos_gastos, 0)
    return suma_ingresos, suma_gastos
    

def consulta_de_movimientos(lista_ingresos, lista_gastos):
    """Muestra los ingresos y gastos registrados."""
    print("INGRESOS")
    if len(lista_ingresos) == 0:
        print("No hay ingresos cargados.")
    else:
        for movimiento in lista_ingresos:
            print(
                "Monto:", movimiento[0],
                "- Fecha:", movimiento[1],
                "- Categoría:", movimiento[2],
                "- Clase:", movimiento[3]
            )

    print("GASTOS")
    if len(lista_gastos) == 0:
        print("No hay gastos cargados.")
    else:
        for movimiento in lista_gastos:
            print(
                "Monto:", movimiento[0],
                "- Fecha:", movimiento[1],
                "- Categoría:", movimiento[2],
                "- Clase:", movimiento[3]
            )



"""Main"""

lista_ingresos = []
lista_gastos = []

categorias_gastos_fijos = ["Alquiler","Servicios","Suscripciones","Impuestos"]
categorias_gastos_variables = ["Supermercado","Bares/Restaurantes","Transporte","Combustible","Salud","Educacion","Ocio/Entretenimiento","Regalos","Otros gastos"]
categorias_ingresos_fijos = ["Sueldo"]
categorias_ingresos_variables = ["Freelance","Ventas","Inversiones","Reintegros","Regalos","Otros ingresos"]

print("Bienvenido a Finanzapp!")

opcion = mostrar_menu()
while opcion != 4:
    if opcion == 1:
        tipo = validar_tipo()
        nuevo_movimiento = registro_movimientos(tipo)
        guardar_movimientos(
            nuevo_movimiento,
            tipo,
            lista_ingresos,
            lista_gastos
        )
    elif opcion == 2:
        consulta_de_movimientos(
            lista_ingresos,
            lista_gastos
        )
    elif opcion == 3:
        total_ingresos, total_gastos = calculo_movimientos(
            lista_ingresos,
            lista_gastos
        )
        print("Total de ingresos:", total_ingresos)
        print("Total de gastos:", total_gastos)
    opcion = mostrar_menu()
print("Gracias por usar Finanzapp!")