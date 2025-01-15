import os
from flask import Flask, render_template, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from googletrans import Translator
import torch

# Configuración de la aplicación Flask
app = Flask(__name__)

# Cargar el modelo GPT-2 y el tokenizador
model_name = "gpt2"  # Puedes cambiar a gpt2-medium, gpt2-large, gpt2-xl si lo prefieres
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Traductor
translator = Translator()

# Función para generar la respuesta con la IA
def generate_response(user_input):
    # Tokenizar la entrada del usuario
    input_ids = tokenizer.encode(user_input, return_tensors='pt')

    # Generar la respuesta con el modelo GPT-2
    with torch.no_grad():
        output = model.generate(input_ids, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2, top_p=0.9, temperature=0.7)

    # Decodificar la respuesta
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Traducir la respuesta generada al español
    translated_response = translator.translate(response, src='en', dest='es').text

    return translated_response

# Ruta principal que sirve la página HTML
@app.route('/')
def home():
    return render_template('index.html')  # Asegúrate de tener el archivo index.html en la carpeta templates

# Ruta para recibir los mensajes del chat desde la interfaz
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    
    # Generar la respuesta de la IA
    response = generate_response(user_input)
    
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
