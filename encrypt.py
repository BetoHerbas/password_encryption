import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


def generar_clave(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    clave = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return clave


def encriptar(datos, clave):
    f = Fernet(clave)
    return f.encrypt(datos.encode())


def desencriptar(datos_encriptados, clave):
    f = Fernet(clave)
    return f.decrypt(datos_encriptados).decode()


def guardar_contraseñas(contraseñas, salt, archivo="contraseñas.json"):
    datos = {
        "salt": salt.hex(),  # Guardar la sal en formato hexadecimal
        "contraseñas": contraseñas
    }
    try:
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)  # Usar indent=4 para formato legible
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")


def cargar_contraseñas(archivo="contraseñas.json"):
    try:
        with open(archivo, "r") as f:
            contenido = f.read()
            if not contenido:  
                return None, {}
            datos = json.loads(contenido)
            salt = bytes.fromhex(datos["salt"])  
            return salt, datos["contraseñas"]
    except FileNotFoundError:
        return None, {}
    except json.JSONDecodeError:
        return None, {}