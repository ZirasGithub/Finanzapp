

"""Recuerden que tienen que hacer anotaciones docstring después de cada función, explicando qué hace cada una"""
"""Evitar usar funciones globales, todas las funciones deben recibir sus parámetros"""
#=======================================
#=========      FINANZAPP      =========       
#=======================================

import re

TIPOS_INVERSION = ["Plazo fijo", "Fondo de inversion", "Acciones", "Cripto", "Otros"]

def mostrar_menu_usuario():
    """Muestra el menú principal de un usuario común y devuelve la opción elegida."""
    print("\n--- FINANZAPP ---")
    print("1 - Cargar movimiento")
    print("2 - Consultar movimientos")
    print("3 - Ver totales")
    print("4 - Ahorro / Inversion")
    print("5 - Ver ahorros e inversiones")
    print("6 - Salir")
    opcion = input("Seleccione una opción: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 6:
        opcion = input("Opción inválida, seleccione un número entre 1 y 6: ")
    return int(opcion)

def mostrar_submenu_ahorro():
    """Muestra el submenu de ahorro e inversion y devuelve la opcion elegida"""
    print("\n--- AHORRO / INVERSION ---")
    print("1 - Reservar dinero")
    print("2 - Invertir dinero")
    print("3 - Volver al menu principal")
    opcion = input("Seleccione una opción: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 3:
        opcion = input("Opción inválida, seleccione un numero entre 1 y 3: ")
    return int(opcion)


def mostrar_menu_admin():
    """Muestra el menú del superusuario y devuelve la opción elegida"""
    print("\n--- FINANZAPP (Superusuario) ---")
    print("1 - Ver movimientos de todos los usuarios")
    print("2 - Editar un movimiento de un usuario")
    print("3 - Salir")
    opcion = input("Seleccione una opción: ")
 
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 3:
        opcion = input("Opción inválida, seleccione un número entre 1 y 3: ")
    return int(opcion)


#creamos los usuarios con esta funcion, validando si los mismos ya existen o no en la lista "usuarios"
def crear_usuario(usuarios):
    """Crea un usuario nuevo validando que el nombre no exista y que el password tenga más de 6 caracteres.
    Devuelve el nombre y el id del usuario creado."""
    print("Creando usuario...")
    nombres_existentes = {usuario[0] for usuario in usuarios}

    user = input("Ingrese el nombre: ")
    while user in nombres_existentes:
        print("El nombre ya existe, ingrese otro...")
        user = input("Ingrese el nombre: ")

    while len(user) == 0:
        print("Debe ingresar un nombre valido...")
        user = input("Ingrese el nombre: ")

    password = input("Ingrese el password (más de 6 caracteres): ")
    while not re.match(r"^.{7,}$", password):
        password = input("Password inválido, debe tener más de 6 caracteres: ")

    ids_existentes = [usuario[2] for usuario in usuarios]
    nuevo_id = max(ids_existentes) + 1
    usuarios.append((user, password, nuevo_id, "usuario"))
    print("Usuario creado con éxito.")
    return user, nuevo_id

#realizamos inicio de sesion y validamos que exista (en caso de no existir, pasamos a crearlo)
def iniciar_sesion(usuarios):
    """Valida nombre y contraseña de un usuario existente. Si no existe, ofrece crear uno nuevo."""
    print("Iniciando sesión...")
    nombre = input("Ingrese el nombre: ")
    usuario_encontrado = False
    password_correcta = ""
    id_user = None

    for user, password, id_u, rol in usuarios:
        if nombre == user:
            usuario_encontrado = True
            password_correcta = password
            id_user = id_u

    if usuario_encontrado:
        password = input("Ingrese el password: ")
        while password != password_correcta:
            print("Error: El password no es correcto.")
            password = input("Ingrese el password: ")
        print("Acceso concedido! Bienvenido")
        return nombre, id_user
    else:
        print("Error: El nombre no existe, ¿desea crear un usuario?")
        var = input("s/n: ")
        if var == "s":
            return crear_usuario(usuarios)
        return None


def acceso(usuarios):
    """Punto de entrada: permite iniciar sesión o crear un usuario hasta lograr acceso"""
    resultado = None
    while resultado is None:
        opcion = input("1 - Iniciar sesión\n2 - Crear usuario\nSeleccione una opción: ")
        while opcion not in ("1", "2"):
            opcion = input("Opción inválida. 1 - Iniciar sesión / 2 - Crear usuario: ")
        resultado = iniciar_sesion(usuarios) if opcion == "1" else crear_usuario(usuarios)
    return resultado

def obtener_rol(usuarios, id_user):
    """Devuelve el rol ('usuario' o 'admin') correspondiente a un id de usuario."""
    for nombre, password, id_u, rol in usuarios:
        if id_u == id_user:
            return rol
    return "usuario"


def inicializar_datos_usuario(id_user, movimientos_usuarios, ahorros_usuarios):
    """Crea las estructuras de movimientos, reserva e inversion de un usuario si todavía no existen."""
    if id_user not in movimientos_usuarios:
        movimientos_usuarios[id_user] = {"ingresos": [], "gastos": []}
    if id_user not in ahorros_usuarios:
        inversiones_iniciales = {tipo: 0.0 for tipo in TIPOS_INVERSION}
        ahorros_usuarios[id_user] = {"reserva": 0.0, "inversion": inversiones_iniciales}


def registro_movimientos(tipo, categorias_gastos_fijos, categorias_gastos_variables, categorias_ingresos_fijos, categorias_ingresos_variables):
    """Registra los movimientos en listas, dependiendo el tipo"""
    monto = validacion_de_monto()
    fecha = validacion_de_fecha()
    categoria, clase_movimiento = seleccionar_categoria(tipo, categorias_gastos_fijos, categorias_gastos_variables, categorias_ingresos_fijos, categorias_ingresos_variables)
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


def registro_categoria_nueva(categoria, tipo, clase_movimiento, categorias_gastos_fijos, categorias_gastos_variables, categorias_ingresos_fijos, categorias_ingresos_variables):
    """Agrega una categoria nueva a la lista correspondiente"""
    if tipo == "gasto" and clase_movimiento == "fijo":
        categorias_gastos_fijos.append(categoria)
    elif tipo == "gasto" and clase_movimiento == "variable":
        categorias_gastos_variables.append(categoria)
    elif tipo == "ingreso" and clase_movimiento == "fijo":
        categorias_ingresos_fijos.append(categoria)
    else:
        categorias_ingresos_variables.append(categoria)


def seleccionar_categoria(tipo, categorias_gastos_fijos, categorias_gastos_variables, categorias_ingresos_fijos, categorias_ingresos_variables):
    """Permite elegir una categoría existente o crear una nueva."""
    if tipo == "gasto":
        categorias = categorias_gastos_fijos + categorias_gastos_variables
    else:
        categorias = categorias_ingresos_fijos + categorias_ingresos_variables

    for i in range(len(categorias)):
        print(i, "-", categorias[i])
    print(len(categorias), "- Crear nueva categoria")

    opcion = input("Seleccione una categoria: ")
    while not opcion.isdigit() or int(opcion) < 0 or int(opcion) > len(categorias):
        opcion = input("Opcion invalida, ingrese un numero: ")
    opcion = int(opcion)

    if opcion == len(categorias):
        categoria = input("Ingrese el nombre de la nueva categoría: ")
        clase_movimiento = input("¿Fijo o variable? ").strip().lower()
        while clase_movimiento != "fijo" and clase_movimiento != "variable":
            clase_movimiento = input("Opción inválida, ingrese fijo o variable: ").strip().lower()
        registro_categoria_nueva(categoria, tipo, clase_movimiento, categorias_gastos_fijos, categorias_gastos_variables, categorias_ingresos_fijos, categorias_ingresos_variables)
        return categoria, clase_movimiento

    categoria = categorias[opcion]
    if categoria in categorias_gastos_fijos or categoria in categorias_ingresos_fijos:
        clase_movimiento = "fijo"
    else:
        clase_movimiento = "variable"

    return categoria, clase_movimiento


def validacion_de_monto():
    """Pide el monto y controla si es correcto y no es un número negativo"""
    monto = input("Monto: ")
    while not monto.replace(",", "", 1).isdigit():
        monto = input("El monto es inválido, reingrese: ")
    return float(monto.replace(",", "."))


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
    while ((mes == 2 and dia > 29) or (mes in [4, 6, 9, 11] and dia > 30)):
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


def consulta_admin(movimientos_usuarios, usuarios):
    """Permite al superusuario ver los movimientos de todos los usuarios."""
    for nombre, password, id_u, rol in usuarios:
        if id_u in movimientos_usuarios:
            print(f"\n=== Usuario: {nombre} (ID {id_u}) ===")
            consulta_de_movimientos(
                movimientos_usuarios[id_u]["ingresos"],
                movimientos_usuarios[id_u]["gastos"]
            )


def editar_movimiento_admin(movimientos_usuarios):
    """Permite al superusuario editar el monto de un movimiento de cualquier usuario."""
    id_buscado = input("Ingrese el ID del usuario cuyo movimiento quiere editar: ")
    while not id_buscado.isdigit() or int(id_buscado) not in movimientos_usuarios:
        id_buscado = input("ID inválido, reingrese: ")
    id_buscado = int(id_buscado)

    tipo = validar_tipo()
    clave = "ingresos" if tipo == "ingreso" else "gastos"
    lista = movimientos_usuarios[id_buscado][clave]

    print(clave.upper())
    if len(lista) == 0:
        print("No hay movimientos cargados.")
        return
    for i in range(len(lista)):
        print(i + 1, "- Monto:", lista[i][0], "- Fecha:", lista[i][1], "- Categoría:", lista[i][2])

    indice = input(f"Ingrese el número de movimiento a editar (1-{len(lista)}): ")
    while not indice.isdigit() or int(indice) < 1 or int(indice) > len(lista):
        indice = input("Índice inválido, reingrese: ")
    indice = int(indice) - 1

    nuevo_monto = validacion_de_monto()
    lista[indice][0] = nuevo_monto
    print("Movimiento actualizado con éxito.")

# RESERVA E INVERSIÓN 

def seleccionar_tipo_inversion():
    """Muestra los tipos de inversión disponibles y devuelve el elegido."""
    for i in range(len(TIPOS_INVERSION)):
        print(i + 1, "-", TIPOS_INVERSION[i])
    opcion = input("Seleccione un tipo de inversión: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(TIPOS_INVERSION):
        opcion = input("Opción inválida, ingrese un número: ")
    return TIPOS_INVERSION[int(opcion) - 1]


def depositar_en_reserva(ahorros_usuarios, id_user):
    """Agrega dinero a la reserva del usuario."""
    monto = validacion_de_monto()
    ahorros_usuarios[id_user]["reserva"] += monto
    print(f"Reserva actualizada. Total reservado: ${ahorros_usuarios[id_user]['reserva']}")


def depositar_en_inversion(ahorros_usuarios, id_user):
    """Agrega dinero a un tipo de inversión elegido por el usuario."""
    tipo = seleccionar_tipo_inversion()
    monto = validacion_de_monto()
    ahorros_usuarios[id_user]["inversion"][tipo] += monto
    print(f"Inversión actualizada. Total en {tipo}: ${ahorros_usuarios[id_user]['inversion'][tipo]}")


def consulta_ahorro_inversion(ahorros_usuarios, id_user):
    """Muestra la reserva y las inversiones (por tipo) del usuario logueado."""
    datos = ahorros_usuarios[id_user]
    print("\nRESERVA")
    print("Total reservado:", datos["reserva"])

    print("\nINVERSIONES")
    hay_inversiones = False
    for tipo, monto in datos["inversion"].items():
        if monto > 0:
            hay_inversiones = True
            print(f"{tipo}: ${monto}")
    if not hay_inversiones:
        print("No hay inversiones cargadas.")

    total_invertido = sum(datos["inversion"].values())
    print(f"\nTotal invertido: ${total_invertido}")
    print(f"Total general (reserva + inversión): ${datos['reserva'] + total_invertido}")


"""Main"""

usuarios = [
    ("lucia", "pedros", 1, "usuario"),
    ("jaz", "racyces", 2, "usuario"),
    ("blas", "macias", 3, "usuario"),
    ("lucas", "pezzano", 4, "usuario"),
    ("admin", "admin1234", 0, "admin"),
]

categorias_gastos_fijos = ["Alquiler","Servicios","Suscripciones","Impuestos"]
categorias_gastos_variables = ["Supermercado","Bares/Restaurantes","Transporte","Combustible","Salud","Educacion","Ocio/Entretenimiento","Regalos","Otros gastos"]
categorias_ingresos_fijos = ["Sueldo"]
categorias_ingresos_variables = ["Freelance","Ventas","Inversiones","Reintegros","Regalos","Otros ingresos"]

movimientos_usuarios = {}   # id_user -> {"ingresos": [...], "gastos": [...]}
ahorros_usuarios = {}       # id_user -> {"reserva": monto, "inversion": {tipo: monto, ...}}

print("Bienvenido a Finanzapp!")

nombre, id_user = acceso(usuarios)
rol = obtener_rol(usuarios, id_user)
inicializar_datos_usuario(id_user, movimientos_usuarios, ahorros_usuarios)

if rol == "admin":
    opcion = mostrar_menu_admin()
    while opcion != 3:
        if opcion == 1:
            consulta_admin(movimientos_usuarios, usuarios)
        elif opcion == 2:
            editar_movimiento_admin(movimientos_usuarios)
        opcion = mostrar_menu_admin()

else:
    opcion = mostrar_menu_usuario()
    while opcion != 6:
        if opcion == 1:
            tipo = validar_tipo()
            nuevo_movimiento = registro_movimientos(tipo, categorias_gastos_fijos, categorias_gastos_variables, categorias_ingresos_fijos, categorias_ingresos_variables)
            guardar_movimientos(
                nuevo_movimiento,
                tipo,
                movimientos_usuarios[id_user]["ingresos"],
                movimientos_usuarios[id_user]["gastos"]
            )
        elif opcion == 2:
            consulta_de_movimientos(
                movimientos_usuarios[id_user]["ingresos"],
                movimientos_usuarios[id_user]["gastos"]
            )
        elif opcion == 3:
            total_ingresos, total_gastos, balance_acumulado = calculo_movimientos(
                movimientos_usuarios[id_user]["ingresos"],
                movimientos_usuarios[id_user]["gastos"]
            )
            print("Total de ingresos:", total_ingresos)
            print("Total de gastos:", total_gastos)
            print("Balance acumulado: ", balance_acumulado)
        elif opcion == 4:
            sub_opcion = mostrar_submenu_ahorro()
            while sub_opcion != 3:
                if sub_opcion == 1:
                    depositar_en_reserva(ahorros_usuarios, id_user)
                elif sub_opcion == 2:
                    depositar_en_inversion(ahorros_usuarios, id_user)
                sub_opcion = mostrar_submenu_ahorro()
        elif opcion == 5:
            consulta_ahorro_inversion(ahorros_usuarios, id_user)
        opcion = mostrar_menu_usuario()

print("Gracias por usar Finanzapp!")