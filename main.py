
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

class OpcionesRegistro:
    def __init__(self):
        self.nro_categoria = 0
        self.nro_opcion = 0
        self.objeto = ""
        self.valor = 0

class  JugadoresRegistro:
    def __init__(self):
        self.nombre = ""
        self.creditos = 0
        self.juegos = [[0, 0, 0, 0] for _ in range(2)]


MAX_JUGADORES = 10
TAMANIO_MAZO = 52
MAX_CARTAS_MANO = TAMANIO_MAZO
CONTRASENA = "admin123"


RUTA = Path(__file__).resolve().parent

CATEGORIAS_FISICO = RUTA / "Categorias.dat"
OPCIONES_FISICO = RUTA / "Opciones.dat"
JUGADORES_FISICO = RUTA / "Jugadores.dat"


jugadores = [""] * MAX_JUGADORES

rachas_mayor_menor = [0] * MAX_JUGADORES
mayor_menor_jugadas = [0] * MAX_JUGADORES

secreto_jugadas = [0] * MAX_JUGADORES
secreto_ganadas = [0] * MAX_JUGADORES
secreto_perdidas = [0] * MAX_JUGADORES

blackjack_jugadas = [0] * MAX_JUGADORES
blackjack_ganadas = [0] * MAX_JUGADORES

parimpar_jugadas = [0] * MAX_JUGADORES
parimpar_aciertos = [0] * MAX_JUGADORES
creditos = [0] * MAX_JUGADORES

cantidad_jugadores = 0

numero_maximo_intentos_secreto = 6

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


def buscar_jugador(nombre):
    indice = -1
    i = 0

    while i < cantidad_jugadores:
        if jugadores[i] == nombre:
            indice = i
        i += 1

    return indice


def pedir_jugador():
    global cantidad_jugadores

    nombre = input("Ingrese su nombre (2 o mas caracteres): ")

    while len(nombre) < 2:
        nombre = input("Ingrese su nombre (2 o mas caracteres): ")

    indice = buscar_jugador(nombre)

    if indice != -1:
        print("Bienvenido de nuevo", nombre)

    else:
        if cantidad_jugadores == MAX_JUGADORES:
            print("No hay cupos para un nuevo jugador")
            indice = -1

        else:
            indice = cantidad_jugadores

            jugadores[indice] = nombre
            rachas_mayor_menor[indice] = 0
            mayor_menor_jugadas[indice] = 0
            secreto_jugadas[indice] = 0
            secreto_ganadas[indice] = 0
            secreto_perdidas[indice] = 0
            blackjack_jugadas[indice] = 0
            blackjack_ganadas[indice] = 0
            parimpar_jugadas[indice] = 0
            parimpar_aciertos[indice] = 0
            creditos[indice] = 1000

            cantidad_jugadores += 1

    return indice


def mayor_menor():

    indice = pedir_jugador()

    if indice == -1:
        input("Presione enter para continuar...")
        return

    nombre = jugadores[indice]
    mayor_menor_jugadas[indice] += 1

    racha_juego = 0
    juego_terminado = False

    numero = random.randint(1, 1000)

    while not juego_terminado:

        siguiente_numero = random.randint(1, 1000)

        while siguiente_numero == numero:
            siguiente_numero = random.randint(1, 1000)

        print("Numero actual:", numero)

        opcion = input("El siguiente numero sera mayor o menor?: ").lower()

        while opcion != "mayor" and opcion != "menor":
            opcion = input("Ingrese mayor o menor: ").lower()

        acerto = (opcion == "menor" and siguiente_numero < numero) or (
            opcion == "mayor" and siguiente_numero > numero
        )

        if acerto:

            print("Correcto! El numero era:", siguiente_numero)

            racha_juego += 1
            numero = siguiente_numero

        else:
            print("El juego esta terminado. El numero era:", siguiente_numero)
            juego_terminado = True

    print(nombre, "tu racha fue de:", racha_juego)

    if racha_juego > rachas_mayor_menor[indice]:
        rachas_mayor_menor[indice] = racha_juego

    input("Presione enter para continuar...")


def numero_secreto():

    indice = pedir_jugador()

    if indice == -1:
        input("Presione enter para continuar...")
        return

    secreto_jugadas[indice] += 1

    secreto = random.randint(1, 100)

    numero_intento = 0
    victoria = False

    while numero_intento < numero_maximo_intentos_secreto and not victoria:

        print(
            "Intentos restantes:",
            numero_maximo_intentos_secreto - numero_intento,
        )

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

        secreto_ganadas[indice] += 1
        print("Ganaste! Te llevo", numero_intento, "intentos")

    else:

        secreto_perdidas[indice] += 1
        print("Perdiste")
        print("El numero era:", secreto)

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

    indice = pedir_jugador()

    if indice == -1:
        input("Presione enter para continuar...")
        return

    nombre = jugadores[indice]

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

        blackjack_jugadas[indice] += 1

        puntos_jugador = sumar_puntos(cartas_jugador, cantidad_cartas_jugador)
        puntos_banca = sumar_puntos(cartas_banca, cantidad_cartas_banca)

        print("\nCartas de la banca:", cartas_banca[0], "y", cartas_banca[1])
        print("Tus cartas:", cartas_jugador[0], "y", cartas_jugador[1])
        print("Tus puntos:", puntos_jugador)

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

                print("Sacaste:", carta)
                print("Tus puntos:", puntos_jugador)

                if puntos_jugador > 21:
                    se_paso = True
                    turno_jugador = False

                elif puntos_jugador == 21:
                    turno_jugador = False

            else:
                turno_jugador = False

        if se_paso:
            print("Te pasaste de 21. Gana la banca")

        else:

            while puntos_banca <= 16:
                carta = sacar_carta(mazo, cantidad_mazo)
                cantidad_mazo -= 1

                cartas_banca[cantidad_cartas_banca] = carta
                cantidad_cartas_banca += 1

                puntos_banca = sumar_puntos(cartas_banca, cantidad_cartas_banca)
                print("La banca saco:", carta)

            print("Puntos de la banca:", puntos_banca)
            print("Tus puntos:", puntos_jugador)

            if puntos_banca > 21:
                print("La banca se paso de 21. Ganaste", nombre)
                blackjack_ganadas[indice] += 1

            elif puntos_jugador > puntos_banca:
                print("Ganaste", nombre)
                blackjack_ganadas[indice] += 1

            elif puntos_banca > puntos_jugador:
                print("Gana la banca")

            else:
                print("Empate")

        respuesta = input("Queres jugar otra partida? (si/no): ").lower()

        while respuesta != "si" and respuesta != "no":
            respuesta = input("Ingrese si o no: ").lower()

        jugar_otra = respuesta == "si"

    input("Presione enter para continuar...")


def par_impar():

    indice = pedir_jugador()

    if indice == -1:
        input("Presione enter para continuar...")
        return

    nombre = jugadores[indice]

    if creditos[indice] == 0:
        print(nombre, "te quedaste sin credito, ya no podes jugar")
        input("Presione enter para continuar...")
        return

    print("Tu credito es de: $", creditos[indice])

    apuesta_valida = False
    apuesta = 0

    while not apuesta_valida:

        try:

            apuesta = int(input("Cuanto queres apostar?: "))

            if apuesta < 1:
                print("La apuesta debe ser mayor a 0")

            elif apuesta > creditos[indice]:
                print("No podes apostar mas de lo que tenes")

            else:
                apuesta_valida = True

        except ValueError:
            print("Ingrese un entero valido")

    numero1 = random.randint(1, 6)
    numero2 = random.randint(1, 6)

    opcion = input("Par o impar?: ").lower()

    while opcion != "par" and opcion != "impar":
        opcion = input("Ingrese par o impar: ").lower()

    suma = numero1 + numero2

    print("Los numeros fueron:", numero1, "y", numero2)
    print("La suma es:", suma)

    suma_es_par = suma % 2 == 0
    gano = (opcion == "par" and suma_es_par) or (
        opcion == "impar" and not suma_es_par
    )

    parimpar_jugadas[indice] += 1

    if gano:

        print(nombre, "ganaste")
        parimpar_aciertos[indice] += 1
        creditos[indice] += apuesta

    else:

        print(nombre, "perdiste")
        creditos[indice] -= apuesta

    print("Tu credito ahora es: $", creditos[indice])

    input("Presione enter para continuar...")


def copiar_arreglo(origen, cantidad):
    copia = [None] * MAX_JUGADORES
    i = 0

    while i < cantidad:
        copia[i] = origen[i]
        i += 1

    return copia


def ordenar_y_mostrar(nombres, valores, cantidad, descendente):

    if cantidad == 0:
        print("Todavia no hay jugadores")
        return

    i = 0

    while i < cantidad - 1:
        j = i + 1

        while j < cantidad:

            hay_que_cambiar = False

            if descendente:
                if valores[i] < valores[j]:
                    hay_que_cambiar = True
            else:
                if valores[i] > valores[j]:
                    hay_que_cambiar = True

            if hay_que_cambiar:
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
        print(i + 1, "-", nombres[i], ":", valores[i])
        i += 1


def reporte():

    opcion = ""

    while opcion != "e":

        clear()

        print("""
    ===== REPORTE =====

    [*] A. Ranking de victorias por juego
    [*] B. Juegos jugados por un jugador
    [*] C. Jugadores de par o impar segun su credito
    [*] D. Racha de un jugador en mayor o menor
    [*] E. Volver al menu principal
    """)

        opcion = input("Ingrese una opcion: ").lower()

        while opcion not in ("a", "b", "c", "d", "e"):
            opcion = input("Ingrese una opcion: ").lower()

        if opcion == "a":

            print("\n[*] Numero secreto")
            ordenar_y_mostrar(
                copiar_arreglo(jugadores, cantidad_jugadores),
                copiar_arreglo(secreto_ganadas, cantidad_jugadores),
                cantidad_jugadores,
                True,
            )

            print("\n[*] BlackJack")
            ordenar_y_mostrar(
                copiar_arreglo(jugadores, cantidad_jugadores),
                copiar_arreglo(blackjack_ganadas, cantidad_jugadores),
                cantidad_jugadores,
                True,
            )

            print("\n[*] Par o impar")
            ordenar_y_mostrar(
                copiar_arreglo(jugadores, cantidad_jugadores),
                copiar_arreglo(parimpar_aciertos, cantidad_jugadores),
                cantidad_jugadores,
                True,
            )

            print()
            input("Presione enter para continuar...")

        elif opcion == "b":

            nombre = input("Ingrese el nombre del jugador: ")

            indice = buscar_jugador(nombre)

            if indice == -1:
                print("Ese jugador no existe")

            else:

                jugo_algo = False

                print("\nJuegos jugados por", nombre)

                if mayor_menor_jugadas[indice] > 0:
                    jugo_algo = True
                    print("\n[*] Mayor o menor")
                    print("Partidas:", mayor_menor_jugadas[indice])
                    print("Mejor racha:", rachas_mayor_menor[indice])

                if secreto_jugadas[indice] > 0:
                    jugo_algo = True
                    print("\n[*] Numero secreto")
                    print("Partidas:", secreto_jugadas[indice])
                    print("Ganadas:", secreto_ganadas[indice])
                    print("Perdidas:", secreto_perdidas[indice])

                if blackjack_jugadas[indice] > 0:
                    jugo_algo = True
                    print("\n[*] BlackJack")
                    print("Partidas:", blackjack_jugadas[indice])
                    print("Ganadas:", blackjack_ganadas[indice])

                if parimpar_jugadas[indice] > 0:
                    jugo_algo = True
                    print("\n[*] Par o impar")
                    print("Partidas:", parimpar_jugadas[indice])
                    print("Aciertos:", parimpar_aciertos[indice])
                    print("Credito: $", creditos[indice])

                if not jugo_algo:
                    print(nombre, "todavia no jugo a ningun juego")

            print()
            input("Presione enter para continuar...")

        elif opcion == "c":

            nombres_parimpar = [""] * MAX_JUGADORES
            creditos_parimpar = [0] * MAX_JUGADORES
            cantidad_parimpar = 0

            i = 0

            while i < cantidad_jugadores:
                if parimpar_jugadas[i] > 0:
                    nombres_parimpar[cantidad_parimpar] = jugadores[i]
                    creditos_parimpar[cantidad_parimpar] = creditos[i]
                    cantidad_parimpar += 1
                i += 1

            print("\n[*] Jugadores de par o impar segun su credito")

            ordenar_y_mostrar(
                nombres_parimpar, creditos_parimpar, cantidad_parimpar, False
            )

            print()
            input("Presione enter para continuar...")

        elif opcion == "d":

            nombre = input("Ingrese el nombre del jugador: ")

            indice = buscar_jugador(nombre)

            if indice == -1:
                print("Ese jugador no existe")

            else:
                if mayor_menor_jugadas[indice] == 0:
                    print(nombre, "todavia no jugo al mayor o menor")
                else:
                    print(
                        "La racha de",
                        nombre,
                        "en mayor o menor es:",
                        rachas_mayor_menor[indice],
                    )

            print()
            input("Presione enter para continuar...")

def admin():
    contrasena = pwinput.pwinput("Ingrese la contrasena: ", mask="*")
    if contrasena != CONTRASENA:
        return -1
    option = ""

    print("""
    [*] A. Categoria - Modificacion
    [*] B. Categoria - Alta
    [*] C. Categoria Baja
    [*] D. Opciones - Consulta
    [*] E. Opciones Alta
    """)

    while option not in ("a", "b", "c", "d", "e"):
        option = input("Ingrese una opcion valida: ").lower()

    if option == "a":
        pass
    elif option == "b":
        pass
    elif option == "c":
        pass
    elif option == "d":
        pass
    elif option == "e":
        pass

    return 0

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


if __name__ == '__main__':
    main()
