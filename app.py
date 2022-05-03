# cargamos el modelo de huggingsound
import re
import unidecode
from huggingsound import SpeechRecognitionModel
from models.model import *
from models.plantillas_codigo import *
from models.variables_globales import *


# creación del modelo
model = SpeechRecognitionModel("patrickvonplaten/wav2vec2-large-xlsr-53-spanish-with-lm")

# Variables globales
bloque = '' # Define el contexto (si es función, condicional, ciclo, etc.)
codigo = None # Guarda el código hasta el momento
indentacion = 0 # Nivel de indentación
linea_codigo = 0 # Esto para dar seguimiento al eliminado de una linea
recomendacion = ""

import gradio as gr

def transcribe(audio, state=""):
    global bloque
    global codigo
    

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

inputs = gr.inputs.Audio(label="Dar click para escuchar tu voz", type="filepath", source="microphone")
output1 = gr.outputs.Textbox(label="Asi se ve tu código")
output2 = gr.outputs.Textbox(label="Transcripción en español de la última línea de código")

title = "Expresate con voz"
description = "<h1>Hola</h1> Aplicación que ayuda a programar a traves de tu voz"
# ,'mientras variable alpha es menor igual a numero dos'
# ,'Definir variable con nombre india igual a numero uno'
examples = [
            'definir función con nombre magica y parámetros x y z'
            'mientras variable india es menor o igual a  seis',
            'ejecuta print con argumentos variable india producto cadena o cadena','Asignar variable india con india mas uno',
            './grabaciones-wav/codigo_o/Audios demo while/definir_func_avitua.wav',
            './grabaciones-wav/codigo_o/Audios demo while/linea1_avitua.wav',
            './grabaciones-wav/codigo_o/Audios demo while/linea2_avitua.wav',
            './grabaciones-wav/codigo_o/Audios demo while/linea3_avitua.wav',
            './grabaciones-wav/codigo_o/Audios demo while/linea4_avitua.wav',
            './grabaciones-wav/codigo_o/Audios demo while/fin_bloque_avitua.wav',
            ]

article = "<a  style='color:#eb9f59;' href = 'https://github.com/gandres-dev/Hackaton-Common-Voice'> Repositorio de la app"
demo = gr.Interface(fn=transcribe, inputs=inputs, outputs=[output1,output2],
                    title=title, description=description, article=article,
                    allow_flagging="never", theme="darkpeach", examples=examples,
                    # live=True
                    )

if __name__ == "__main__":
    demo.launch()