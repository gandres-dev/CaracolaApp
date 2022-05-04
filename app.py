# cargamos el modelo de huggingsound
import re
import unidecode
from huggingsound import SpeechRecognitionModel
from models.model import *
from models.plantillas_codigo import *
from models.variables_globales import *


# creación del modelo
model = SpeechRecognitionModel("patrickvonplaten/wav2vec2-large-xlsr-53-spanish-with-lm")



tabla='''
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-r31x{color:#ffffff;text-align:center;vertical-align:top}
.tg .tg-urxo{border-color:#ffffff;color:#ffffff;text-align:center;vertical-align:top}
.tg .tg-iejp{border-color:#ffffff;color:#ffffff;font-weight:bold;text-align:center;vertical-align:top}
</style>
<table class="tg">
<thead>
  <tr>
    <th class="tg-iejp">Fonético</th>
    <th class="tg-r31x">andrea</th>
    <th class="tg-r31x">bravo</th>
    <th class="tg-r31x">carlos</th>
    <th class="tg-r31x">delta</th>
    <th class="tg-r31x">eduardo</th>
    <th class="tg-r31x">fernando</th>
    <th class="tg-r31x">garcia</th>
    <th class="tg-r31x">hotel</th>
    <th class="tg-r31x">india</th>
    <th class="tg-r31x">julieta</th>
    <th class="tg-r31x">kilo</th>
    <th class="tg-r31x">lima</th>
    <th class="tg-r31x">miguel</th>
    <th class="tg-r31x">noviembre</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-iejp">Letra</td>
    <td class="tg-r31x">a</td>
    <td class="tg-r31x">b</td>
    <td class="tg-r31x">c</td>
    <td class="tg-r31x">d</td>
    <td class="tg-r31x">e</td>
    <td class="tg-r31x">f</td>
    <td class="tg-r31x">g</td>
    <td class="tg-r31x">h</td>
    <td class="tg-r31x">i</td>
    <td class="tg-r31x">j</td>
    <td class="tg-r31x">k</td>
    <td class="tg-r31x">l</td>
    <td class="tg-r31x">m</td>
    <td class="tg-r31x">n</td>
  </tr>
  <tr>
    <td class="tg-urxo"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
  </tr>
  <tr>
    <td class="tg-iejp">Fonético</td>
    <td class="tg-r31x">oscar</td>
    <td class="tg-r31x">papa</td>
    <td class="tg-r31x">queretaro</td>
    <td class="tg-r31x">romero</td>
    <td class="tg-r31x">sierra</td>
    <td class="tg-r31x">tango</td>
    <td class="tg-r31x">uniforme</td>
    <td class="tg-r31x">victor</td>
    <td class="tg-r31x">waffle</td>
    <td class="tg-r31x">equis</td>
    <td class="tg-r31x">yarda</td>
    <td class="tg-r31x">zapato</td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
  </tr>
  <tr>
    <td class="tg-iejp">Letra</td>
    <td class="tg-r31x">o</td>
    <td class="tg-r31x">p</td>
    <td class="tg-r31x">q</td>
    <td class="tg-r31x">r</td>
    <td class="tg-r31x">s</td>
    <td class="tg-r31x">t</td>
    <td class="tg-r31x">u</td>
    <td class="tg-r31x">v</td>
    <td class="tg-r31x">w</td>
    <td class="tg-r31x">x</td>
    <td class="tg-r31x">y</td>
    <td class="tg-r31x">z</td>
    <td class="tg-r31x"></td>
    <td class="tg-r31x"></td>
  </tr>
</tbody>
</table>
'''


# Variables globales
bloque = '' # Define el contexto (si es función, condicional, ciclo, etc.)
codigo = None # Guarda el código hasta el momento
indentacion = 0 # Nivel de indentación
linea_codigo = 0 # Esto para dar seguimiento al eliminado de una linea
recomendacion = ""
# fin_de_bloque=False

import gradio as gr

def transcribe(audio, Español, Codigo_Python):
    global bloque
    global codigo
    global indentacion

    transcriptions_es = model.transcribe([audio])[0]
    # quitamos el acento de la transcripcion
    frase = unidecode.unidecode(transcriptions_es['transcription']).lower()
    
    # print(frase)
    if not bloque:
        # Significa que es la primera vez
        codigo = main(frase)        
    else:        
        codigo = agregar_adentro(codigo, frase)
            
    return codigo, frase

inputs = gr.inputs.Audio(label="Dar click para grabar tu voz", type="filepath", source="microphone")
output1 = gr.outputs.Textbox(label="Asi se ve tu código")
output2 = gr.outputs.Textbox(label="Lo que entendió la caracola fue:")

title = "Caracola App"
description = '<p style="color:white">Aplicación que ayuda a programar a traves de tu voz.\nSe usa el siguiente diccionario fonético para capturar las variables de una letra.</p>'+tabla+'<br> <h3 style="color:white"> Instrucciones </h3> <p style="color:white"> Selecciona uno de los ejemplos y da click en enviar para convertir comandos de voz en código! </p>'
# ,'mientras variable alpha es menor igual a numero dos'
# ,'Definir variable con nombre india igual a numero uno'
input2 = gr.inputs.Textbox(lines=0, placeholder="Aqui aparece el texto en español de los ejemplos")
input3 = gr.inputs.Textbox(lines=0, placeholder="Aqui aparece el codigo en python de los ejemplos")

output_html = gr.outputs.HTML(label='Asi se ve tu código:')

examples = [
            ['../wav/comentario.wav','agregar comentario mi primer función', '# mi primer funcion'],
            ['../wav/funcion.wav','definir función con nombre mágica y parámetros noviembre', 'def magica(n):'],    
            ['../wav/definira.wav','definir variable con nombre andrea igual a natural cero', 'a=0'],
            ['../wav/definirb.wav','definir variable con nombre bravo igual a natural uno', 'b = 1'],
            ['../wav/iteracion.wav','ejecuta iteracion para india en un rango noviembre', 'for i in range(n)'],
            ['../wav/asignar_c_b.wav','asignar variable carlos con bravo', 'c=b'],
            ['../wav/andreabravo.wav','asignar variable bravo con andrea mas bravo', 'b = a + b'],
            ['../wav/asignar_a_c.wav','asignar variable andrea con carlos', 'a=c'],
            ['../wav/terminar_bloque.wav','terminar bloque',''],
            ['../wav/comentario2.wav','agregar comentario fin de ciclo', '# fin de ciclo'],
            ['../wav/regresa.wav','regresa variable andrea', 'return a'],
            ['../wav/llamada.wav', 'ejecuta mágica con argumentos diez', 'magica(10)']
            ]            
          
article = "<a  style='color:#eb9f59;' href = 'https://github.com/gandres-dev/Hackaton-Common-Voice'> Repositorio de la app"
demo = gr.Interface(fn=transcribe, inputs=[inputs, input2, input3], outputs=[output_html,output2],
                    examples=examples,
                    title=title, description=description, article=article,
                    allow_flagging="never", theme="darkpeach",
                    )

demo.launch()