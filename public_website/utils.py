from hashlib import sha256

def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()