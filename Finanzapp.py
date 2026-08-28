"""Recuerden que tienen que hacer anotaciones docstring después de cada función, explicando qué hace cada una"""
"""Evitar usar funciones globales, todas las funciones deben recibir sus parámetros"""
#=======================================
#=========      FINANZAPP      =========       
#=======================================

def registro_movimientos(tipo):
    """Registra los movimientos en listas, dependiendo el tipo"""
    monto = validacion_de_monto() #Hay que validar que no se coloquen montos negativos en validacion_de_monto()
    fecha = input("Fecha: ") #Hay que validar que la fecha que se elija sea válida en validacion_de_fecha()
    categoria = input("Categoria: ") 

    if categoria in categorias_gastos_fijos or categoria in categorias_ingresos_fijos:
        clase_movimiento = "fijo"
    elif categoria in categorias_gastos_variables or categoria in categorias_ingresos_variables:
        clase_movimiento = "variable"
    else:
        clase_movimiento = input("Categoría no reconocida. ¿Fijo o variable? ") #Hay que validar que pasa si el usuario coloca una categoría no reconocida. La categoria nueva se crea dentro de esta función? Si es así, se debe appendear a las listas de categorías en el main 
        registro_categoria_nueva(categoria, tipo, clase_movimiento)

    """Se crea una lista con los datos del movimiento y se devuelve hacia afuera, para que la función categorizacion_movimientos() la asigne al tipo de movimiento (a lista_ingresos o lista_gastos)"""

    movimiento = [monto, fecha, categoria, clase_movimiento]
    return movimiento

def validacion_de_monto():
    """Pide el monto y controla si el monto ingresado es correcto y no es un número negativo"""
    monto_string = input("Monto: ")
    while not monto_string.isdigit():
        monto_string = input("El monto es inválido. Reingrese: ")
        return float(monto_string)

def registro_categoria_nueva(categoria, tipo, clase_movimiento):
    """Agrega una categoría nueva a la lista correspondiente según el nombre de la categoría ingresada, el tipo y clase"""
    if tipo == "gasto" and clase_movimiento == "fijo":
        categorias_gastos_fijos.append(categoria)
    elif tipo == "gasto" and clase_movimiento == "variable":
        categorias_gastos_variables.append(categoria)
    elif tipo == "ingreso" and clase_movimiento == "fijo":
        categorias_ingresos_fijos.append(categoria)
    else:
        categorias_ingresos_variables.append(categoria)    

def sumar (x,y):
    return x+y

def calculo_movimientos():
    """Calcula matemáticamente los movimientos, ya sean ingresos o gastos - Usar reduce para este caso"""
    suma_total = map(sumar,lista_ingresos)
    suma_gastos = map(sumar,lista_gastos)
    dinero_total = suma_total - suma_gastos
    

def categorizacion_movimientos(movimientos, tipo):
    """Categoriza los movimientos en las listas lista_ingresos o lista_gastos"""
    if tipo == "ingreso": #Validar escritura del string ingresado por el usuario
        lista_ingresos.append(movimientos)
    else:
        lista_gastos.append(movimientos)

    
def consulta_de_movimientos():
    """Consulta los movimientos pertenecientes a un tiempo determinado"""
    pass

def validacion_de_fecha():
    """Controla que la fecha ingresada sea válida"""
    pass

"""Main"""

lista_ingresos = []
lista_gastos = []

categorias_gastos_fijos = ["Alquiler","Servicios","Suscripciones","Impuestos"]
categorias_gastos_variables = ["Supermercado","Bares/Restaurantes","Transporte","Combustible","Salud","Educacion","Ocio/Entretenimiento","Regalos","Otros gastos"]
categorias_ingresos_fijos = ["Sueldo"]
categorias_ingresos_variables = ["Freelance","Ventas","Inversiones","Reintegros","Regalos","Otros ingresos"]


tipo = input("¿Ingreso o gasto?")
nuevo_movimiento = registro_movimientos(tipo)
categorizacion_movimientos (nuevo_movimiento, tipo)
