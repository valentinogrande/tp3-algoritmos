import os
import pickle


# las clases tienen que llamarse igual que en main.py para poder leer los registros
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


class JugadoresRegistro:
    def __init__(self):
        self.nombre = ""
        self.creditos = 10000.0
        self.juegos = [[0] * 4 for i in range(2)]


RUTA = os.path.dirname(os.path.abspath(__file__))

CATEGORIAS_FISICO = os.path.join(RUTA, "Categorias.dat")
OPCIONES_FISICO = os.path.join(RUTA, "Opciones.dat")
JUGADORES_FISICO = os.path.join(RUTA, "Jugadores.dat")


def mostrar_categorias():
    print("===== CATEGORIAS =====")

    if not os.path.exists(CATEGORIAS_FISICO) or os.path.getsize(CATEGORIAS_FISICO) == 0:
        print("no hay categorias")
    else:
        tamanio = os.path.getsize(CATEGORIAS_FISICO)
        logico = open(CATEGORIAS_FISICO, "rb")

        while logico.tell() < tamanio:
            reg = pickle.load(logico)
            print(reg.nro_categoria.strip(), "|", reg.nombre_categoria.strip(), "|", reg.estado)
            print("   pregunta:", reg.pregunta.strip())

        logico.close()

    print()


def mostrar_opciones():
    print("===== OPCIONES =====")

    if not os.path.exists(OPCIONES_FISICO) or os.path.getsize(OPCIONES_FISICO) == 0:
        print("no hay opciones")
    else:
        tamanio = os.path.getsize(OPCIONES_FISICO)
        logico = open(OPCIONES_FISICO, "rb")

        while logico.tell() < tamanio:
            reg = pickle.load(logico)
            print(reg.nro_opcion.strip(), "| categoria", reg.nro_categoria.strip(), "|", reg.objeto.strip(), "=", reg.valor.strip())

        logico.close()

    print()


def mostrar_jugadores():
    print("===== JUGADORES =====")

    if not os.path.exists(JUGADORES_FISICO) or os.path.getsize(JUGADORES_FISICO) == 0:
        print("no hay jugadores")
    else:
        tamanio = os.path.getsize(JUGADORES_FISICO)
        logico = open(JUGADORES_FISICO, "rb")

        while logico.tell() < tamanio:
            reg = pickle.load(logico)
            print(reg.nombre.strip(), "| $", reg.creditos)
            print("   ganadas: ", reg.juegos[0])
            print("   perdidas:", reg.juegos[1])

        logico.close()

    print()


mostrar_categorias()
mostrar_opciones()
mostrar_jugadores()
