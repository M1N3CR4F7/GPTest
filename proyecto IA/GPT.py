import os
import sys
import datetime
import json
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_log_filename():
    now = datetime.datetime.now()
    return now.strftime("%Y.%m.%d.%H.%M.%S.log")

def initialize_log():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_filename = os.path.join("logs", generate_log_filename())
    log_file = open(log_filename, "w", encoding="utf-8")
    log_file.write(f"Log started at {datetime.datetime.now()}\n")
    return log_file

def load_config():
    default_config = {
        "temperature": 0.7,
        "max_input_length": 50,
        "max_output_length": 100,
        "top_p": 0.9,
        "model_name": "gpt2"
    }
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    else:
        return default_config

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def load_model(model_name):
    print(f"Cargando modelo: {model_name}...")
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.config.pad_token_id = model.config.eos_token_id  # Configurar pad_token_id
    return model, tokenizer

def generate_text(prompt, model, tokenizer, config):
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=config["max_input_length"], truncation=True)
    outputs = model.generate(
        inputs,
        max_length=config["max_output_length"],
        temperature=config["temperature"],
        top_p=config["top_p"],
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def restart_program():
    print("Reiniciando la aplicación...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

def show_menu(config):
    while True:
        print("\nMenú de configuración:")
        print(f"1. Ajustar creatividad (temperature: 0.1-1.0) - Actual: {config['temperature'] * 100:.1f}%")
        print(f"2. Ajustar longitud máxima de entrada - Actual: {config['max_input_length']} tokens")
        print(f"3. Ajustar longitud máxima de salida - Actual: {config['max_output_length']} tokens")
        print(f"4. Ajustar top-p (0.1-1.0) - Actual: {config['top_p'] * 100:.1f}%")
        print(f"5. Cambiar de modelo - Actual: {config['model_name']}")
        print("6. Resetear configuración a valores predeterminados")
        print("7. Salir del menú")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            value = input("Ingresa un valor para la creatividad (0% - 100%): ")
            if value.isdigit():
                config["temperature"] = max(0.1, min(1.0, int(value) / 100))
                print(f"Creatividad ajustada a {config['temperature'] * 100:.1f}%")
            elif value.lower() == "reset":
                config["temperature"] = 0.7
                print("Creatividad reseteada a 70%.")

        elif choice == "2":
            value = input("Ingresa la longitud máxima de entrada en tokens: ")
            if value.isdigit():
                config["max_input_length"] = max(1, int(value))
                print(f"Longitud máxima de entrada ajustada a {config['max_input_length']} tokens")
            elif value.lower() == "reset":
                config["max_input_length"] = 50
                print("Longitud máxima de entrada reseteada a 50 tokens.")

        elif choice == "3":
            value = input("Ingresa la longitud máxima de salida en tokens: ")
            if value.isdigit():
                config["max_output_length"] = max(1, int(value))
                print(f"Longitud máxima de salida ajustada a {config['max_output_length']} tokens")
            elif value.lower() == "reset":
                config["max_output_length"] = 100
                print("Longitud máxima de salida reseteada a 100 tokens.")

        elif choice == "4":
            value = input("Ingresa un valor para top-p (0% - 100%): ")
            if value.isdigit():
                config["top_p"] = max(0.1, min(1.0, int(value) / 100))
                print(f"Top-p ajustado a {config['top_p'] * 100:.1f}%")
            elif value.lower() == "reset":
                config["top_p"] = 0.9
                print("Top-p reseteado a 90%.")

        elif choice == "5":
            print("Modelos disponibles:")
            print("1. gpt2 (Básico y rápido)")
            print("2. gpt2-medium (Equilibrado en tamaño y rendimiento)")
            print("3. gpt2-large (Modelo potente, más coherente, pero más pesado)")
            print("4. gpt2-xl (El modelo más avanzado y pesado)")
            value = input("Selecciona un modelo (número o nombre): ")

            if value in ["1", "2", "3", "4"]:
                models = {"1": "gpt2", "2": "gpt2-medium", "3": "gpt2-large", "4": "gpt2-xl"}
                config["model_name"] = models[value]
            elif value in ["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"]:
                config["model_name"] = value
            else:
                print("Selección inválida.")
                continue

            print(f"Modelo cambiado a {config['model_name']}. Reiniciando...")
            save_config(config)
            restart_program()

        elif choice == "6":
            config.update({
                "temperature": 0.7,
                "max_input_length": 50,
                "max_output_length": 100,
                "top_p": 0.9,
                "model_name": "gpt2"
            })
            print("Configuración reseteada a valores predeterminados.")

        elif choice == "7":
            os.system("cls" if os.name == "nt" else "clear")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")

        save_config(config)

def main():
    config = load_config()
    log_file = initialize_log()

    model, tokenizer = load_model(config["model_name"])

    print("Para más ayuda, di '/?'.")

    while True:
        try:
            prompt = input("Escribe lo que quieres que la IA responda (o 'exit' para terminar): ")
            if prompt.lower() == "exit":
                break

            if prompt == "/?":
                show_menu(config)
                continue

            response = generate_text(prompt, model, tokenizer, config)
            print(f"Respuesta de GPT-2: {response}\n")
            log_file.write(f"Entrada: {prompt}\n")
            log_file.write(f"Respuesta: {response}\n")

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            log_file.write(f"Error: {e}\n")

    log_file.write(f"Log finalizado en {datetime.datetime.now()}\n")
    log_file.close()

if __name__ == "__main__":
    main()
