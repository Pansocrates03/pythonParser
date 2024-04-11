
# Implementación de un scanner mediante la codificación de un Autómata
# Finito Determinista como una Matríz de Transiciones
# Autor: Dr. Santiago Conant, Agosto 2014 (modificado en Agosto 2015)

import sys

# tokens
INT = 100  # Número entero
FLT = 101  # Número de punto flotante
OPB = 102  # Operador binario
LRP = 103  # Delimitador: paréntesis izquierdo
RRP = 104  # Delimitador: paréntesis derecho
END = 105  # Fin de la entrada
COM = 106  # Separador coma ,
IDE = 107  # Identificador
ASI = 108  # Operador de Asignacion
ERR = 200  # Error léxico: palabra desconocida


# Matriz de transiciones: codificación del AFD
# [renglón, columna] = [estado no final, transición]
# Estados > 99 son finales (ACEPTORES)
# Caso especial: Estado 200 = ERROR
#      dig  op  (   ) raro esp  .   $   ,  let asig
MT = [[  1,OPB,LRP,RRP,  4,  0,  4,END,COM, 5, ASI], # edo 0 - estado inicial
      [  1,INT,INT,INT,  4,INT,  2,INT,INT, 4, ASI], # edo 1 - dígitos enteros
      [  3,  4,  4,  4,  4,ERR,  4,  4,  4, 4, ASI], # edo 2 - primer decimal flotante
      [  3,FLT,FLT,FLT,  4,FLT,  4,FLT,FLT, 4, ASI], # edo 3 - decimales restantes flotante
      [  4,  4,  4,  4,  4,ERR,  4,  4,ERR, 4, 4], # edo 4 - estado de error
      [  5,OPB, IDE,IDE,  4,IDE,END,  5,IDE, 5, ASI]] # edo 5 - Identificadores 


# Filtro de caracteres: regresa el número de columna de la matriz de transiciones
# de acuerdo al caracter dado

digitos = ["0","1","2","3","4","5","6","7","8","9"]
letras = ["_","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
operadores = ["+","-","*","/"]

def filtro(c):
    """Regresa el número de columna asociado al tipo de caracter dado(c)"""
    if c in digitos: #digitos
        return 0
    elif c in operadores: # operadores
        return 1
    elif c == '(': # delimitador (
        return 2
    elif c == ')': # delimitador )
        return 3
    elif c == ' ' or ord(c) == 9 or ord(c) == 10 or ord(c) == 13: # blancos
        return 5
    elif c == '.': # punto
        return 6
    elif c == '$': # fin de entrada
        return 7
    elif c == ',': # coma
        return 8
    elif c.lower() in letras:
        return 9
    elif c == "=": # igual
        return 10
    else: # caracter raro
        return 4

# Función principal: implementa el análisis léxico
def scanner():
    """Implementa un analizador léxico: lee los caracteres de la entrada estándar"""
    edo = 0 # número de estado en el autómata
    lexema = "" # palabra que genera el token
    tokens = []
    leer = True # indica si se requiere leer un caracter de la entrada estándar


    while (True):
        while edo < 100:    # mientras el estado no sea ACEPTOR ni ERROR
            if leer: c = sys.stdin.read(1)
            else: leer = True
            edo = MT[edo][filtro(c)]
            if edo < 100 and edo != 0: lexema += c

        ## Lista de errores
        if edo == INT:    
            leer = False # ya se leyó el siguiente caracter
            #print("Entero", lexema)
        elif edo == FLT:   
            leer = False # ya se leyó el siguiente caracter
            #print("Flotante", lexema)
        elif edo == OPB:   
            lexema += c  # el último caracter forma el lexema
            #print("Operador", lexema)
        elif edo == LRP:   
            lexema += c  # el último caracter forma el lexema
            #print("Delimitador", lexema)
        elif edo == RRP:  
            lexema += c  # el último caracter forma el lexema
            #print("Delimitador", lexema)
        elif edo == COM:
            lexema += c # el ultimo carcter forma el lexema
            #print("Separador , ")
        elif edo == IDE:
            leer = False
            #print("Identificador", lexema)
        elif edo == ASI:
            lexema += c # el último caracter forma el lexema
            #print("Asignador", lexema)
        elif edo == ERR:   
            leer = False # el último caracter no es raro
            #print("ERROR! palabra ilegal", lexema)
        tokens.append(edo)
        if edo == END: return tokens
        lexema = ""
        edo = 0
        
global tokens
tokens = scanner()

global token_pos
token_pos = 0

print(tokens)




############################################ PARSEADOR




def match(tokenEsperado):
    global tokens
    global token_pos
    if tokens[token_pos] == tokenEsperado:
        print('Se ha recibido el token ' + str(tokenEsperado) )
        token_pos = token_pos + 1
        return True
    else:
        #print('Se ha recibido el token ' + str(tokens[token_pos]) + ' y se esperaba el token ' + str(tokenEsperado))
        return False
# Checara asignación

def SEN():
    if match(IDE):
        if SEN1():
            if match(END):
                return True

def SEN1():
    if match(ASI):
        if EXP():
            return True
    if match(LRP):
        if ARGS():
            if match(RRP):
                return True

def EXP():
    if match(LRP):
        if EXP():
            if match(104):
                if EXP1():
                    return True
    if match(INT) or match(FLT):
        if EXP1():
            return True
    if match(IDE):
        if ID1():
            if EXP1():
                return True

def EXP1():
    if match(OPB):
        if EXP():
            if EXP1():
                return True
    else: return True

def ID1():
    if match(LRP):
        if ARGS():
            if match(RRP):
                return True
    else: return True

def ARGS():
    if ARGS1():
        return True
    else: return False

def ARGS1():
    if EXP():
        if ARGS2():
            return True

def ARGS2():
    if match(COM):
        if ARGS1():
            return True
    else: return True
        



if SEN():
    print("Efectivamente mi estimado, el texto ingresado es válido")
else:
    print("Desgraciadamente mi estimado, el texto ingresado no es válido")


    #SUPUTAMADRE
