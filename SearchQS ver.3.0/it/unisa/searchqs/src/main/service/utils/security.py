import string
import random
import hashlib

PEPPER_HEX = "13pmcWU1ZAjDFi22U6ANycDY0len2k5H"

def generation_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt_password(password, salt_hex, pepper_hex):
    password = hashlib.sha512((password + salt_hex + pepper_hex).encode()).hexdigest()
    return password

def password_is_correct(password_inserted, password_db, salt_hex):
    password_inserted = encrypt_password(password_inserted, salt_hex, PEPPER_HEX)
    return (password_inserted == password_db)









