"""
    Participantes:
                1. Valentino Grande
                2. Miqueas Girardi
                3. Felipe Figueroa Casas
                4. Francisco Gibbons
    Comision: 108
"""

import os
import random
import pickle
import pwinput


class CategoriaRegistro:
    def __init__(self):
        self.nro_categoria = 0
        self.nombre_categoria = ""
        self.pregunta = ""
        self.estado = ""


# Sirve para leer el id de la categoria previa, Principalmente para sumarle 1
#  al proximo id, en la insercion de nuevas categorias
def leer_numero_previo_categoria():
    numero = 0

    if os.path.getsize(CATEGORIAS_FISICO) > 0:
        categoria_logico.seek(0, 0)
        _ = pickle.load(categoria_logico)
        reg_size = categoria_logico.tell()

        categoria_logico.seek(-reg_size, 2)
        reg = pickle.load(categoria_logico)

        numero = int(reg.nro_categoria.strip())

    return numero


# Validamos el nombre de la categoria, su len y si ya existe.
def pedir_nombre_categoria():
    nombre = input("Ingrese el nombre de la categoria: ").strip()
    valido = False

    while not valido:
        if len(nombre) == 0 or len(nombre) > 30:
            print(f"{DARK_RED}El nombre debe tener entre 1 y 30 caracteres{RESET}")
            nombre = input("Ingrese el nombre de la categoria: ").strip()

        elif buscar_categoria(nombre) != -1:
            print(f"{DARK_RED}Ya existe una categoria con ese nombre{RESET}")
            nombre = input("Ingrese el nombre de la categoria: ").strip()

        else:
            valido = True

    return nombre


def categoria_input():

    reg = CategoriaRegistro()

    reg.nro_categoria = str(leer_numero_previo_categoria() + 1).ljust(4, " ")

    nombre = pedir_nombre_categoria()
    reg.nombre_categoria = nombre.ljust(30, " ")

    pregunta = input("Ingrese la pregunta: ").strip()
    while len(pregunta) == 0 or len(pregunta) > 200:
        print(f"{DARK_RED}La pregunta debe tener entre 1 y 200 caracteres{RESET}")
        pregunta = input("Ingrese la pregunta: ").strip()

    reg.pregunta = pregunta.ljust(200, " ")

    reg.estado = "A"

    return reg


class OpcionesRegistro:
    def __init__(self):
        self.nro_categoria = 0
        self.nro_opcion = 0
        self.objeto = ""
        self.valor = 0


# Similar a leer_numero_previo_categoria(), pero con opciones
def leer_numero_previo_opcion():
    numero = 0

    if os.path.getsize(OPCIONES_FISICO) > 0:
        opciones_logico.seek(0, 0)
        _ = pickle.load(opciones_logico)
        reg_size = opciones_logico.tell()

        opciones_logico.seek(-reg_size, 2)
        reg = pickle.load(opciones_logico)

        numero = int(reg.nro_opcion.strip())

    return numero


# Busqueda secuencial en categorias
def buscar_categoria(nombre):
    nro_categoria = -1
    tamanio = os.path.getsize(CATEGORIAS_FISICO)

    categoria_logico.seek(0, 0)

    while categoria_logico.tell() < tamanio and nro_categoria == -1:
        reg = pickle.load(categoria_logico)

        if reg.nombre_categoria.strip().lower() == nombre.lower():
            nro_categoria = int(reg.nro_categoria.strip())

    return nro_categoria


def opciones_input(nro_categoria):

    reg = OpcionesRegistro()

    reg.nro_opcion = str(leer_numero_previo_opcion() + 1).ljust(5, " ")
    reg.nro_categoria = nro_categoria

    objeto = input("Ingrese el nombre del objeto: ").strip()
    while len(objeto) == 0 or len(objeto) > 100:
        print(f"{DARK_RED}El objeto debe tener entre 1 y 100 caracteres{RESET}")
        objeto = input("Ingrese el nombre del objeto: ").strip()

    reg.objeto = objeto.ljust(100, " ")

    valor = input("Ingrese el valor: ").strip()
    while len(valor) > 10 or not valor.isdigit():
        print(f"{DARK_RED}Valor invalido, tiene que ser un numero de hasta 10 digitos{RESET}")
        valor = input("Ingrese el valor: ").strip()

    reg.valor = valor.ljust(10, " ")

    return reg


class JugadoresRegistro:
    def __init__(self):
        self.nombre = ""
        self.creditos = 10000.0
        # juegos[0] son las ganadas y juegos[1] las perdidas
        # cada columna es un juego, en el mismo orden que NOMBRES_JUEGOS
        self.juegos = [[0] * 4 for i in range(2)]


# Busqueda seq para el nombre del jugador
def buscar_nombre(nombre):
    posicion = -1
    tamanio = os.path.getsize(JUGADORES_FISICO)

    jugadores_logico.seek(0, 0)

    while jugadores_logico.tell() < tamanio and posicion == -1:
        inicio = jugadores_logico.tell()
        reg = pickle.load(jugadores_logico)

        if reg.nombre.strip() == nombre:
            posicion = inicio

    return posicion


# retorna el registro de un user segun su posicion
def leer_jugador(posicion):
    jugadores_logico.seek(posicion, 0)
    reg = pickle.load(jugadores_logico)

    return reg


# da de alta un jugador y retorna su posicion
def alta_jugador(nombre):
    reg = JugadoresRegistro()
    reg.nombre = nombre.ljust(30, " ")

    jugadores_logico.seek(0, 2)
    posicion = jugadores_logico.tell()
    pickle.dump(reg, jugadores_logico)
    jugadores_logico.flush()

    return posicion


# pregunta nombre, sino existe crea, si existe saluda
def pedir_jugador():
    nombre = input("Ingrese su nombre (2 a 30 caracteres): ").strip()

    while len(nombre) < 2 or len(nombre) > 30:
        print(f"{DARK_RED}El nombre debe tener entre 2 y 30 caracteres{RESET}")
        nombre = input("Ingrese su nombre (2 a 30 caracteres): ").strip()

    posicion = buscar_nombre(nombre)

    if posicion != -1:
        print(f"{YELLOW}Bienvenido de nuevo {nombre}{RESET}")

    else:
        posicion = alta_jugador(nombre)
        print(f"{YELLOW}Jugador {nombre} registrado con $10000{RESET}")

    return posicion


# pide la pocision del user para hacer el update + el juego + si gano o perdio
def registrar_resultado(posicion, juego, gano):
    reg = leer_jugador(posicion)

    if gano:
        reg.juegos[0][juego] += 1
    else:
        reg.juegos[1][juego] += 1

    jugadores_logico.seek(posicion, 0)
    pickle.dump(reg, jugadores_logico)
    jugadores_logico.flush()


TAMANIO_MAZO = 52
CONTRASENA = "admin123"  # contrasenia que deberia estar hasheada


# retorna el path donde se ejecuta el main.py
RUTA = os.path.dirname(os.path.abspath(__file__))

CATEGORIAS_FISICO = os.path.join(RUTA, "Categorias.dat")
OPCIONES_FISICO = os.path.join(RUTA, "Opciones.dat")
JUGADORES_FISICO = os.path.join(RUTA, "Jugadores.dat")

# estos dos files tiene q existir previamente
categoria_logico = open(CATEGORIAS_FISICO, "r+b")
opciones_logico = open(OPCIONES_FISICO, "r+b")

# contemplaos q no exista
if os.path.exists(JUGADORES_FISICO):
    jugadores_logico = open(JUGADORES_FISICO, "r+b")
else:
    jugadores_logico = open(JUGADORES_FISICO, "w+b")

NOMBRES_JUEGOS = ["Mayor o menor", "Numero secreto", "BlackJack", "Par o impar"]

numero_maximo_intentos_secreto = 5

RED = "\033[91m"
DARK_RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"
WHITE = "\033[97m"
YELLOW = "\033[93m"

texto = f"""
{RED}{BOLD}
+==============================================================+
|  ██╗    ██╗ █████╗ ██████╗ ███╗  ██╗██╗███╗  ██╗ ██████╗    |
|  ██║    ██║██╔══██╗██╔══██╗████╗ ██║██║████╗ ██║██╔════╝    |
|  ██║ █╗ ██║███████║██████╔╝██╔██╗██║██║██╔██╗██║██║  ███╗   |
|  ██║███╗██║██╔══██║██╔══██╗██║╚████║██║██║╚████║██║   ██║   |
|  ╚███╔███╔╝██║  ██║██║  ██║██║ ╚███║██║██║ ╚███║╚██████╔╝   |
|   ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚══╝╚═╝╚═╝  ╚══╝ ╚═════╝    |
+==============================================================+
{RESET}

{DARK_RED}{BOLD}
+==============================================================+
|   ⚠   LOS JUEGOS DE APUESTA ESTAN PROHIBIDOS               |
|        PARA LOS MENORES DE EDAD   ⚠                         |
+--------------------------------------------------------------+
|        ⚠   PERJUDICIAL PARA LA SALUD   ⚠                    |
+--------------------------------------------------------------+
|  [!] Genera adiccion y dependencia psicologica              |
|  [!] Provoca perdidas economicas graves                     |
|  [!] Destruye vinculos familiares y sociales                |
|  [!] Causa ansiedad, depresion y estres cronico             |
|  [!] Riesgo de endeudamiento y ruina financiera             |
+==============================================================+
{RESET}

{WHITE}{BOLD}
>>> LINEA 800 - JUEGO RESPONSABLE <<<
{RESET}
"""

TITULO_MAYOR_MENOR = r"""
 __  __   ___   _____  ___   __  __ ___ _  _  ___  ___
|  \/  | /_\ \ / / _ \| _ \ |  \/  | __| \| |/ _ \| _ \
| |\/| |/ _ \ V / (_) |   / | |\/| | _|| .` | (_) |   /
|_|  |_/_/ \_\_| \___/|_|_\ |_|  |_|___|_|\_|\___/|_|_\
"""

TITULO_NUMERO_SECRETO = r"""
 _  _ _   _ __  __ ___ ___  ___    ___ ___ ___ ___ ___ _____ ___
| \| | | | |  \/  | __| _ \/ _ \  / __| __/ __| _ \ __|_   _/ _ \
| .` | |_| | |\/| | _||   / (_) | \__ \ _| (__|   / _|  | || (_) |
|_|\_|\___/|_|  |_|___|_|_\\___/  |___/___\___|_|_\___| |_| \___/
"""

TITULO_BLACKJACK = r"""
 ___ _      _   ___ _  __  _  _   ___ _  __
| _ ) |    /_\ / __| |/ / | |/_\ / __| |/ /
| _ \ |__ / _ \ (__| ' < || / _ \ (__| ' <
|___/____/_/ \_\___|_|\_\__/_/ \_\___|_|\_\
"""

TITULO_PAR_IMPAR = r"""
 ___  _   ___    ___    ___ __  __ ___  _   ___
| _ \/_\ | _ \  / _ \  |_ _|  \/  | _ \/_\ | _ \
|  _/ _ \|   / | (_) |  | || |\/| |  _/ _ \|   /
|_|/_/ \_\_|_\  \___/  |___|_|  |_|_|/_/ \_\_|_\
"""


# hace el clear segun el OS
def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print(f"{DARK_RED}No se puede limpiar la pantalla{RESET}")


# cuenta la cant de opcs por categoria
def contar_opciones(nro_categoria):
    cantidad = 0
    tamanio = os.path.getsize(OPCIONES_FISICO)

    opciones_logico.seek(0, 0)

    while opciones_logico.tell() < tamanio:
        reg = pickle.load(opciones_logico)

        if int(reg.nro_categoria.strip()) == nro_categoria:
            cantidad += 1

    return cantidad


# la categoria es jugable si y solo si hay mas de 6 opcs
def categoria_jugable(nro_categoria, estado):
    jugable = False

    if estado == "A":
        jugable = contar_opciones(int(nro_categoria)) >= 6

    return jugable


# devuelve la cantidad de categorias con mas de 6 opciones y en estado A,
# el parametro mostar siginifa si se van a imprimir o no
def recorrer_categorias_jugables(mostrar):
    cantidad = 0
    tamanio = os.path.getsize(CATEGORIAS_FISICO)
    categoria_logico.seek(0, 0)

    while categoria_logico.tell() < tamanio:
        reg = pickle.load(categoria_logico)

        nro_categoria = reg.nro_categoria.strip()
        nombre = reg.nombre_categoria.strip()
        estado = reg.estado

        if categoria_jugable(nro_categoria, estado):
            if mostrar:
                print(f"{YELLOW}{nro_categoria.strip()}{RESET} - {nombre}")
            cantidad += 1

    return cantidad


# otra busqyeda secuencial por nro_categoria
def buscar_categoria_por_numero(nro_categoria):
    encontrada = -1
    tamanio = os.path.getsize(CATEGORIAS_FISICO)

    categoria_logico.seek(0, 0)

    while categoria_logico.tell() < tamanio and encontrada == -1:
        inicio = categoria_logico.tell()
        reg = pickle.load(categoria_logico)

        if int(reg.nro_categoria.strip()) == nro_categoria:
            encontrada = inicio

    return encontrada


# se busca un registro de una categoria valida,  > 6 opcs y estado = A
def pedir_categoria():
    reg = CategoriaRegistro()
    valida = False

    while not valida:
        try:
            nro_categoria = int(input("Elegi el numero de categoria: "))
            posicion = buscar_categoria_por_numero(nro_categoria)

            if posicion == -1:
                print(f"{DARK_RED}No existe una categoria con ese numero{RESET}")

            else:
                categoria_logico.seek(posicion, 0)
                reg = pickle.load(categoria_logico)

                if categoria_jugable(reg.nro_categoria.strip(), reg.estado):
                    valida = True
                else:
                    print(f"{DARK_RED}Esa categoria no se puede jugar{RESET}")

        except ValueError:
            print(f"{DARK_RED}Ingrese un entero valido{RESET}")

    return reg


# pone en objetos y valores los de la categoria actual
def cargar_opciones(nro_categoria, objetos, valores):
    idx = 0
    tamanio = os.path.getsize(OPCIONES_FISICO)

    opciones_logico.seek(0, 0)

    while opciones_logico.tell() < tamanio:
        reg = pickle.load(opciones_logico)

        if int(reg.nro_categoria.strip()) == nro_categoria:
            objetos[idx] = reg.objeto.strip()
            valores[idx] = int(reg.valor.strip())
            idx += 1


def elegir_opcion(usadas, cantidad, actual):
    disponibles = 0
    i = 0

    while i < cantidad:
        if not usadas[i]:
            disponibles += 1
        i += 1

    # si ya salieron todas las volvemos a habilitar, menos la actual
    if disponibles == 0:
        i = 0

        while i < cantidad:
            if i == actual:
                usadas[i] = True
            else:
                usadas[i] = False
            i += 1

    elegida = random.randint(0, cantidad - 1)

    # usamos nros randoms hasta q toque uno que este en usadas[random] = true
    while usadas[elegida]:
        elegida = random.randint(0, cantidad - 1)

    usadas[elegida] = True

    return elegida


# la base del mayor/menor
def jugar_rondas_mayor_menor(categoria):
    nro_categoria = int(categoria.nro_categoria.strip())
    cantidad = contar_opciones(nro_categoria)

    objetos = [""] * cantidad
    valores = [0] * cantidad
    usadas = [False] * cantidad

    cargar_opciones(nro_categoria, objetos, valores)

    aciertos = 0
    actual = elegir_opcion(usadas, cantidad, -1)
    ronda = 1

    while ronda <= 6:
        nueva = elegir_opcion(usadas, cantidad, actual)

        print(f"\n{RED}{BOLD}Ronda {ronda} de 6{RESET}")
        print(f"{BOLD}{categoria.pregunta.strip()}{RESET}")
        print(f"{YELLOW}1.{RESET} {objetos[actual]} / {YELLOW}2.{RESET} {objetos[nueva]}")

        respuesta = input("Elegi 1 o 2: ")

        while respuesta != "1" and respuesta != "2":
            print(f"{DARK_RED}Opcion invalida{RESET}")
            respuesta = input("Elegi 1 o 2: ")

        if valores[actual] >= valores[nueva]:
            correcta = actual
        else:
            correcta = nueva

        if respuesta == "1":
            elegida = actual
        else:
            elegida = nueva

        print(f"{objetos[actual]} {YELLOW}{valores[actual]}{RESET} / {objetos[nueva]} {YELLOW}{valores[nueva]}{RESET}")

        if valores[elegida] == valores[correcta]:
            print(f"{YELLOW}Correcto! Sumas 1 punto{RESET}")
            aciertos += 1
        else:
            print(f"{DARK_RED}Incorrecto{RESET}")

        print(f"Aciertos: {aciertos}")
        input("Presione enter para continuar...")

        actual = correcta
        ronda += 1

    return aciertos


def mayor_menor():
    clear()
    print(f"{RED}{BOLD}{TITULO_MAYOR_MENOR}{RESET}")

    posicion = pedir_jugador()
    reg = leer_jugador(posicion)
    nombre = reg.nombre.strip()

    if reg.creditos <= 0:
        print(f"{DARK_RED}{nombre} no tenes mas credito{RESET}")

    else:
        if recorrer_categorias_jugables(False) == 0:
            print(f"{DARK_RED}No hay categorias activas con al menos 6 opciones{RESET}")

        else:
            print(f"Tu credito es de: {YELLOW}${reg.creditos}{RESET}")
            apuesta = validar_apuesta(reg.creditos)

            print(f"\n{RED}{BOLD}Categorias:{RESET}")
            recorrer_categorias_jugables(True)

            categoria = pedir_categoria()
            aciertos = jugar_rondas_mayor_menor(categoria)

            print(f"\nTerminaste con {aciertos} aciertos de 6")

            if aciertos >= 4:
                print(f"{YELLOW}{nombre} ganaste ${apuesta}{RESET}")
                reg.creditos += apuesta
                reg.juegos[0][0] += 1

            else:
                print(f"{DARK_RED}{nombre} perdiste ${apuesta}{RESET}")
                reg.creditos -= apuesta
                reg.juegos[1][0] += 1

            jugadores_logico.seek(posicion, 0)
            pickle.dump(reg, jugadores_logico)
            jugadores_logico.flush()

            print(f"Tu credito ahora es: {YELLOW}${reg.creditos}{RESET}")

    input("Presione enter para continuar...")


def numero_secreto():
    clear()
    print(f"{RED}{BOLD}{TITULO_NUMERO_SECRETO}{RESET}")

    posicion = pedir_jugador()

    secreto =random.randint(1, 100)

    numero_intento = 0
    gano = False

    while numero_intento < numero_maximo_intentos_secreto and not gano:

        print(f"Intentos restantes: {numero_maximo_intentos_secreto - numero_intento}")

        valido = False
        intento = 0

        while not valido:
            try:
                intento = int(input("Ingrese un numero entre 1 y 100: "))

                if intento < 1 or intento > 100:
                    print(f"{DARK_RED}El numero debe estar entre 1 y 100{RESET}")

                else:
                    valido = True

            except ValueError:
                print(f"{DARK_RED}Ingrese un entero valido{RESET}")

        numero_intento += 1

        if intento == secreto:
            gano = True

        else:
            if intento < secreto:
                print(f"El numero secreto es {YELLOW}mayor{RESET}")

            else:
                print(f"El numero secreto es {YELLOW}menor{RESET}")

    if gano:
        print(f"{YELLOW}Ganaste! Te llevo {numero_intento} intentos{RESET}")

    else:
        print(f"{DARK_RED}Perdiste{RESET}")
        print(f"El numero era: {secreto}")

    registrar_resultado(posicion, 1, gano)

    input("Presione enter para continuar...")


def armar_mazo(mazo):
    palos = ["corazones", "diamantes", "picas", "treboles"]
    numeros = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    idx = 0

    for i in range(len(palos)):
        for j in range(len(numeros)):
            mazo[idx] = numeros[j] + " de " + palos[i]
            idx += 1


def sacar_carta(mazo):
    indice_carta = random.randint(0, TAMANIO_MAZO - 1)

    while mazo[indice_carta] == "":
        indice_carta = random.randint(0, TAMANIO_MAZO - 1)

    carta = mazo[indice_carta]
    mazo[indice_carta] = ""

    return carta


def obtener_numero_carta(carta):
    numero = ""
    i = 0

    while carta[i] != " ":
        numero += carta[i]
        i += 1

    return numero


def sumar_puntos(cartas, cantidad):
    total = 0
    hay_as = False
    i = 0

    while i < cantidad:
        numero = obtener_numero_carta(cartas[i])

        if numero == "J" or numero == "Q" or numero == "K":
            total += 10

        elif numero == "A":
            total += 1
            hay_as = True

        else:
            total += int(numero)

        i += 1

    if hay_as and total + 10 <= 21:
        total += 10

    return total


def blackjack():
    clear()
    print(f"{RED}{BOLD}{TITULO_BLACKJACK}{RESET}")

    posicion = pedir_jugador()
    reg = leer_jugador(posicion)
    nombre = reg.nombre.strip()

    if reg.creditos <= 0:
        print(f"{DARK_RED}{nombre} no tenes mas credito{RESET}")
        jugar_otra = False
    else:
        jugar_otra = True

    while jugar_otra:
        print(f"\nTu credito es de: {YELLOW}${reg.creditos}{RESET}")
        apuesta = validar_apuesta(reg.creditos)

        mazo = [""] * TAMANIO_MAZO
        armar_mazo(mazo)

        cartas_jugador = [""] * TAMANIO_MAZO
        cartas_banca = [""] * TAMANIO_MAZO

        cantidad_cartas_jugador = 0
        cantidad_cartas_banca = 0

        cartas_jugador[cantidad_cartas_jugador] = sacar_carta(mazo)
        cantidad_cartas_jugador += 1

        cartas_banca[cantidad_cartas_banca] = sacar_carta(mazo)
        cantidad_cartas_banca += 1

        cartas_jugador[cantidad_cartas_jugador] = sacar_carta(mazo)
        cantidad_cartas_jugador += 1

        cartas_banca[cantidad_cartas_banca] = sacar_carta(mazo)
        cantidad_cartas_banca += 1

        puntos_jugador = sumar_puntos(cartas_jugador, cantidad_cartas_jugador)
        puntos_banca = sumar_puntos(cartas_banca, cantidad_cartas_banca)

        print(f"\nCarta visible de la banca: {cartas_banca[0]}")
        print(f"Tus cartas: {cartas_jugador[0]} y {cartas_jugador[1]}")
        print(f"Tus puntos: {puntos_jugador}")

        se_paso = False
        if puntos_jugador < 21:
            turno_jugador = True
        else:
            turno_jugador = False

        while turno_jugador:

            opcion = input("Queres pedir o plantarte? (pedir/plantarse): ").lower()

            while opcion != "pedir" and opcion != "plantarse":
                opcion = input("Ingrese pedir o plantarse: ").lower()

            if opcion == "pedir":
                carta = sacar_carta(mazo)

                cartas_jugador[cantidad_cartas_jugador] = carta
                cantidad_cartas_jugador += 1

                puntos_jugador = sumar_puntos(cartas_jugador, cantidad_cartas_jugador)

                print(f"Sacaste: {carta}")
                print(f"Tus puntos: {puntos_jugador}")

                if puntos_jugador > 21:
                    se_paso = True
                    turno_jugador = False

                elif puntos_jugador == 21:
                    turno_jugador = False

            else:
                turno_jugador = False

        if se_paso:
            print(f"{DARK_RED}Te pasaste de 21. Gana la banca{RESET}")
            resultado = "perdio"

        else:

            print(f"La banca da vuelta su carta: {cartas_banca[1]}")

            while puntos_banca <= 16:
                carta = sacar_carta(mazo)

                cartas_banca[cantidad_cartas_banca] = carta
                cantidad_cartas_banca += 1

                puntos_banca = sumar_puntos(cartas_banca, cantidad_cartas_banca)
                print(f"La banca saco: {carta}")

            print(f"Puntos de la banca: {puntos_banca}")
            print(f"Tus puntos: {puntos_jugador}")

            if puntos_banca > 21:
                print(f"{YELLOW}La banca se paso de 21. Ganaste {nombre}{RESET}")
                resultado = "gano"

            elif puntos_jugador > puntos_banca:
                print(f"{YELLOW}Ganaste {nombre}{RESET}")
                resultado = "gano"

            elif puntos_banca > puntos_jugador:
                print(f"{DARK_RED}Gana la banca{RESET}")
                resultado = "perdio"

            else:
                print(f"{YELLOW}Empate, no ganas ni perdes nada{RESET}")
                resultado = "empate"

        if resultado == "gano":
            reg.creditos += apuesta
            reg.juegos[0][2] += 1
            print(f"{YELLOW}Ganaste ${apuesta}{RESET}")

        elif resultado == "perdio":
            reg.creditos -= apuesta
            reg.juegos[1][2] += 1
            print(f"{DARK_RED}Perdiste ${apuesta}{RESET}")

        jugadores_logico.seek(posicion, 0)
        pickle.dump(reg, jugadores_logico)
        jugadores_logico.flush()

        print(f"Tu credito ahora es: {YELLOW}${reg.creditos}{RESET}")

        if reg.creditos <= 0:
            print(f"{DARK_RED}{nombre} no tenes mas credito{RESET}")
            jugar_otra = False

        else:
            respuesta = input("Queres jugar otra partida? (si/no): ").lower()

            while respuesta != "si" and respuesta != "no":
                respuesta = input("Ingrese si o no: ").lower()

            if respuesta == "no":
                jugar_otra = False

    input("Presione enter para continuar...")


def validar_apuesta(credito):
    apuesta_valida = False
    apuesta = 0

    while not apuesta_valida:

        try:

            apuesta = int(input("Cuanto queres apostar?: "))

            if apuesta < 1:
                print(f"{DARK_RED}La apuesta debe ser mayor a 0{RESET}")

            elif apuesta > credito:
                print(f"{DARK_RED}No te alcanza el credito{RESET}")

            else:
                apuesta_valida = True

        except ValueError:
            print(f"{DARK_RED}Ingrese un entero valido{RESET}")

    return apuesta


def par_impar():
    clear()
    print(f"{RED}{BOLD}{TITULO_PAR_IMPAR}{RESET}")

    posicion = pedir_jugador()
    reg = leer_jugador(posicion)
    nombre = reg.nombre.strip()

    if reg.creditos <= 0:
        print(f"{DARK_RED}{nombre} no tenes mas credito{RESET}")

    else:

        print(f"Tu credito es de: {YELLOW}${reg.creditos}{RESET}")

        apuesta = validar_apuesta(reg.creditos)

        numero1 = random.randint(1, 6)
        numero2 = random.randint(1, 6)

        opcion = input("Par o impar?: ").lower()

        while opcion != "par" and opcion != "impar":
            opcion = input("Ingrese par o impar: ").lower()

        suma = numero1 + numero2

        print(f"Los numeros fueron: {numero1} y {numero2}")
        print(f"La suma es: {suma}")

        if suma % 2 == 0:
            resultado = "par"
        else:
            resultado = "impar"

        if opcion == resultado:
            gano = True
        else:
            gano = False

        if gano:
            print(f"{YELLOW}{nombre} ganaste{RESET}")
            reg.creditos += apuesta
            reg.juegos[0][3] += 1

        else:
            print(f"{DARK_RED}{nombre} perdiste{RESET}")
            reg.creditos -= apuesta
            reg.juegos[1][3] += 1

        jugadores_logico.seek(posicion, 0)
        pickle.dump(reg, jugadores_logico)
        jugadores_logico.flush()

        print(f"Tu credito ahora es: {YELLOW}${reg.creditos}{RESET}")

    input("Presione enter para continuar...")


# ordena el archivo de jugadores de mayor a menor credito y lo muestra
def ordenar_y_mostrar():
    jugadores_logico.seek(0, 0)
    auxi = pickle.load(jugadores_logico)
    tam_reg = jugadores_logico.tell()
    tam_arch = os.path.getsize(JUGADORES_FISICO)
    cant_reg = int(tam_arch / tam_reg)

    for i in range(0, cant_reg - 1):
        for j in range(i + 1, cant_reg):
            jugadores_logico.seek(i * tam_reg, 0)
            auxi = pickle.load(jugadores_logico)
            jugadores_logico.seek(j * tam_reg, 0)
            auxj = pickle.load(jugadores_logico)

            if auxi.creditos < auxj.creditos:
                jugadores_logico.seek(i * tam_reg, 0)
                pickle.dump(auxj, jugadores_logico)
                jugadores_logico.seek(j * tam_reg, 0)
                pickle.dump(auxi, jugadores_logico)
                jugadores_logico.flush()

    jugadores_logico.seek(0, 0)

    for i in range(cant_reg):
        reg = pickle.load(jugadores_logico)
        print(f"{YELLOW}{i + 1}.{RESET} {reg.nombre.strip()}: {YELLOW}${reg.creditos}{RESET}")


def reporte_creditos():
    if os.path.getsize(JUGADORES_FISICO) == 0:
        print(f"{DARK_RED}No hay jugadores{RESET}")

    else:
        print(f"\n{RED}{BOLD}[*] Jugadores ordenados por credito{RESET}")
        ordenar_y_mostrar()


def reporte_jugador():
    nombre = input("Ingrese el nombre del jugador: ").strip()

    posicion = buscar_nombre(nombre)

    if posicion == -1:
        print(f"{DARK_RED}Ese jugador no existe{RESET}")

    else:
        reg = leer_jugador(posicion)

        print(f"\n{RED}{BOLD}Juegos jugados por {nombre}{RESET}")

        for juego in range(4):
            ganadas = reg.juegos[0][juego]
            perdidas = reg.juegos[1][juego]

            if ganadas + perdidas > 0:
                print(f"\n{RED}{BOLD}[*] {NOMBRES_JUEGOS[juego]}{RESET}")
                print(f"Ganadas: {ganadas}")
                print(f"Perdidas: {perdidas}")

            juego += 1

        print(f"\nCreditos: {YELLOW}${reg.creditos}{RESET}")


def reporte():

    opcion = ""

    while opcion != "c":

        clear()

        print(f"""
    {RED}{BOLD}===== REPORTE ====={RESET}

    {RED}[*]{RESET} {YELLOW}A.{RESET} Jugadores ordenados por credito
    {RED}[*]{RESET} {YELLOW}B.{RESET} Juegos jugados por un jugador
    {RED}[*]{RESET} {YELLOW}C.{RESET} Volver al menu principal
    """)

        opcion = input("Ingrese una opcion: ").lower()

        while opcion not in ("a", "b", "c"):
            print(f"{DARK_RED}Opcion invalida{RESET}")
            opcion = input("Ingrese una opcion: ").lower()

        if opcion == "a":
            reporte_creditos()
            print()
            input("Presione enter para continuar...")

        elif opcion == "b":
            reporte_jugador()
            print()
            input("Presione enter para continuar...")


def pedir_contrasena():
    intentos = 0
    correcta = False

    while intentos < 3 and not correcta:
        contrasena = pwinput.pwinput("Ingrese la contrasena: ", mask="*")
        intentos += 1

        if contrasena == CONTRASENA:
            correcta = True
        else:
            print(f"{DARK_RED}Contrasena incorrecta. Intentos restantes: {3 - intentos}{RESET}")

    return correcta


def listar_categorias(solo_activas):
    cantidad = 0
    tamanio = os.path.getsize(CATEGORIAS_FISICO)

    categoria_logico.seek(0, 0)

    while categoria_logico.tell() < tamanio:
        reg = pickle.load(categoria_logico)

        if not solo_activas or reg.estado == "A":
            print(f"    {YELLOW}{reg.nro_categoria.strip()}{RESET} - {reg.nombre_categoria.strip()}")
            cantidad += 1

    return cantidad


def pedir_posicion_categoria(solo_activas):
    posicion = -1

    while posicion == -1:
        try:

            nro_categoria = int(input("Ingrese el numero de categoria: "))
            posicion = buscar_categoria_por_numero(nro_categoria)

            if posicion == -1:
                print(f"{DARK_RED}No existe una categoria con ese numero{RESET}")

            elif solo_activas:
                categoria_logico.seek(posicion, 0)
                reg = pickle.load(categoria_logico)

                if reg.estado != "A":
                    print(f"{DARK_RED}Esa categoria no esta activa{RESET}")
                    posicion = -1

        except ValueError:
            print(f"{DARK_RED}Ingrese un entero valido{RESET}")

    return posicion


def alta_categoria():
    reg = categoria_input()

    categoria_logico.seek(0, 2)
    pickle.dump(reg, categoria_logico)
    categoria_logico.flush()

    print(f"{YELLOW}Categoria {reg.nro_categoria.strip()} - {reg.nombre_categoria.strip()} dada de alta{RESET}")


def modificar_categoria():
    print(f"{RED}{BOLD}Categorias activas:{RESET}")

    if listar_categorias(True) == 0:
        print(f"{DARK_RED}No hay categorias activas{RESET}")

    else:
        posicion = pedir_posicion_categoria(True)

        categoria_logico.seek(posicion, 0)
        reg = pickle.load(categoria_logico)

        print(f"Nombre actual: {reg.nombre_categoria.strip()}")
        nombre = pedir_nombre_categoria()
        reg.nombre_categoria = nombre.ljust(30, " ")

        categoria_logico.seek(posicion, 0)
        pickle.dump(reg, categoria_logico)
        categoria_logico.flush()

        print(f"{YELLOW}Categoria {reg.nro_categoria.strip()} modificada{RESET}")


def baja_categoria():
    print(f"{RED}{BOLD}Categorias activas:{RESET}")

    if listar_categorias(True) == 0:
        print(f"{DARK_RED}No hay categorias activas{RESET}")

    else:

        posicion = pedir_posicion_categoria(True)

        categoria_logico.seek(posicion, 0)
        reg = pickle.load(categoria_logico)
        reg.estado = "I"

        categoria_logico.seek(posicion, 0)
        pickle.dump(reg, categoria_logico)
        categoria_logico.flush()

        print(f"{YELLOW}Categoria {reg.nro_categoria.strip()} - {reg.nombre_categoria.strip()} dada de baja{RESET}")


def alta_opcion():
    print(f"{RED}{BOLD}Categorias activas:{RESET}")

    if listar_categorias(True) == 0:
        print(f"{DARK_RED}Antes de registrar opciones se deben dar de alta categorias{RESET}")

    else:

        posicion = pedir_posicion_categoria(True)

        categoria_logico.seek(posicion, 0)
        categoria = pickle.load(categoria_logico)

        print(f"Pregunta: {BOLD}{categoria.pregunta.strip()}{RESET}")

        otra = "s"

        while otra == "s":
            reg = opciones_input(categoria.nro_categoria)

            opciones_logico.seek(0, 2)
            pickle.dump(reg, opciones_logico)
            opciones_logico.flush()

            print(f"{YELLOW}Opcion {reg.nro_opcion.strip()} dada de alta{RESET}")

            otra = input("Cargar otra opcion en esta categoria? (s/n): ").lower()

            while otra != "s" and otra != "n":
                print(f"{DARK_RED}Opcion invalida{RESET}")
                otra = input("Cargar otra opcion en esta categoria? (s/n): ").lower()


def consultar_opciones():
    print(f"{RED}{BOLD}Categorias:{RESET}")

    if listar_categorias(False) == 0:
        print(f"{DARK_RED}No hay categorias cargadas{RESET}")

    else:

        posicion = pedir_posicion_categoria(False)

        categoria_logico.seek(posicion, 0)
        categoria = pickle.load(categoria_logico)
        nro_categoria = int(categoria.nro_categoria.strip())

        print(f"\nPregunta: {BOLD}{categoria.pregunta.strip()}{RESET}")

        cantidad = 0
        tamanio = os.path.getsize(OPCIONES_FISICO)

        opciones_logico.seek(0, 0)

        while opciones_logico.tell() < tamanio:
            reg = pickle.load(opciones_logico)

            if int(reg.nro_categoria.strip()) == nro_categoria:
                print(f"    {reg.objeto.strip()}: {reg.valor.strip()}")
                cantidad += 1

        if cantidad == 0:
            print(f"{DARK_RED}No hay opciones{RESET}")


def administrar_categorias():
    opcion = ""

    while opcion != "4":

        clear()

        print(f"""
    {RED}{BOLD}===== ADMINISTRAR CATEGORIAS ====={RESET}

    {RED}[*]{RESET} {YELLOW}1.{RESET} Alta
    {RED}[*]{RESET} {YELLOW}2.{RESET} Modificacion
    {RED}[*]{RESET} {YELLOW}3.{RESET} Baja
    {RED}[*]{RESET} {YELLOW}4.{RESET} Volver
    """)

        opcion = input("Ingrese una opcion: ")

        while opcion not in ("1", "2", "3", "4"):
            print(f"{DARK_RED}Opcion invalida{RESET}")
            opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            alta_categoria()
            input("Presione enter para continuar...")

        elif opcion == "2":
            modificar_categoria()
            input("Presione enter para continuar...")

        elif opcion == "3":
            baja_categoria()
            input("Presione enter para continuar...")


def administrar_opciones():
    opcion = ""

    while opcion != "3":
        clear()

        print(f"""
    {RED}{BOLD}===== ADMINISTRAR OPCIONES ====={RESET}

    {RED}[*]{RESET} {YELLOW}1.{RESET} Alta
    {RED}[*]{RESET} {YELLOW}2.{RESET} Consulta
    {RED}[*]{RESET} {YELLOW}3.{RESET} Volver
    """)

        opcion = input("Ingrese una opcion: ")

        while opcion not in ("1", "2", "3"):
            print(f"{DARK_RED}Opcion invalida{RESET}")
            opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            alta_opcion()
            input("Presione enter para continuar...")

        elif opcion == "2":
            consultar_opciones()
            input("Presione enter para continuar...")


def admin():
    if not pedir_contrasena():
        print(f"{DARK_RED}Supero los 3 intentos{RESET}")
        input("Presione enter para continuar...")

    else:

        opcion = ""

        while opcion != "3":
            clear()

            print(f"""
    {RED}{BOLD}===== ADMINISTRACION DE JUEGOS ====={RESET}

    {RED}[*]{RESET} {YELLOW}1.{RESET} Administrar Categorias
    {RED}[*]{RESET} {YELLOW}2.{RESET} Administrar Opciones
    {RED}[*]{RESET} {YELLOW}3.{RESET} Volver
    """)

            opcion = input("Ingrese una opcion: ")

            while opcion not in ("1", "2", "3"):
                print(f"{DARK_RED}Opcion invalida{RESET}")
                opcion = input("Ingrese una opcion: ")

            if opcion == "1":
                administrar_categorias()

            elif opcion == "2":
                administrar_opciones()


def despedida():
    clear()

    print(f"""{RED}{BOLD}
+==============================================================+
|                                                              |
|   {WHITE}Gracias por jugar, no apueste, juega por diversion{RED}         |
|                                                              |
+==============================================================+
{RESET}""")


def main():
    clear()

    print(texto)

    input("Presione enter para jugar...")

    option = ""

    while option != "g":
        clear()

        print(f"""
    {RED}{BOLD}===== MENU PRINCIPAL ====={RESET}

    {RED}[*]{RESET} {YELLOW}A.{RESET} Juego de mayor o menor
    {RED}[*]{RESET} {YELLOW}B.{RESET} Adivinar el numero secreto
    {RED}[*]{RESET} {YELLOW}C.{RESET} BlackJack
    {RED}[*]{RESET} {YELLOW}D.{RESET} Par o impar
    {RED}[*]{RESET} {YELLOW}E.{RESET} Reporte
    {RED}[*]{RESET} {YELLOW}F.{RESET} Administracion de juegos
    {RED}[*]{RESET} {YELLOW}G.{RESET} Salir
    """)

        option = input("Ingrese una opcion: ").lower()

        while option not in ("a", "b", "c", "d", "e", "f", "g"):
            option = input("Ingrese una opcion: ").lower()

        if option == "a":
            mayor_menor()

        elif option == "b":
            numero_secreto()

        elif option == "c":
            blackjack()

        elif option == "d":
            par_impar()

        elif option == "e":
            reporte()

        elif option == "f":
            admin()

        elif option == "g":
            despedida()
            input("Presione enter para salir...")

    categoria_logico.close()
    opciones_logico.close()
    jugadores_logico.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        despedida()
        categoria_logico.close()
        opciones_logico.close()
        jugadores_logico.close()
