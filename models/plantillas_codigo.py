import re

def crear_funcion(instruccion):
    """
    Crea el template de la estructura de una función

    Parametros
    ----------
    instrucion: str
        La intruccion de voz en texto.

    Regresa
    ---------
    output: str
        Codigo generado
    recomendacion: str
        Una sugerencia o fallo
    """

    global indentacion
    global recomendacion
    global bloque

    bloque='funcion'

    # guarda los avisos o recomendaciones que el programa te hace
    recomendacion = ''

    # guarda la línea de código
    output = ''
    
    # pivote que ayuda a definir el nombre de una función
    before_keyword, keyword, after_keyword = instruccion.partition('nombre')

    # verifica que haya o esté escrita la frase "nombre"
    if len(after_keyword) == 0:
        recomendacion = f'¡No me dijiste el nombre de la función!'

    # de otro modo, si tiene nombre la función
    else:

        # obtenemos el nombre de la función por el usuario
        name_func = after_keyword.split(' ')[1]

        # verificamos si no desea poner parametros                                
        if instruccion.strip().split(' ')[-1] == name_func:
            parametros = ''

        # de otro modo, si desea una función con parámetros
        else:
            before_keyword, keyword, after_keyword = instruccion.partition('parametros')

            # verifica que si exista el nombre de los parámetros
            if len(after_keyword) == 0:
                parametros = ''
                recomendacion = f'¡No me dijiste el nombre de los parámetros!'

            # escribe como parámetros todo lo que está después de "parámetros"
            else:
                candidatos = []
                cadena_separada = after_keyword.strip().split(' ')

                for palabra in cadena_separada:
                    try:
                        candidatos.append(diccionario_fonetico[palabra])
                    except:
                        continue
                
                if len(candidatos) == 0:
                    parametros = after_keyword.split(' ')[1:]
                    parametros = ', '.join(parametros)

                else:
                    parametros = ', '.join(candidatos)

        # indenta aunque marque que detecte que no le dije parámetros
        if not recomendacion or recomendacion == '¡No me dijiste el nombre de los parámetros!':
            indentacion += 1

        # concatenación del nombre y parámetros de la función
        output = f'def {name_func}({parametros}):\n' + '\t' * indentacion + '|'
    return output



def encontrar_palabras(transcript,cjto_palabras):

    """
    Toma un string (en minúsculos) y un conjunto de palabras. Busca el primer match
    de cjto_palabras en transcript y particiona el string

    Parametros
    ----------
    transcript: str
        La intruccion de voz en texto ya en minúsculas.
    cjto_palabras: list(str)
        Lista de strings donde se comienza a dividir el transcript original

    Regresa
    ---------
    output: list(str)
        [antes_palabra,palabra,despues_palabra]

        antes_palabra: string que está antes de la palabra de interés (de cjto_palabras)
        palabra: string que da la palabra clave donde dividimos
        despues_palabra: string que está después de la palabra
    
    Ejemplo
    --------
    encontrar_palabras('variable india producto variable alfa',['producto','suma','menos','entre'])
    >> ['variable india','producto',' variable alfa]
    """ 
    inicio,final=list(re.finditer(r'|'.join(cjto_palabras),transcript))[0].span()
    antes_palabra=transcript[:inicio].strip()
    despues_palabra=transcript[final:].strip()
    palabra=transcript[inicio:final]
    return antes_palabra,palabra,despues_palabra



def crear_condicional(transcript):
    ''' 
    Toma el transcript de un enunciado condicional y regresa su traducción a código en Python

    Parametros
    ----------
    transcript: str
        La intruccion de voz en texto ya en minúsculas.


    Regresa
    ---------
    output: str
        Cadena con el código en python, tiene una línea al final y un pipe 
        que representa el prompt donde se seguirá escribiendo
    
    Ejemplo
    --------
    crear_condicional('mientras variable india sea menor igual a numero seis')
    >> while (i<=6):
    >>      |
    '''    
    global indentacion
    global bloque

    keyword_mapeo={'mientras':'while','si':'if','contrario':'else'}
    antes_keyword,keyword,desp_keyword=encontrar_palabras(transcript,keyword_mapeo.keys())
    cadena=keyword_mapeo[keyword]
    bloque = keyword

    if cadena=='else':
        indentacion=indentacion+1
        return 'else:'+'\n' +'\t'* indentacion+'|'

    # Primera división
    condicional_mapeo={'menor estricto':'<','menor o igual':'<=','igual':'==','diferente':'!='
    ,'mayor estricto':'>','mayor o igual':'>='}
    cjto_condicional=condicional_mapeo.keys()
    antes_condicional,palabra_condicional,despues_condicional=encontrar_palabras(transcript,cjto_condicional) 
    
    
    # Buscar antes en la lista de variables
    a_var,var,d_var=encontrar_palabras(antes_condicional,['variable'])
    nombre_var=d_var.split(' ')[0]

    if diccionario_fonetico.get(nombre_var,False):
        nombre_var=diccionario_fonetico[nombre_var]


    cadena+=' '+nombre_var+' ' +condicional_mapeo[palabra_condicional]

    # Buscar en despues_condicional el número 

    valor=despues_condicional.split(' ')[-1]

    if dict_numeros.get(valor,False):
        valor=str(dict_numeros[valor])

    indentacion+=1

    return f'{keyword_mapeo[keyword]} {nombre_var} {condicional_mapeo[palabra_condicional]} {valor}:'+'\n' +'\t'* indentacion+'|'



def crear_cadena(transcript):
    """
    Toma el transcript de un enunciado que contiene una cadena y regresa el código en Python.
    Para usarse cuando ya se sabe que transcript sólo es los límites de la cadena

    Parametros
    ----------
    transcript: str
        La intruccion de voz en texto ya en minúsculas.


    Regresa
    ---------
    output: list(str)
        antes_palabra:parte del transcript que va antes de las comillas
        palabra: Cadena con el código en python de las comillas y lo que está adentro
        despues_palabra:parte del transcript que va antes de las comillas
    
    Ejemplo
    --------
    crear_cadena('ejecuta print con argumentos variable India producto cadena guion cadena')[1]
    >> ['ejecuta print con argumentos variable India producto','"guion"','']
    """
    try:
        inicio,final = list(re.finditer(r"cadena (.+) cadena",transcript))[0].span()
    except:
        return ''
    antes_palabra = transcript[:inicio].strip()
    despues_palabra = transcript[final:].strip()
    palabra = list(re.finditer(r"cadena (.+) cadena", transcript))[0].group(1)
    return antes_palabra, f'"{palabra}"', despues_palabra



def crear_var_existente(transcript):
    """
    Toma el transcript de un enunciado que contiene la mención de una variable
     y devuelve dicha variable

    Parametros
    ----------
    transcript: str
        La intruccion de voz en texto ya en minúsculas.


    Regresa
    ---------
    output: str
        palabra: Cadena con el código en python del nombre de la variable
    
    Ejemplo
    --------
    crear_var_existente('ejecuta print con argumentos variable india producto cadena guión cadena')
    >> i
    """
    try:
        antes_var,var,desp_var=encontrar_palabras(transcript,['variable'])
    except:
        return '' 

    nombre_var=desp_var.split(' ')[0]
    if diccionario_fonetico.get(nombre_var,False):
        nombre_var=diccionario_fonetico[nombre_var]
    
    return nombre_var



def crear_operacion(transcript):
    '''
    Toma el transcript de una operación binaria y la traduce a código de Python.
    Para traducir las variables que se usan en la operación binaria busca 
    si son cadenas o sólo menciones de variables usando las funciones
    crear_cadena y crear_var_existente

    Parametros
    ----------
    transcript: str
        La intruccion de voz en texto ya en minúsculas.


    Regresa
    ---------
    output: str
        Cadena con el código en python
    
    Ejemplo
    --------
    crear_operacion('variable India producto cadena guión cadena')
    >> i*'-'
    '''
    global dict_operaciones
    

    try:
        antes_op,op,desp_op=encontrar_palabras(transcript,dict_operaciones.keys())
    except:
        return '' 

    # Buscamos la información en la cadena detrás del operador
    cadena_izq=crear_var_existente(antes_op)
    try:
        cadena_izq+=f'{crear_cadena(antes_op)[1]}'
    except:
        cadena_izq+=''
        
    if len(cadena_izq)==0:
        nombre_var=antes_op.split(' ')[-1]
        if dict_numeros.get(nombre_var,False):
            nombre_var=dict_numeros[nombre_var]
        cadena_izq+=str(nombre_var)
        
    # Buscamos la información en la cadena después del operador
    cadena_der=crear_var_existente(desp_op)
    try:
        cadena_der+=f'{crear_cadena(desp_op)[1]}'
    except:
        cadena_der+=''
    
    if len(cadena_der)==0:
        nombre_var=desp_op.split(' ')[0]
        if dict_numeros.get(nombre_var,False):
            nombre_var=dict_numeros[nombre_var]
        if diccionario_fonetico.get(nombre_var,False):
            nombre_var=diccionario_fonetico[nombre_var]
        cadena_der+=str(nombre_var)

                
    return f'{cadena_izq} {dict_operaciones[op]} {cadena_der}'



def crear_llamada(transcript):
    """
    Toma el transcript de la llamada de una función y la convierte en código de Python
        Hace uso de las funciones que detectan operaciones, variables y comillas
        ,para cada argumento de la función

    Parametros
    ----------
    transcript: str
        La intruccion de voz en texto ya en minúsculas.


    Regresa
    ---------
    output: str
        Cadena con el código en python
    
    Ejemplo
    --------
    crear_llamada(ejecuta print con argumentos variable India producto cadena guión cadena 
                    coma cadena hola cadena')
    >> print(i*'-','hola')
    
    """
    global bloque
    global indentacion

    bloque='llamada'
    try:
        antes_ej,ej,desp_ej=encontrar_palabras(transcript,['ejecuta'])
    except:
        return ''
    funcion_nombre=desp_ej.split(' ')[0]
    # Aquí tal vez valdría la pena tener un registro de las funciones previamente definidas para
    # poder buscar en un directorio con Jaccard y no aproximar

    antes_arg,keyword,desp_arg=encontrar_palabras(desp_ej,['argumentos','parametros'])

    argumentos=desp_arg.split('coma')
    lista_cadenas=[]
    for arg in argumentos:
        arg=arg.strip()
        cadena_arg=''
        # print('arg',arg)
        # Caso cuando es operacion
        cadena_op=crear_operacion(arg)
        cadena_var=crear_var_existente(arg)
        cadena_cadena=crear_cadena(arg)
        if len(cadena_op)!=0:
            lista_cadenas.append(cadena_op)
        elif len(cadena_var)!=0:
            lista_cadenas.append(cadena_var)
        elif len(cadena_cadena)!=0:
            lista_cadenas.append(cadena_cadena[1])
        else:
            nombre_var=arg
            if dict_numeros.get(nombre_var,False):
                nombre_var=str(dict_numeros[nombre_var])
                
            lista_cadenas.append(nombre_var)

        # Caso cuando es variable
    
    cadena_final=','.join(lista_cadenas)
    cadena=f'{funcion_nombre}({cadena_final})\n'+'\t'*indentacion+'|'

    return cadena



def crear_regresa(transcript):
    antes_reg,reg,desp_reg=encontrar_palabras(transcript,['regresa'])

    arg=desp_reg.strip()
    cadena_arg=''

    # Si es llamada
    cadena_llamada=crear_llamada(arg)
    # Caso cuando es operacion
    cadena_op=crear_operacion(arg)
    cadena_var=crear_var_existente(arg)
    cadena_cadena=crear_cadena(arg)
    
    cadena_final=''
    if len(cadena_llamada)!=0:
        cadena_final+=cadena_llamada[:-2]
    elif len(cadena_op)!=0:
        cadena_final+=cadena_op
    elif len(cadena_var)!=0:
        cadena_final+=cadena_var
    elif len(cadena_cadena)!=0:
        cadena_final+=cadena_cadena[1]
    else:
        nombre_var=arg
        if dict_numeros.get(nombre_var,False):
            nombre_var=str(dict_numeros[nombre_var])
            
        cadena_final+=nombre_var
    global indentacion
    indentacion-=1
    return f'return {cadena_final}\n'+'\t'*indentacion+'|'



def crear_variable(instruccion):
    """
    Estructura:
    definir variable con nombre [nombre_variable] igual a /*objeto_basico* valor/ 

    Parametros
    ----------
    instrucion: str
        La intruccion de voz en texto.

    Regresa
    ---------
    output: str
        Codigo generado
    recomendacion: str
        Una sugerencia o fallo

    Testing
    -------
    >>> definir variable con nombre india igual a numero uno
    >>> definir variable con nombre i igual a numero 1 (int)
    >>> definir variable con nombre i igual a flotante tres punto cinco (float) 
    >>> definir variable con nombre i igual a cadena hola (string) 
    >>> definir variable con nombre i igual a lista/dic (string)   
    """     
    global indentacion
    global bloque

    bloque='variable'

    # pivote que ayuda a definir el nombre de la variable
    before_keyword, keyword, after_keyword = instruccion.partition('nombre')
    after_keyword_list = after_keyword.strip().split(' ')
    # [india igual a numero uno]
    name_variable = after_keyword_list[0]
    
    # Como sabemos que despues del nombre va seguido de "igual a"
    tipo_dato = after_keyword_list[3]        
    #print(after_keyword_list[4:]) -> lista
    valor = tipos_datos[tipo_dato](after_keyword_list[4:])        
    
    # Verificamos si es una palabra fonetica
    if diccionario_fonetico.get(name_variable,False):
        name_variable=diccionario_fonetico[name_variable] 

    codigo_generado = f'{name_variable} = {valor}\n'+ '\t' * indentacion + '|'
    return codigo_generado



def asignar_variable(instruccion):
    """    
    Asigna una variable (eg. indio = indio + 1)

    Parametros
    ----------
    instrucion: str
        La intruccion de voz en texto.

    Regresa
    ---------
    output: str
        Codigo generado (indio = indio + 1)
    
    Testing
    --------
    >>>'asignar variable india con india suma uno',
    >>>'asignar variable contador con contador menos uno',
    >>>'asignar variable contador con alfa',
    >>>'asignar variable india con india',
    
    """ 
   
    before_keyword, keyword, after_keyword = instruccion.partition('variable')
    after_keyword_list = after_keyword.strip().split(' ')
    name_variable = after_keyword_list[0]
    start = after_keyword_list.index('con') + 1
    operacion = after_keyword_list[start:]
    if len(operacion) != 1:
        operacion_str = crear_operacion(keyword + ' ' + ' '.join(operacion))
    else:
        operacion_str = operacion[0]
        # Verificamos si es una palabra fonetica para lado derecho de la 
        # asignacion
        if diccionario_fonetico.get(operacion_str,False):
            operacion_str=diccionario_fonetico[operacion_str] 

    # Verificamos si es una palabra fonetica
    if diccionario_fonetico.get(name_variable,False):
        name_variable=diccionario_fonetico[name_variable] 

    codigo_generado = f'{name_variable} = {operacion_str}\n'+ '\t' * indentacion + '|'
    return codigo_generado



def crear_for(instruccion):
    """
    Crea el template de la estructura de un ciclo for.

    Parámetros
    ----------
    instrucción: str
        La intrucción de voz en texto.

    Regresa
    ---------
    output: str
        Estructura del ciclo for
    recomendacion: str
        Una sugerencia o error
    """
    global bloque 
    global indentacion
    global recomendacion

    bloque='for'
    vocabulario_basico = ['iteracion', 'rango']

    # verificamos si la frase cumple los requisitos
    instruccion_tokens = instruccion.strip().split(' ')

    for i in vocabulario_basico:
        try:
            instruccion_tokens.index(i)
        except:
            recomendacion = 'Parece que quieres una iteración pero no reconozco tus comandos, inténtalo de nuevo'
            return f'', recomendacion

    # guarda los avisos o recomendaciones que el programa te hace
    recomendacion = ''

    # guarda la línea de código
    output = ''
    
    # pivote que ayuda a definir el rango e iterador
    before_keyword, keyword, after_keyword = instruccion.partition('iteracion')

    if after_keyword.strip().split(' ')[1] in diccionario_fonetico:
        iterador = diccionario_fonetico[after_keyword.strip().split(' ')[1]]

    else:
        iterador = after_keyword.strip().split(' ')[1]

    before_keyword, keyword, after_keyword = instruccion.partition('rango')

    limites = []


    for i, item in enumerate(after_keyword.strip().split(' ')):
        try:
            limites.append(dict_numeros[item])
        except:
            continue

    if len(limites) == 0:
        for i, item in enumerate(after_keyword.strip().split(' ')):
            try:
                limites.append(diccionario_fonetico[item])
            except:
                continue
    
    indentacion += 1

    if len(limites) == 0:
        return f'', 'No encontré los límites del rango, vuelve a intentarlo'

    elif len(limites) == 1:
        return f'for {iterador} in range({limites[-1]}):\n' + '\t' * indentacion + '|'

    elif len(limites) == 2:
        return f'for {iterador} in range({limites[0]}, {limites[1]}):\n' + '\t' * indentacion + '|'

    elif len(limites) >= 2:
        recomendacion = 'Me dictaste más de un número en el rango pero tomé los dos primeros'
        return f'for {iterador} in range({limites[0]}, {limites[1]}):\n' + '\t' * indentacion + '|'



def crear_comentario(instruccion):
    """
    Agrega el comentario de la intrucción en una línea de código

    Parámetros
    ----------
    instrucción: str
        La intrucción de voz en texto.

    Regresa
    ---------
    output: str
        Comentario
    """

    global bloque 
    global indentacion

    # guarda los avisos o recomendaciones que el programa te hace
    recomendacion = ''

    # guarda la línea de código
    output = ''

    before_keyword, keyword, after_keyword = instruccion.partition('comentario')

    return '# ' + after_keyword + '\n' + '\t' * indentacion + '|'



def fin_de_bloque(transcripcion):
    """
    Función auxiliar que es llamada por otras funciones.
    """

    global indentacion
    global bloque

    bloque = 'fin'
    indentacion = indentacion - 1

    return ''