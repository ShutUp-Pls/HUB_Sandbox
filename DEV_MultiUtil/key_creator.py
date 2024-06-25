import hashlib

def crear_hash(passw):
    # Crear un hash de la contraseña
    hash_objeto = hashlib.sha256(passw.encode())
    hash_hex = hash_objeto.hexdigest()
    return hash_hex
