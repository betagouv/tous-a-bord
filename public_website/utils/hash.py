from hashlib import sha256

def hash(input: str):
    return sha256(input.encode('utf-8')).hexdigest()
