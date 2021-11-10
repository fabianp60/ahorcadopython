# Juego del ahorcado

import random
import os
import msvcrt
import sys

PALABRAS = []
PALABRA_OCULTA = ""
LETRAS_USADAS = []
PALABRA_IMPRIMIBLE = ''
ULTIMA_TECLA = ''
OPORTUNIDADES = 6
ADIVINASTE = False

# Funcion para limpiar pantalla independiente del sistema operativo
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_palabras():
    global PALABRAS
    try:
        with open('./data.txt', 'r', encoding="utf-8") as file:
            PALABRAS = [palabra.strip() for palabra in file if palabra != '']
        if len(PALABRAS) == 0:
            raise Exception('No hay palabras en el archivo')
    except FileNotFoundError:
        print('No se encontro el archivo data.txt')
        return False
    except Exception as e:
        print(e)
        return False
    return True

# Selecciona una palabra al azar de la lista de PALABRAS
def seleccionar_nueva_palabra():
    return random.choice(PALABRAS)

def imprimir_interfaz():
    limpiar_pantalla()
    imprimir_titulo()
    if ADIVINASTE:
        imprimir_dibujo_ganaste()
    elif OPORTUNIDADES > 0:
        imprimir_dibujo_vivo()
    else:
        imprimir_dibujo_ahorcado()
    imprimir_palabra_oculta()
    imprimir_letras_usadas()
    imprimir_atajos_de_teclado()


def imprimir_titulo():
    print('╔════════════════════════════════════════════════════╗')
    print('║ ╔════════════════════════════════════════════════╗ ║')
    print('║ ║               JUEGO DEL AHORCADO               ║ ║')
    print('║ ╚════════════════════════════════════════════════╝ ║')
    print('╚════════════════════════════════════════════════════╝\r\n')

# https://elcodigoascii.com.ar/codigos-ascii-extendidos/lineas-doble-vertical-recuadro-grafico-dos-verticales-codigo-ascii-186.html
def imprimir_dibujo_vivo():
    print('┌───┐')
    print('│ (._.)')
    print('│  ─┼─')
    print('│   │')
    print('│  / \\')
    print('│  ░▒▓\r\n')

def imprimir_dibujo_ganaste():
    print('          ╔═══════════╗')
    print(" \\('▼')/ ═╣ ¡GANASTE! ║")
    print('    │     ╚═══════════╝')
    print('    │')
    print('   / \\')
    print('   ░▒▓\r\n')


def imprimir_dibujo_ahorcado():
    txt_perdiste = f"PERDISTE, LA PALABRA ERA: {PALABRA_OCULTA.upper()}"
    print( '┌───┐    ╔' + '═'*(len(txt_perdiste) + 2) + '╗')
    print(f'│ (×_×) ═╣ {txt_perdiste} ║')
    print( '│  /│\\   ╚' + '═'*(len(txt_perdiste) + 2) + '╝')
    print( '│   │')
    print( '│  / \\')
    print( '│\r\n')


def imprimir_palabra_oculta():
    print("╔" + "═"*(16 + (len(PALABRA_IMPRIMIBLE)*2)) + "╗")
    print("║ Tu palabra es: ", end='')

    for letra in PALABRA_IMPRIMIBLE:
        print(letra + ' ', end='')
    print("║")
    print("╚" + "═"*(16 + (len(PALABRA_IMPRIMIBLE)*2)) + "╝")


def imprimir_letras_usadas():
    cant_espacios = 2
    if len(LETRAS_USADAS) > 0:
        cant_espacios = 1

    print("╔" + "═"*(16 + cant_espacios + (len(LETRAS_USADAS)*2)) + "╗")
    print("║ Letras usadas: ", end='')
    for letra in LETRAS_USADAS:
        print(letra + ' ', end='')
    print(" "*cant_espacios + "║")
    print("║ Oportunidades: " + str(OPORTUNIDADES) + " "*((len(LETRAS_USADAS)*2)-len(str(OPORTUNIDADES))) + " ║")
    print("╚" + "═"*(16 + cant_espacios + (len(LETRAS_USADAS)*2)) + "╝")
    print()


def imprimir_atajos_de_teclado():
    print('[Letras de la A a la Z, "ESC" = Salir, "TAB" = Reiniciar juego]\r\n')


def obtener_tecleada_valida():
    tecleada_valida = False
    CARACTERES_VALIDOS = 'abcdefghijklmnñopqrstuvwxyz'
    CARACTERES_ESPECIALES_VALIDOS = ['\x1b', '\t'] # [ESC, TAB]
    ch = ''

    while not tecleada_valida:
        try:
            keystroke = msvcrt.getch()
            if keystroke in [b'\xe0', b'\000']:
                keystroke = msvcrt.getch()
            else:
                ch = keystroke.decode('utf-8')

            if ch in CARACTERES_ESPECIALES_VALIDOS or ch in CARACTERES_VALIDOS or ch in CARACTERES_VALIDOS.upper():
                tecleada_valida = True
        except:
            tecleada_valida = False
    return ch


def procesar_entrada_usuario():
    print('Ingresa una letra u opción: ' + ULTIMA_TECLA, end='')
    sys.stdout.flush()
    return obtener_tecleada_valida()


def reiniciar_juego():
    global PALABRA_OCULTA
    global OPORTUNIDADES
    global PALABRA_IMPRIMIBLE
    global ADIVINASTE
    PALABRA_OCULTA = seleccionar_nueva_palabra()
    LETRAS_USADAS.clear()
    PALABRA_IMPRIMIBLE = '_' * len(PALABRA_OCULTA)
    OPORTUNIDADES = 6
    ADIVINASTE = False

def normalizar_tildes(palabra):
    palabra = palabra.upper()
    palabra = palabra.replace('Á', 'A')
    palabra = palabra.replace('É', 'E')
    palabra = palabra.replace('Í', 'I')
    palabra = palabra.replace('Ó', 'O')
    palabra = palabra.replace('Ú', 'U')
    return palabra

def ejecutar():
    global ULTIMA_TECLA
    global PALABRA_IMPRIMIBLE
    global OPORTUNIDADES
    global ADIVINASTE

    if cargar_palabras():
        salir = False
        reiniciar_juego()

        while not salir:
            imprimir_interfaz()
            tecla = procesar_entrada_usuario()
            if tecla == '\x1b':
                salir = True
            elif tecla == '\t':
                reiniciar_juego()
            else:
                ULTIMA_TECLA = tecla.upper()
                if not ADIVINASTE and OPORTUNIDADES > 0:
                    if tecla.upper() in normalizar_tildes(PALABRA_OCULTA):
                        for posletra in range(len(PALABRA_OCULTA)):
                            if normalizar_tildes(PALABRA_OCULTA[posletra]) == tecla.upper():
                                PALABRA_IMPRIMIBLE = PALABRA_IMPRIMIBLE[:posletra] + PALABRA_OCULTA[posletra].upper() + PALABRA_IMPRIMIBLE[posletra + 1:]
                        ADIVINASTE = len(list(filter(lambda x: x == "_", PALABRA_IMPRIMIBLE))) == 0
                    else:
                        if tecla.upper() not in LETRAS_USADAS:
                            LETRAS_USADAS.append(tecla.upper())
                            OPORTUNIDADES -= 1


if __name__ == '__main__':
    ejecutar()
