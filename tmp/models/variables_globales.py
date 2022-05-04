def numero(text):
    """Convierte un texto de numero en numero entero (int)    

    Parametros
    ----------
    text: list
        Serie de valores

    Regresa
    ---------
    dict_numeros: int
        El número correspondiente
    """
    global dict_numeros    
    # Como sabemos que siempre sera el primer elemento el valor despues
    # de número (eg. cuatro or veintecinco)
    numero_str = text[0]           
    return dict_numeros[numero_str]

def flotante(text): 
    """Convierte un texto de numero en numero floatante (float)    

    Parametros
    ----------
    text: list
        Serie de valores

    Regresa
    ---------
    dict_numeros: float
        El número correspondiente en floatante (eg 3.4)
    """
    global dict_numeros
    text = " ".join(text)
    before_keyword, keyword, after_keyword = text.partition('punto')
    print(before_keyword)
    print(after_keyword)

    # Obtenemos los dos numeros antes y despues del punto
    before_num = before_keyword.strip().split(' ')[0]
    after_num = after_keyword.strip().split(' ')[0]
    
    # Hacemos el mapeo uno -> 1
    num1_int = dict_numeros[before_num]
    num2_int = dict_numeros[after_num]        
    
    return float(str(num1_int) + '.' + str(num2_int))

def cadena(text):
    """Convierte un texto de numero en string (str)    

    Parametros
    ----------
    text: list
        Serie de valores

    Regresa
    ---------
    string: str
        Una cadena con el contenido del texto
    """    
    numero_str = text[:]                   
    return ' '.join(text)

def lista(text):
    """Convierte un texto de numero en string (str)    

    Parametros
    ----------
    text: list
        Serie de valores

    Regresa
    ---------
    lista: list
        Una lista vacia
    """
    return []


diccionario_fonetico={'alfa':'a',
                    'bravo':'b',
                    'carlos':'c',
                    'delta':'d',
                    'eduardo':'e',
                    'fernando':'f',
                    'garcia':'g',
                    'hotel':'h',
                    'india':'i',
                    'julieta':'j',
                    'kilo':'k',
                    'lima':'l',
                    'miguel':'m',
                    'noviembre':'n',
                    'oscar':'o',
                    'papa':'p',
                    'queretaro':'q',
                    'romero':'',
                    'sierra':'s',
                    'tango':'t',
                    'uniforme':'u',
                    'victor':'v',
                    'wafle':'w',
                    'equis':'x',
                    'yarda':'y',
                    'llarda':'y',
                    'espacio':' '}

# Separa en operadores comunes

# si esto se lematiza puedes agarrar todas las frases de la forma suma, sumar, etc.
dict_operaciones={
    'producto':'*','mas':'+','menos':'-','concatena':'+','entre':'/','modulo':'%'
    } 

dict_numeros = {
    'cero':0,
    'uno': 1,
    'dos': 2,
    'tres': 3,
    'cuatro':4,
    'cinco': 5,
    'seis': 6,
    'siete': 7,
    'ocho': 8,
    'nueve': 9,
    'diez': 10,
    'once': 11,
    'doce': 12,
    'trece': 13,
    'catorce': 14,
    'quince': 15,
    'dieciseis': 16,
    'diecisiete': 17,
    'dieciocho': 18,
    'diecinueve': 19,
    'veinte': 20,
    'treinta': 30,
    'cuarenta': 40,
    'cicuenta': 50,
}
    
# Diccionario de funciones
tipos_datos ={
    'numero': numero,
    'flotante': flotante,
    'cadena': cadena,
    'lista': lista,
}    