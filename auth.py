import hashlib

def verificar_contraseña(contraseña_ingresada, hash_almacenado):
    # Hashear la contraseña ingresada y compararla con el hash almacenado
    return hashlib.sha256(contraseña_ingresada.encode()).hexdigest() == hash_almacenado

def generar_hash(contraseña):
    # Generar un hash SHA-256 de la contraseña
    return hashlib.sha256(contraseña.encode()).hexdigest()