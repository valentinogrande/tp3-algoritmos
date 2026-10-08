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
from pathlib import Path


class CategoriaRegistro:
    def __init__(self):
        self.nro_categoria = 0
        self.nombre_categoria = ""
        self.pregunta = ""
        self.estado = ""


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


def pedir_nombre_categoria():
    nombre = input("Introduce el nombre de la categoria: ").strip()
    valido = False

    while not valido:

        if len(nombre) == 0 or len(nombre) > 30:
            print("El nombre debe tener entre 1 y 30 caracteres")
            nombre = input("Introduce el nombre de la categoria: ").strip()

        elif buscar_categoria(nombre) != -1:
            print("Ya existe una categoria con ese nombre")
            nombre = input("Introduce el nombre de la categoria: ").strip()

        else:
            valido = True

    return nombre


def categoria_input():

    reg = CategoriaRegistro()

    reg.nro_categoria = str(leer_numero_previo_categoria() + 1).ljust(4, " ")

    nombre = pedir_nombre_categoria()
    reg.nombre_categoria = nombre.ljust(30, " ")

    pregunta = input("Introduce la pregunta: ").strip()
    while len(pregunta) == 0 or len(pregunta) > 200:
        print("La pregunta debe tener entre 1 y 200 caracteres")
        pregunta = input("Introduce la pregunta: ").strip()

    reg.pregunta = pregunta.ljust(200, " ")

    reg.estado = "A"

    return reg


class OpcionesRegistro:
    def __init__(self):
        self.nro_categoria = 0
        self.nro_opcion = 0
        self.objeto = ""
        self.valor = 0


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

    objeto = input("Introduce el nombre del objeto: ").strip()
    while len(objeto) == 0 or len(objeto) > 100:
        print("El objeto debe tener entre 1 y 100 caracteres")
        objeto = input("Introduce el nombre del objeto: ").strip()

    reg.objeto = objeto.ljust(100, " ")

    valor = input("Introduce el valor: ").strip()
    while len(valor) > 10 or not valor.isdigit():
        print("El valor debe ser un numero entero positivo de hasta 10 digitos")
        valor = input("Introduce el valor: ").strip()

    reg.valor = valor.ljust(10, " ")

    return reg


class JugadoresRegistro:
    def __init__(self):
        self.nombre = ""
        self.creditos = 10000.0
        # Fila 0: veces que gano, fila 1: veces que perdio
        # Columna 0: mayor/menor, 1: numero secreto, 2: blackjack, 3: par/impar
        self.juegos = [[0] * 4 for i in range(2)]


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


def leer_jugador(posicion):
    jugadores_logico.seek(posicion, 0)
    reg = pickle.load(jugadores_logico)

    return reg


def alta_jugador(nombre):
    reg = JugadoresRegistro()
    reg.nombre = nombre.ljust(30, " ")

    jugadores_logico.seek(0, 2)
    posicion = jugadores_logico.tell()
    pickle.dump(reg, jugadores_logico)
    jugadores_logico.flush()

    return posicion


def pedir_jugador():
    nombre = input("Ingrese su nombre (2 a 30 caracteres): ").strip()

    while len(nombre) < 2 or len(nombre) > 30:
        print("El nombre debe tener entre 2 y 30 caracteres")
        nombre = input("Ingrese su nombre (2 a 30 caracteres): ").strip()

    posicion = buscar_nombre(nombre)

    if posicion != -1:
        print(f"Bienvenido de nuevo {nombre}")

    else:
        posicion = alta_jugador(nombre)
        print(f"Jugador {nombre} registrado con ${JugadoresRegistro().creditos}")

    return posicion


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
MAX_CARTAS_MANO = TAMANIO_MAZO
CONTRASENA = "admin123"
INTENTOS_CONTRASENA = 3


RUTA = Path(__file__).resolve().parent

CATEGORIAS_FISICO = RUTA / "Categorias.dat"
OPCIONES_FISICO = RUTA / "Opciones.dat"
JUGADORES_FISICO = RUTA / "Jugadores.dat"

categoria_logico = open(CATEGORIAS_FISICO, "r+b")
opciones_logico = open(OPCIONES_FISICO, "r+b")
jugadores_logico = open(JUGADORES_FISICO, "r+b")

NOMBRES_JUEGOS = ["Mayor o menor", "Numero secreto", "BlackJack", "Par o impar"]

numero_maximo_intentos_secreto = 5

RONDAS_MAYOR_MENOR = 6
ACIERTOS_PARA_GANAR = 4
MINIMO_OPCIONES = 6

RED = "\033[91m"
DARK_RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"
WHITE = "\033[97m"

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


def clear():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("No se puede limpiar la pantalla")


def contar_opciones(nro_categoria):
    cantidad = 0
    tamanio = os.path.getsize(OPCIONES_FISICO)

    opciones_logico.seek(0, 0)

    while opciones_logico.tell() < tamanio:
        reg = pickle.load(opciones_logico)

        if int(reg.nro_categoria.strip()) == nro_categoria:
            cantidad += 1

    return cantidad


def categoria_jugable(reg):
    jugable = False

    if reg.estado == "A":
        jugable = contar_opciones(int(reg.nro_categoria.strip())) >= MINIMO_OPCIONES

    return jugable


def recorrer_categorias_jugables(mostrar):
    cantidad = 0
    tamanio = os.path.getsize(CATEGORIAS_FISICO)
    posicion = 0

    while posicion < tamanio:
        categoria_logico.seek(posicion, 0)
        reg = pickle.load(categoria_logico)
        posicion = categoria_logico.tell()

        if categoria_jugable(reg):
            if mostrar:
                print(f"    {reg.nro_categoria.strip()} - {reg.nombre_categoria.strip()}")
            cantidad += 1

    return cantidad


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


def pedir_categoria():
    reg = None

    while reg is None:

        try:

            nro_categoria = int(input("Elegi el numero de categoria: "))
            posicion = buscar_categoria_por_numero(nro_categoria)

            if posicion == -1:
                print("No existe una categoria con ese numero")

            else:
                categoria_logico.seek(posicion, 0)
                candidata = pickle.load(categoria_logico)

                if categoria_jugable(candidata):
                    reg = candidata
                else:
                    print("Esa categoria no esta disponible para jugar")

        except ValueError:
            print("Ingrese un entero valido")

    return reg


def cargar_opciones(nro_categoria, objetos, valores):
    cantidad = 0
    tamanio = os.path.getsize(OPCIONES_FISICO)

    opciones_logico.seek(0, 0)

    while opciones_logico.tell() < tamanio:
        reg = pickle.load(opciones_logico)

        if int(reg.nro_categoria.strip()) == nro_categoria:
            objetos[cantidad] = reg.objeto.strip()
            valores[cantidad] = int(reg.valor.strip())
            cantidad += 1

    return cantidad


def elegir_opcion(usadas, cantidad, actual):
    disponibles = 0
    i = 0

    while i < cantidad:
        if not usadas[i]:
            disponibles += 1
        i += 1

    # Si ya salieron todas, se vuelven a habilitar menos la que esta en juego
    if disponibles == 0:
        i = 0

        while i < cantidad:
            usadas[i] = i == actual
            i += 1

    elegida = random.randint(0, cantidad - 1)

    while usadas[elegida]:
        elegida = random.randint(0, cantidad - 1)

    usadas[elegida] = True

    return elegida


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

    while ronda <= RONDAS_MAYOR_MENOR:

        nueva = elegir_opcion(usadas, cantidad, actual)

        print(f"\nRonda {ronda} de {RONDAS_MAYOR_MENOR}")
        print(categoria.pregunta.strip())
        print(f"1. {objetos[actual]} / 2. {objetos[nueva]}")

        respuesta = input("Elegi 1 o 2: ")

        while respuesta != "1" and respuesta != "2":
            print("Opcion invalida")
            respuesta = input("Elegi 1 o 2: ")

        if valores[actual] >= valores[nueva]:
            correcta = actual
        else:
            correcta = nueva

        if respuesta == "1":
            elegida = actual
        else:
            elegida = nueva

        print(f"{objetos[actual]} {valores[actual]} / {objetos[nueva]} {valores[nueva]}")

        if valores[elegida] == valores[correcta]:
            print("Correcto! Sumas 1 punto")
            aciertos += 1
        else:
            print("Incorrecto")

        print(f"Aciertos: {aciertos}")
        input("Presione enter para continuar...")

        actual = correcta
        ronda += 1

    return aciertos


def mayor_menor():

    posicion = pedir_jugador()
    reg = leer_jugador(posicion)
    nombre = reg.nombre.strip()

    if reg.creditos <= 0:
        print(f"{nombre} te quedaste sin credito, ya no podes jugar")

    else:

        if recorrer_categorias_jugables(False) == 0:
            print(f"No hay categorias activas con al menos {MINIMO_OPCIONES} opciones")

        else:

            print(f"Tu credito es de: ${reg.creditos}")
            apuesta = pedir_apuesta(reg.creditos)

            print("\nCategorias:")
            recorrer_categorias_jugables(True)

            categoria = pedir_categoria()
            aciertos = jugar_rondas_mayor_menor(categoria)

            print(f"\nTerminaste con {aciertos} aciertos de {RONDAS_MAYOR_MENOR}")

            if aciertos >= ACIERTOS_PARA_GANAR:
                print(f"{nombre} ganaste ${apuesta}")
                reg.creditos += apuesta
                reg.juegos[0][0] += 1

            else:
                print(f"{nombre} perdiste ${apuesta}")
                reg.creditos -= apuesta
                reg.juegos[1][0] += 1

            jugadores_logico.seek(posicion, 0)
            pickle.dump(reg, jugadores_logico)
            jugadores_logico.flush()

            print(f"Tu credito ahora es: ${reg.creditos}")

    input("Presione enter para continuar...")


def numero_secreto():

    posicion = pedir_jugador()

    secreto =random.randint(1, 100)

    numero_intento = 0
    victoria = False

    while numero_intento < numero_maximo_intentos_secreto and not victoria:

        print(f"Intentos restantes: {numero_maximo_intentos_secreto - numero_intento}")

        valido = False
        intento = 0

        while not valido:

            try:

                intento = int(input("Ingrese un numero entre 1 y 100: "))

                if intento < 1 or intento > 100:
                    print("El numero debe estar entre 1 y 100")

                else:
                    valido = True

            except ValueError:
                print("Ingrese un entero valido")

        numero_intento += 1

        if intento == secreto:

            victoria = True

        else:

            if intento < secreto:
                print("El numero secreto es mayor")

            else:
                print("El numero secreto es menor")

    if victoria:
        print(f"Ganaste! Te llevo {numero_intento} intentos")

    else:
        print("Perdiste")
        print(f"El numero era: {secreto}")

    registrar_resultado(posicion, 1, victoria)

    input("Presione enter para continuar...")


def armar_mazo(mazo):
    palos = ["corazones", "diamantes", "picas", "treboles"]
    numeros = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    cantidad = 0
    i = 0

    while i < len(palos):
        j = 0

        while j < len(numeros):
            mazo[cantidad] = numeros[j] + " de " + palos[i]
            cantidad += 1
            j += 1

        i += 1

    return cantidad


def sacar_carta(mazo, cantidad):
    indice_carta = random.randint(0, cantidad - 1)
    carta = mazo[indice_carta]

    mazo[indice_carta] = mazo[cantidad - 1]

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
    ases = 0
    i = 0

    while i < cantidad:
        numero = obtener_numero_carta(cartas[i])

        if numero == "J" or numero == "Q" or numero == "K":
            total += 10

        elif numero == "A":
            total += 11
            ases += 1

        else:
            total += int(numero)

        i += 1

    while total > 21 and ases > 0:
        total -= 10
        ases -= 1

    return total


def blackjack():

    posicion = pedir_jugador()
    nombre = leer_jugador(posicion).nombre.strip()

    jugar_otra = True

    while jugar_otra:

        mazo = [""] * TAMANIO_MAZO
        cantidad_mazo = armar_mazo(mazo)

        cartas_jugador = [""] * MAX_CARTAS_MANO
        cartas_banca = [""] * MAX_CARTAS_MANO

        cantidad_cartas_jugador = 0
        cantidad_cartas_banca = 0

        cartas_jugador[cantidad_cartas_jugador] = sacar_carta(mazo, cantidad_mazo)
        cantidad_cartas_jugador += 1
        cantidad_mazo -= 1

        cartas_banca[cantidad_cartas_banca] = sacar_carta(mazo, cantidad_mazo)
        cantidad_cartas_banca += 1
        cantidad_mazo -= 1

        cartas_jugador[cantidad_cartas_jugador] = sacar_carta(mazo, cantidad_mazo)
        cantidad_cartas_jugador += 1
        cantidad_mazo -= 1

        cartas_banca[cantidad_cartas_banca] = sacar_carta(mazo, cantidad_mazo)
        cantidad_cartas_banca += 1
        cantidad_mazo -= 1

        puntos_jugador = sumar_puntos(cartas_jugador, cantidad_cartas_jugador)
        puntos_banca = sumar_puntos(cartas_banca, cantidad_cartas_banca)

        print(f"\nCarta visible de la banca: {cartas_banca[0]}")
        print(f"Tus cartas: {cartas_jugador[0]} y {cartas_jugador[1]}")
        print(f"Tus puntos: {puntos_jugador}")

        se_paso = False
        turno_jugador = puntos_jugador < 21

        while turno_jugador:

            opcion = input("Queres pedir o plantarte? (pedir/plantarse): ").lower()

            while opcion != "pedir" and opcion != "plantarse":
                opcion = input("Ingrese pedir o plantarse: ").lower()

            if opcion == "pedir":

                carta = sacar_carta(mazo, cantidad_mazo)
                cantidad_mazo -= 1

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
            print("Te pasaste de 21. Gana la banca")
            registrar_resultado(posicion, 2, False)

        else:

            print(f"La banca da vuelta su carta: {cartas_banca[1]}")

            while puntos_banca <= 16:
                carta = sacar_carta(mazo, cantidad_mazo)
                cantidad_mazo -= 1

                cartas_banca[cantidad_cartas_banca] = carta
                cantidad_cartas_banca += 1

                puntos_banca = sumar_puntos(cartas_banca, cantidad_cartas_banca)
                print(f"La banca saco: {carta}")

            print(f"Puntos de la banca: {puntos_banca}")
            print(f"Tus puntos: {puntos_jugador}")

            if puntos_banca > 21:
                print(f"La banca se paso de 21. Ganaste {nombre}")
                registrar_resultado(posicion, 2, True)

            elif puntos_jugador > puntos_banca:
                print(f"Ganaste {nombre}")
                registrar_resultado(posicion, 2, True)

            elif puntos_banca > puntos_jugador:
                print("Gana la banca")
                registrar_resultado(posicion, 2, False)

            else:
                print("Empate")

        respuesta = input("Queres jugar otra partida? (si/no): ").lower()

        while respuesta != "si" and respuesta != "no":
            respuesta = input("Ingrese si o no: ").lower()

        jugar_otra = respuesta == "si"

    input("Presione enter para continuar...")


def pedir_apuesta(credito):
    apuesta_valida = False
    apuesta = 0

    while not apuesta_valida:

        try:

            apuesta = int(input("Cuanto queres apostar?: "))

            if apuesta < 1:
                print("La apuesta debe ser mayor a 0")

            elif apuesta > credito:
                print("No podes apostar mas de lo que tenes")

            else:
                apuesta_valida = True

        except ValueError:
            print("Ingrese un entero valido")

    return apuesta


def par_impar():

    posicion = pedir_jugador()
    reg = leer_jugador(posicion)
    nombre = reg.nombre.strip()

    if reg.creditos <= 0:
        print(f"{nombre} te quedaste sin credito, ya no podes jugar")

    else:

        print(f"Tu credito es de: ${reg.creditos}")

        apuesta = pedir_apuesta(reg.creditos)

        numero1 = random.randint(1, 6)
        numero2 = random.randint(1, 6)

        opcion = input("Par o impar?: ").lower()

        while opcion != "par" and opcion != "impar":
            opcion = input("Ingrese par o impar: ").lower()

        suma = numero1 + numero2

        print(f"Los numeros fueron: {numero1} y {numero2}")
        print(f"La suma es: {suma}")

        suma_es_par = suma % 2 == 0
        gano = (opcion == "par" and suma_es_par) or (
            opcion == "impar" and not suma_es_par
        )

        if gano:
            print(f"{nombre} ganaste")
            reg.creditos += apuesta
            reg.juegos[0][3] += 1

        else:
            print(f"{nombre} perdiste")
            reg.creditos -= apuesta
            reg.juegos[1][3] += 1

        jugadores_logico.seek(posicion, 0)
        pickle.dump(reg, jugadores_logico)
        jugadores_logico.flush()

        print(f"Tu credito ahora es: ${reg.creditos}")

    input("Presione enter para continuar...")


def contar_jugadores():
    cantidad = 0
    tamanio = os.path.getsize(JUGADORES_FISICO)

    jugadores_logico.seek(0, 0)

    while jugadores_logico.tell() < tamanio:
        pickle.load(jugadores_logico)
        cantidad += 1

    return cantidad


def ordenar_y_mostrar(nombres, valores, cantidad):
    i = 0

    while i < cantidad - 1:
        j = i + 1

        while j < cantidad:

            if valores[i] < valores[j]:
                aux = valores[i]
                valores[i] = valores[j]
                valores[j] = aux

                aux = nombres[i]
                nombres[i] = nombres[j]
                nombres[j] = aux

            j += 1

        i += 1

    i = 0

    while i < cantidad:
        print(f"{i + 1} - {nombres[i]}: ${valores[i]}")
        i += 1


def reporte_creditos():
    cantidad = contar_jugadores()

    if cantidad == 0:
        print("Todavia no hay jugadores")

    else:

        nombres = [""] * cantidad
        creditos = [0.0] * cantidad

        jugadores_logico.seek(0, 0)
        i = 0

        while i < cantidad:
            reg = pickle.load(jugadores_logico)
            nombres[i] = reg.nombre.strip()
            creditos[i] = reg.creditos
            i += 1

        print("\n[*] Jugadores ordenados por credito")
        ordenar_y_mostrar(nombres, creditos, cantidad)


def reporte_jugador():
    nombre = input("Ingrese el nombre del jugador: ").strip()

    posicion = buscar_nombre(nombre)

    if posicion == -1:
        print("Ese jugador no existe")

    else:

        reg = leer_jugador(posicion)
        jugo_algo = False

        print(f"\nJuegos jugados por {nombre}")

        juego = 0

        while juego < 4:

            ganadas = reg.juegos[0][juego]
            perdidas = reg.juegos[1][juego]

            if ganadas + perdidas > 0:
                jugo_algo = True
                print(f"\n[*] {NOMBRES_JUEGOS[juego]}")
                print(f"Ganadas: {ganadas}")
                print(f"Perdidas: {perdidas}")

            juego += 1

        if not jugo_algo:
            print(f"{nombre} todavia no tiene partidas registradas")

        print(f"\nCreditos: ${reg.creditos}")


def reporte():

    opcion = ""

    while opcion != "c":

        clear()

        print("""
    ===== REPORTE =====

    [*] A. Jugadores ordenados por credito
    [*] B. Juegos jugados por un jugador
    [*] C. Volver al menu principal
    """)

        opcion = input("Ingrese una opcion: ").lower()

        while opcion not in ("a", "b", "c"):
            print("Opcion invalida")
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

    while intentos < INTENTOS_CONTRASENA and not correcta:
        contrasena = pwinput.pwinput("Ingrese la contrasena: ", mask="*")
        intentos += 1

        if contrasena == CONTRASENA:
            correcta = True
        else:
            print(f"Contrasena incorrecta. Intentos restantes: {INTENTOS_CONTRASENA - intentos}")

    return correcta


def listar_categorias(solo_activas):
    cantidad = 0
    tamanio = os.path.getsize(CATEGORIAS_FISICO)

    categoria_logico.seek(0, 0)

    while categoria_logico.tell() < tamanio:
        reg = pickle.load(categoria_logico)

        if not solo_activas or reg.estado == "A":
            print(f"    {reg.nro_categoria.strip()} - {reg.nombre_categoria.strip()}")
            cantidad += 1

    return cantidad


def pedir_posicion_categoria(solo_activas):
    posicion = -1

    while posicion == -1:

        try:

            nro_categoria = int(input("Ingrese el numero de categoria: "))
            posicion = buscar_categoria_por_numero(nro_categoria)

            if posicion == -1:
                print("No existe una categoria con ese numero")

            elif solo_activas:
                categoria_logico.seek(posicion, 0)
                reg = pickle.load(categoria_logico)

                if reg.estado != "A":
                    print("Esa categoria no esta activa")
                    posicion = -1

        except ValueError:
            print("Ingrese un entero valido")

    return posicion


def alta_categoria():
    reg = categoria_input()

    categoria_logico.seek(0, 2)
    pickle.dump(reg, categoria_logico)
    categoria_logico.flush()

    print(f"Categoria {reg.nro_categoria.strip()} - {reg.nombre_categoria.strip()} dada de alta")


def modificar_categoria():
    print("Categorias activas:")

    if listar_categorias(True) == 0:
        print("No hay categorias activas")

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

        print(f"Categoria {reg.nro_categoria.strip()} modificada")


def baja_categoria():
    print("Categorias activas:")

    if listar_categorias(True) == 0:
        print("No hay categorias activas")

    else:

        posicion = pedir_posicion_categoria(True)

        categoria_logico.seek(posicion, 0)
        reg = pickle.load(categoria_logico)
        reg.estado = "I"

        categoria_logico.seek(posicion, 0)
        pickle.dump(reg, categoria_logico)
        categoria_logico.flush()

        print(f"Categoria {reg.nro_categoria.strip()} - {reg.nombre_categoria.strip()} dada de baja")


def alta_opcion():
    print("Categorias activas:")

    if listar_categorias(True) == 0:
        print("Antes de registrar opciones se deben dar de alta categorias")

    else:

        posicion = pedir_posicion_categoria(True)

        categoria_logico.seek(posicion, 0)
        categoria = pickle.load(categoria_logico)

        print(f"Pregunta: {categoria.pregunta.strip()}")

        otra = "s"

        while otra == "s":

            reg = opciones_input(categoria.nro_categoria)

            opciones_logico.seek(0, 2)
            pickle.dump(reg, opciones_logico)
            opciones_logico.flush()

            print(f"Opcion {reg.nro_opcion.strip()} dada de alta")

            otra = input("Cargar otra opcion en esta categoria? (s/n): ").lower()

            while otra != "s" and otra != "n":
                print("Opcion invalida")
                otra = input("Cargar otra opcion en esta categoria? (s/n): ").lower()


def consultar_opciones():
    print("Categorias:")

    if listar_categorias(False) == 0:
        print("No hay categorias cargadas")

    else:

        posicion = pedir_posicion_categoria(False)

        categoria_logico.seek(posicion, 0)
        categoria = pickle.load(categoria_logico)
        nro_categoria = int(categoria.nro_categoria.strip())

        print(f"\nPregunta: {categoria.pregunta.strip()}")

        cantidad = 0
        tamanio = os.path.getsize(OPCIONES_FISICO)

        opciones_logico.seek(0, 0)

        while opciones_logico.tell() < tamanio:
            reg = pickle.load(opciones_logico)

            if int(reg.nro_categoria.strip()) == nro_categoria:
                print(f"    {reg.objeto.strip()}: {reg.valor.strip()}")
                cantidad += 1

        if cantidad == 0:
            print("La categoria no tiene opciones cargadas")


def administrar_categorias():
    opcion = ""

    while opcion != "4":

        clear()

        print("""
    ===== ADMINISTRAR CATEGORIAS =====

    [*] 1. Alta
    [*] 2. Modificacion
    [*] 3. Baja
    [*] 4. Volver
    """)

        opcion = input("Ingrese una opcion: ")

        while opcion not in ("1", "2", "3", "4"):
            print("Opcion invalida")
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

        print("""
    ===== ADMINISTRAR OPCIONES =====

    [*] 1. Alta
    [*] 2. Consulta
    [*] 3. Volver
    """)

        opcion = input("Ingrese una opcion: ")

        while opcion not in ("1", "2", "3"):
            print("Opcion invalida")
            opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            alta_opcion()
            input("Presione enter para continuar...")

        elif opcion == "2":
            consultar_opciones()
            input("Presione enter para continuar...")


def admin():

    if not pedir_contrasena():
        print(f"Supero los {INTENTOS_CONTRASENA} intentos de ingresar contrasena, salga e intente nuevamente")
        input("Presione enter para continuar...")

    else:

        opcion = ""

        while opcion != "3":

            clear()

            print("""
    ===== ADMINISTRACION DE JUEGOS =====

    [*] 1. Administrar Categorias
    [*] 2. Administrar Opciones
    [*] 3. Volver
    """)

            opcion = input("Ingrese una opcion: ")

            while opcion not in ("1", "2", "3"):
                print("Opcion invalida")
                opcion = input("Ingrese una opcion: ")

            if opcion == "1":
                administrar_categorias()

            elif opcion == "2":
                administrar_opciones()


def main():

    clear()

    print(texto)

    input("Presione enter para jugar...")

    option = ""

    while option != "g":
        clear()

        print("""
    [*] A. Juego de mayor o menor
    [*] B. Adivinar el numero secreto
    [*] C. BlackJack
    [*] D. Par o impar
    [*] E. Reporte
    [*] F. Administracion de juegos
    [*] G. Salir
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
            clear()

            print("""
+==============================================================+
|                                                              |
|   Gracias por jugar, no apueste, juega por diversion         |
|                                                              |
+==============================================================+
    """)

            input("Presione enter para salir...")

    categoria_logico.close()
    opciones_logico.close()
    jugadores_logico.close()


if __name__ == '__main__':
    main()
