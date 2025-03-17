import json

def guardar_contraseñas(contraseñas, archivo="contraseñas.json"):
    with open(archivo, "w") as f:
        json.dump(contraseñas, f)

def cargar_contraseñas(archivo="contraseñas.json"):
    try:
        with open(archivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}