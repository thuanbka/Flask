import hashlib

def sha256_encode(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_string = sha256_hash.hexdigest()
    return hashed_string
