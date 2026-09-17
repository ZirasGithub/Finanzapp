import re

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


#creamos los usuarios con esta funcion, validando si los mismos ya existen o no en la lista "usuarios"
def crear_usuario(usuarios):
    print("creando usuario...")
    nombres_existentes = [usuario[0] for usuario in usuarios]
    ultimo_id = usuarios[-1][2]
    user = input("Ingrese el nombre: ")

    while user in nombres_existentes:
        print("El nombre ya existe, ingrese otro...")
        user = input("Ingrese el nombre: ")

    password = input("Ingrese el password (más de 6 caracteres): ")
    while not re.match(r"^.{7,}$", password):
        password = input("Password inválido, debe tener más de 6 caracteres: ")
    nuevo_id = ultimo_id + 1
    usuarios.append((user, password, nuevo_id))
    print(f"Usuario creado con éxito.")
    return user,nuevo_id

#crear_usuario(usuarios)

#realizamos inicio de sesion y validamos que exista (en caso de no existir, pasamos a crearlo)
def iniciar_sesion(usuarios):
    print("iniciando sesion...")
    nombre = input("ingrese el nombre: ")
    usuario_encontrado = False
    password_correcta= ""
    id_user = None

    for user,password, id in usuarios:
        if nombre == user:
            usuario_encontrado = True
            password_correcta = password
            id_user = int(id)
    if usuario_encontrado == True:
        password = input("ingrese el password: ")
        while password != password_correcta:
            print("Error: El password no es correcto.")
            password = input("ingrese el password: ")
        print("Acceso concedido! Bienvenido")
        return nombre,id_user
    else:
        print("Error: El nombre no existe, desea crear un usuario?.")
        var = input("s/n: ")
        if var == "s":
            return crear_usuario(usuarios)
#iniciar_sesion(usuarios)

#Punto de entrada: permite iniciar sesión o crear un usuario hasta lograr acceso.
def acceso(usuarios):
    
    resultado = None
    while resultado is None:
        opcion = input("1 - Iniciar sesión\n2 - Crear usuario\nSeleccione una opción: ")
        while opcion not in ("1", "2"):
            opcion = input("Opción inválida. 1 - Iniciar sesión / 2 - Crear usuario: ")
        resultado = iniciar_sesion(usuarios) if opcion == "1" else crear_usuario(usuarios)
    return resultado

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
    """Calcula el total de los ingresos y de los gastos + el balance acumulado"""
    montos_ingresos = map(lambda movimiento : movimiento[0], lista_ingresos)
    montos_gastos = map(lambda movimiento: movimiento[0], lista_gastos)
    suma_ingresos = reduce(sumar, montos_ingresos, 0)
    suma_gastos = reduce(sumar, montos_gastos, 0)
    balance_acumulado = suma_ingresos - suma_gastos
    return suma_ingresos, suma_gastos, balance_acumulado
    

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
usuarios= [
    ("lucia","pedros",1),
    ("jaz","racyces",2),
    ("blas","macias",3),
    ("lucas","pezzano",4)
]

print("Bienvenido a Finanzapp!")

nombre, id_user = acceso(usuarios)

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
        total_ingresos, total_gastos, balance_acumulado = calculo_movimientos(
            lista_ingresos,
            lista_gastos
        )
        print("Total de ingresos:", total_ingresos)
        print("Total de gastos:", total_gastos)
        print("Balance acumulado: ",balance_acumulado)
    opcion = mostrar_menu()
print("Gracias por usar Finanzapp!")