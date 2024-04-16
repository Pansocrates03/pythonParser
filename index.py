
# Actividad 3.2: Resaltador de sintaxis
# Basado en el código originario del Dr. Santiago Conant
# Autor: Esteban Sierra Baccio
# Ultima modificacion: 16 de Abril del 2024

"""
Ejemplos funcionales del lenguaje

atomo 25 #t “hola amigo” $

((1 2)(#f #t)) es una “lista anidada” $

(define (prueba x)
    (if (equal x 10)
    (display “x igual a 10”)
    (display “x diferente de 10”))) $

"""

import sys

################################ PARTE 1: EL SCANNER DE TEXTO ################################

# tokens
NUM = 100 # Número
IDE = 101 # Identificador
BOO = 102 # Booleano (True o False)
STR = 103 # Cadena de caracteres
LRP = 104 # Delimitador: paréntesis izquierdo
RRP = 105 # Delimitador: paréntesis derecho
END = 106 # Fin de la entrada
ERR = 200 # Error léxico: palabra desconocida


# Matriz de transiciones: codificación del AFD
# [renglón, columna] = [estado no final, transición]
# Estados > 99 son finales (ACEPTORES)
# Caso especial: Estado 200 = ERROR
#      Dig Let  #  t/f  " (    )   $  esp raro
MT = [[  1,  2, 3,  2,  5, 104,105,END, 0,  7], # edo 0 - estado inicial
      [  1,  7, 7,  7,  7,NUM,NUM,END,NUM,  7], # edo 1 - digito
      [  7,  2, 7,  2,  7,  7,IDE,END,IDE,  7], # edo 2 - Identificador
      [  7,  7, 7,  4,  7,  7,  7,  7,  7,  7], # edo 3 - definicion de booleano
      [  7,  7, 7,  7,  7,  7,BOO,  7,BOO,  7], # edo 4 - booleano
      [  5,  5, 5,  5,  6,  5,  5,  5,  5,  7], # edo 5 - definicion de cadena
      [  7,  7, 7,  7,  7,  7,STR,  7,STR,  7], # edo 6 - cadena
      [  7,  7, 7,  7,  7,  7,  7,  7,ERR,ERR]] # edo 7 - Estado de error 


# Filtro de caracteres: regresa el número de columna de la matriz de transiciones
# de acuerdo al caracter dado

digitos = ["0","1","2","3","4","5","6","7","8","9"]
letras = ["_","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
operadores = ["+","-","*","/"]

def filtro(c):
    """Regresa el número de columna asociado al tipo de caracter dado(c)"""
    if c in digitos: #digitos
        return 0
    elif c == '#':
        return 2
    elif c == 't' or c == 'f':
        return 3
    elif c.lower() in letras:
        return 1
    elif c == '"' or c =='“' or c == '”':
        return 4
    elif c == '(': # delimitador (
        return 5
    elif c == ')': # delimitador )
        return 6
    elif c == '$': # fin de entrada
        return 7
    elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13: # blancos
        return 8
    else: # caracter raro
        return 9

# Función principal: implementa el análisis léxico
def scanner():
    """Implementa un analizador léxico: lee los caracteres de la entrada estándar"""
    edo = 0 # número de estado en el autómata
    lexema = "" # palabra que genera el token
    tokens = []
    code = []
    leer = True # indica si se requiere leer un caracter de la entrada estándar


    while (True):
        while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
            if leer: c = sys.stdin.read(1)
            else: leer = True
            #print("Estado: ", edo)
            #print("Coulmna: ", filtro(c))
            edo = MT[edo][filtro(c)]
            if edo < 100 and edo != 0: lexema += c

        ## Lista de errores
        if edo == NUM:    
            leer = False # ya se leyó el siguiente caracter
            print("Número", lexema)
        elif edo == IDE:   
            leer = False # ya se leyó el siguiente caracter
            print("Identificador", lexema)
        elif edo == BOO:   
            leer = False # ya se leyó el siguiente caracter
            print("Booleano", lexema)
        elif edo == STR:   
            lexema += c  # el último caracter forma el lexema
            print("Cadena", lexema)
        elif edo == LRP:  
            lexema += c  # el último caracter forma el lexema
            print("Delimitador", lexema)
        elif edo == RRP:
            lexema += c # el ultimo carcter forma el lexema
            print("Delimitador" , lexema)
        elif edo == END:
            leer = False
            print("Finalizacion", lexema)
        elif edo == ERR:   
            leer = False # el último caracter no es raro
            print("ERROR! palabra ilegal", lexema)
        tokens.append(edo)
        code.append(lexema)
        if edo == END:
            res = {
                "tokenList": tokens,
                "valueList": code
            }
            return res
        lexema = ""
        edo = 0
        
global tokens
tokens = scanner()
tokens.get("valueList")[-1] = "$"

global token_pos
token_pos = 0

print(tokens)


################################ PARTE 2: PARSEADOR ################################



def match(tokenEsperado):
    global tokens
    global token_pos
    if tokens.get("tokenList")[token_pos] == tokenEsperado:
        ##print('Se ha recibido el token ' + str(tokenEsperado) )
        token_pos = token_pos + 1
        return True
    else:
        #print('Se ha recibido el token ' + str(tokens[token_pos]) + ' y se esperaba el token ' + str(tokenEsperado))
        return False
# Checara asignación

def PROG():
    if EXP():
        if PROG():
            return True
    elif match(END):
        return True

def EXP():
    if ATOMO():
        return True
    elif LISTA():
        return True
    
def ATOMO():
    if match(IDE):
        return True
    elif CONSTANTE():
        return True

def CONSTANTE():
    if match(NUM):
        return True
    elif match(BOO):
        return True
    elif match(STR):
        return True
    
def LISTA():
    if match(LRP):
        if ELEMENTOS():
            if match(RRP):
                return True

def ELEMENTOS():
    if EXP():
        if ELEMENTOS():
            return True
    else:
        return True

if PROG(): print("EL texto ingresado es válido")
else: print("El texto ingresado NO es válido")



    #SUPUTAMADRE


################################ PARTE 3: Resaltador de sintaxis ################################

# Esta funcion se encarga de devolver el texto que representa el archivo HTML ya con los colores y todos
def getHtml(res):

    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <style>
        .NUM { color: green; display: inline-block; }
        .IDE { display: inline-block;}
        .BOO { color: purple; display: inline-block;}
        .STR { color: gold; display: inline-block;}
        .END { color: blue; display: inline-block; }
        .LRP { color: red; display: inline-block; }
        .RRP { color: red; display: inline-block; }

    </style>

"""

    index = 0
    for x in res.get("tokenList"):
        texto = res.get("valueList")[index]
        if x == NUM:
            html = html + "<div class='NUM'>" + texto + "</div>"
        if x == IDE:
            html = html + "<div class='IDE'>" + texto + "</div>"
        if x == BOO:
            html = html + "<div class='BOO'>" + texto + "</div>"
        if x == STR:
            html = html + "<div class='STR'>" + texto + "</div>"
        if x == LRP:
            html = html + "<div class='LRP'>" + texto + "</div>"
        if x == RRP:
            html = html + "<div class='RRP'>" + texto + "</div>"
        if x == END:
            html = html + "<div class='END'>" + "$" + "</div>"
        if x == ERR:
            html = html + "<div class='ERR'>" + texto + "</div>"
        html = html + " "

        index = index +1

    html = html + "</body></html>"
    return html

# Esta otra funcion se encarga de crear el archivo de html llamado "res.html"
with open("res.html","w") as file:
    file.write(getHtml(tokens))
    print("Created file at: res.html")
