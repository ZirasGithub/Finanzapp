import re
from functools import reduce

"""Recuerden que tienen que hacer anotaciones docstring después de cada función, explicando qué hace cada una"""
"""Evitar usar funciones globales, todas las funciones deben recibir sus parámetros"""
#=======================================
#=========      FINANZAPP      =========
#=======================================

CATEGORIAS_AHORRO = ["Reserva de dinero", "Inversion"]


# ---------- MENÚS ----------

def mostrar_menu_usuario():
    """Muestra el menú principal de un usuario común y devuelve la opción elegida."""
    print("\n--- FINANZAPP ---")
    print("1 - Cargar movimiento")
    print("2 - Consultar movimientos")
    print("3 - Ver totales")
    print("4 - Depositar en ahorro")
    print("5 - Salir")
    opcion = input("Seleccione una opción: ")

    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 5:
        opcion = input("Opción inválida, seleccione un número entre 1 y 5: ")
    return int(opcion)


def mostrar_menu_admin():
    """Muestra el menú del superusuario y devuelve la opción elegida."""
    print("\n--- FINANZAPP (Superusuario) ---")
    print("1 - Ver movimientos de todos los usuarios")
    print("2 - Editar un movimiento de un usuario")
    print("3 - Salir")
    opcion = input("Seleccione una opción: ")

    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 3:
        opcion = input("Opción inválida, seleccione un número entre 1 y 3: ")
    return int(opcion)


# ---------- USUARIOS Y ACCESO ----------

def crear_usuario(usuarios):
    """Crea un usuario nuevo validando que el nombre no exista y que el password tenga más de 6 caracteres.
    Devuelve el nombre y el id del usuario creado."""
    print("Creando usuario...")
    nombres_existentes = {usuario[0] for usuario in usuarios}  # conjunto de nombres ya usados

    user = input("Ingrese el nombre: ")
    while user in nombres_existentes:
        print("El nombre ya existe, ingrese otro...")
        user = input("Ingrese el nombre: ")

    password = input("Ingrese el password (más de 6 caracteres): ")
    while not re.match(r"^.{7,}$", password):
        password = input("Password inválido, debe tener más de 6 caracteres: ")

    ids_existentes = [usuario[2] for usuario in usuarios]
    nuevo_id = max(ids_existentes) + 1
    usuarios.append((user, password, nuevo_id, "usuario"))
    print("Usuario creado con éxito.")
    return user, nuevo_id


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
    """Punto de entrada: permite iniciar sesión o crear un usuario hasta lograr acceso."""
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
    """Crea las estructuras de movimientos y ahorro de un usuario si todavía no existen."""
    if id_user not in movimientos_usuarios:
        movimientos_usuarios[id_user] = {"ingresos": [], "gastos": []}
    if id_user not in ahorros_usuarios:
        ahorros_usuarios[id_user] = 0.0


# ---------- CATEGORÍAS (MATRIZ) ----------
# La matriz tiene 2 filas (0 = gasto, 1 = ingreso) y en cada fila 2 columnas (0 = fijo, 1 = variable).
# Cada celda es una lista con los nombres de las categorías correspondientes.

def indice_tipo(tipo):
    """Devuelve el índice de fila de la matriz de categorías según el tipo de movimiento."""
    return 0 if tipo == "gasto" else 1


def indice_clase(clase):
    """Devuelve el índice de columna de la matriz de categorías según la clase del movimiento."""
    return 0 if clase == "fijo" else 1


def registrar_categoria_nueva(categorias_matriz, tipo, clase, categoria):
    """Agrega una categoría nueva en la celda correspondiente de la matriz de categorías."""
    categorias_matriz[indice_tipo(tipo)][indice_clase(clase)].append(categoria)


def seleccionar_categoria(categorias_matriz, tipo):
    """Permite elegir una categoría existente o crear una nueva, usando la matriz de categorías."""
    fila = categorias_matriz[indice_tipo(tipo)]
    categorias_fijas = fila[0]
    categorias_variables = fila[1]
    categorias = categorias_fijas + categorias_variables

    for i in range(len(categorias)):
        print(i + 1, "-", categorias[i])
    print(len(categorias) + 1, "- Crear nueva categoría")

    opcion = input("Seleccione una categoría: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(categorias) + 1:
        opcion = input("Opción inválida, ingrese un número: ")
    opcion = int(opcion)

    if opcion == len(categorias) + 1:
        categoria = input("Ingrese el nombre de la nueva categoría: ")
        while categoria in categorias:
            categoria = input("Esa categoría ya existe, ingrese otra: ")
        clase_movimiento = input("¿Fijo o variable? ").strip().lower()
        while clase_movimiento != "fijo" and clase_movimiento != "variable":
            clase_movimiento = input("Opción inválida, ingrese fijo o variable: ").strip().lower()
        registrar_categoria_nueva(categorias_matriz, tipo, clase_movimiento, categoria)
        return categoria, clase_movimiento

    categoria = categorias[opcion - 1]
    clase_movimiento = "fijo" if categoria in categorias_fijas else "variable"
    return categoria, clase_movimiento


# ---------- VALIDACIONES ----------

def validar_tipo():
    """Valida que el tipo de movimiento sea ingreso o gasto."""
    tipo = input("¿Quiere registrar un ingreso o un gasto? ").strip().lower()
    while tipo != "ingreso" and tipo != "gasto":
        tipo = input("Opción inválida. Elija 'ingreso' o 'gasto': ").strip().lower()
    return tipo


def validacion_de_monto():
    """Pide el monto y valida que sea un número mayor a cero (rechaza negativos, texto y el cero)."""
    monto_string = input("Monto: ")
    while not monto_string.replace(".", "", 1).isdigit() or float(monto_string) <= 0:
        monto_string = input("El monto es inválido (debe ser un número mayor a 0), reingrese: ")
    return float(monto_string)


def validacion_de_fecha():
    """Pide la fecha y controla que tenga un formato y valores válidos."""
    fecha = input("Fecha (dd/mm/aaaa): ")
    patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}$"
    while re.match(patron, fecha) is None:
        fecha = input("Fecha no válida, reingrese en formato dd/mm/aaaa: ")
    partes = fecha.split("/")
    dia = int(partes[0])
    mes = int(partes[1])

    while (mes == 2 and dia > 29) or (mes in [4, 6, 9, 11] and dia > 30):
        fecha = input("La fecha no existe, reingrese: ")
        while re.match(patron, fecha) is None:
            fecha = input("Fecha no válida, reingrese en formato dd/mm/aaaa: ")
        partes = fecha.split("/")
        dia = int(partes[0])
        mes = int(partes[1])
    return fecha


# ---------- REGISTRO DE MOVIMIENTOS ----------

def registro_movimientos(tipo, categorias_matriz):
    """Pide monto, fecha y categoría, y arma el movimiento como lista."""
    monto = validacion_de_monto()
    fecha = validacion_de_fecha()
    categoria, clase_movimiento = seleccionar_categoria(categorias_matriz, tipo)
    movimiento = [monto, fecha, categoria, clase_movimiento]
    return movimiento


def guardar_movimiento(movimientos_usuarios, id_user, tipo, movimiento):
    """Guarda el movimiento en la lista de ingresos o gastos del usuario logueado."""
    if tipo == "ingreso":
        movimientos_usuarios[id_user]["ingresos"].append(movimiento)
    else:
        movimientos_usuarios[id_user]["gastos"].append(movimiento)


def aplicar_categoria_ahorro(ahorros_usuarios, id_user, categoria, monto):
    """Si la categoría es de reserva/inversión, resta el monto del ahorro total del usuario.
    Devuelve False (y no registra el movimiento) si el usuario no tiene ahorro suficiente."""
    if categoria in CATEGORIAS_AHORRO:
        if monto > ahorros_usuarios[id_user]:
            print(f"No se puede registrar: el ahorro disponible es de ${ahorros_usuarios[id_user]}.")
            return False
        ahorros_usuarios[id_user] -= monto
    return True


def depositar_ahorro(ahorros_usuarios, id_user):
    """Agrega dinero al ahorro total del usuario."""
    monto = validacion_de_monto()
    ahorros_usuarios[id_user] += monto
    print(f"Depósito realizado. Ahorro total actual: ${ahorros_usuarios[id_user]}")


# ---------- CÁLCULOS Y CONSULTAS ----------

def calculo_movimientos(movimientos_usuario):
    """Calcula el total de ingresos y el total de gastos del usuario (sin balance acumulado,
    ya que corresponde a la entrega del 100%)."""
    montos_ingresos = map(lambda movimiento: movimiento[0], movimientos_usuario["ingresos"])
    montos_gastos = map(lambda movimiento: movimiento[0], movimientos_usuario["gastos"])
    total_ingresos = reduce(lambda x, y: x + y, montos_ingresos, 0)
    total_gastos = reduce(lambda x, y: x + y, montos_gastos, 0)
    return total_ingresos, total_gastos


def filtrar_por_clase(lista_movimientos, clase):
    """Devuelve solo los movimientos de la clase indicada ('fijo' o 'variable')."""
    return list(filter(lambda movimiento: movimiento[3] == clase, lista_movimientos))


def mostrar_movimientos(lista, titulo):
    """Muestra por consola una lista de movimientos con un título."""
    print(titulo)
    if len(lista) == 0:
        print("No hay movimientos cargados.")
    else:
        for movimiento in lista:
            print(
                "Monto:", movimiento[0],
                "- Fecha:", movimiento[1],
                "- Categoría:", movimiento[2],
                "- Clase:", movimiento[3]
            )


def consulta_de_movimientos(movimientos_usuario):
    """Muestra los ingresos y gastos del usuario, y la cantidad de gastos fijos vs variables."""
    mostrar_movimientos(movimientos_usuario["ingresos"], "INGRESOS")
    mostrar_movimientos(movimientos_usuario["gastos"], "GASTOS")

    gastos_fijos = filtrar_por_clase(movimientos_usuario["gastos"], "fijo")
    gastos_variables = filtrar_por_clase(movimientos_usuario["gastos"], "variable")
    print(f"\nGastos fijos: {len(gastos_fijos)} - Gastos variables: {len(gastos_variables)}")


# ---------- FUNCIONES DE SUPERUSUARIO ----------

def consulta_admin(movimientos_usuarios, usuarios):
    """Permite al superusuario ver los movimientos de todos los usuarios."""
    for nombre, password, id_u, rol in usuarios:
        if id_u in movimientos_usuarios:
            print(f"\n=== Usuario: {nombre} (ID {id_u}) ===")
            consulta_de_movimientos(movimientos_usuarios[id_u])


def editar_movimiento_admin(movimientos_usuarios):
    """Permite al superusuario editar el monto de un movimiento de cualquier usuario."""
    id_buscado = input("Ingrese el ID del usuario cuyo movimiento quiere editar: ")
    while not id_buscado.isdigit() or int(id_buscado) not in movimientos_usuarios:
        id_buscado = input("ID inválido, reingrese: ")
    id_buscado = int(id_buscado)

    tipo = validar_tipo()
    clave = "ingresos" if tipo == "ingreso" else "gastos"
    lista = movimientos_usuarios[id_buscado][clave]
    mostrar_movimientos(lista, clave.upper())

    if len(lista) == 0:
        return

    indice = input(f"Ingrese el número de movimiento a editar (1-{len(lista)}): ")
    while not indice.isdigit() or int(indice) < 1 or int(indice) > len(lista):
        indice = input("Índice inválido, reingrese: ")
    indice = int(indice) - 1

    nuevo_monto = validacion_de_monto()
    lista[indice][0] = nuevo_monto
    print("Movimiento actualizado con éxito.")


# ---------- MAIN ----------

usuarios = [
    ("lucia", "pedros", 1, "usuario"),
    ("jaz", "racyces", 2, "usuario"),
    ("blas", "macias", 3, "usuario"),
    ("lucas", "pezzano", 4, "usuario"),
    ("admin", "admin1234", 0, "admin"),
]

# Matriz de categorías: fila 0 = gasto, fila 1 = ingreso / columna 0 = fijo, columna 1 = variable
categorias_matriz = [
    [
        ["Alquiler", "Servicios", "Suscripciones", "Impuestos"],
        ["Supermercado", "Bares/Restaurantes", "Transporte", "Combustible", "Salud",
         "Educacion", "Ocio/Entretenimiento", "Regalos", "Otros gastos"] + CATEGORIAS_AHORRO
    ],
    [
        ["Sueldo"],
        ["Freelance", "Ventas", "Inversiones", "Reintegros", "Regalos", "Otros ingresos"]
    ]
]

movimientos_usuarios = {}   # id_user -> {"ingresos": [...], "gastos": [...]}
ahorros_usuarios = {}       # id_user -> monto ahorrado

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
    while opcion != 5:
        if opcion == 1:
            tipo = validar_tipo()
            nuevo_movimiento = registro_movimientos(tipo, categorias_matriz)
            categoria_elegida = nuevo_movimiento[2]
            monto_elegido = nuevo_movimiento[0]

            registrar_ok = True
            if tipo == "gasto" and categoria_elegida in CATEGORIAS_AHORRO:
                registrar_ok = aplicar_categoria_ahorro(ahorros_usuarios, id_user, categoria_elegida, monto_elegido)

            if registrar_ok:
                guardar_movimiento(movimientos_usuarios, id_user, tipo, nuevo_movimiento)
                print("Movimiento registrado con éxito.")

        elif opcion == 2:
            consulta_de_movimientos(movimientos_usuarios[id_user])

        elif opcion == 3:
            total_ingresos, total_gastos = calculo_movimientos(movimientos_usuarios[id_user])
            print("Total de ingresos:", total_ingresos)
            print("Total de gastos:", total_gastos)

        elif opcion == 4:
            depositar_ahorro(ahorros_usuarios, id_user)

        opcion = mostrar_menu_usuario()

print("Gracias por usar Finanzapp!")