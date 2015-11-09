import hashlib

def hash_email(email):
    sha = hashlib.sha256()
    sha.update(bytearray(email, 'utf-8'))
    return sha.hexdigest()
