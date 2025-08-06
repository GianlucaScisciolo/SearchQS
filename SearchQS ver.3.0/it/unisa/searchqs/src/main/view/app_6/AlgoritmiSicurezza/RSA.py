import random
import utils as utils

PRIME_NUMBERS = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,	41,	43,	47, 53,	59, 61,	67, 71,	73,	79,	83, 89,	97
]

# Funzione che ritorna il M.C.D tra a e b tramite l'algoritmo di Euclide
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Funzione ch implementa l'algoritmo esteso di Euclide per trovare l'inverso moltiplicativo di due numeri
def multiplicative_inverse(e, z):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_z = z
    while e > 0:
        temp1 = temp_z//e
        temp2 = temp_z - temp1 * e
        temp_z = e
        e = temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    if temp_z == 1:
        return d + z
    
# Funzione che ritorna True se num è primo e False se num non è primo
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

# funzione per generare la chiae pubblica e la chiave privata
def keys_generation(p=0, q=0):
    """
    Chiave Pubblica: è formata da 2 numeri (n; e)
    Chiave Privata: è formata da 2 numeri (n; d)
    """
    """
    1: Si scelgono due numeri primi (p; q) abbastanza grandi (maggiori di 300 cifre). Si calcola il loro 
       prodotto chiamato anche modulo n = p*q (ovviamente la fattorizzazione è segreta) e si pone z = (p-1)*(q-1). 
       (La funzione z coincide con la funzione di Eulero quando n è il prodotto di due numeri primi, tale funzione 
       associa a un numero intero n il numero dei numeri interi co-primi con n e minori di n compreso l'uno. 
       Se n è un numero primo z(n) = n-1).
    """
    min_index = 0
    max_index = len(PRIME_NUMBERS) - 1
    if p == 0:
        p = PRIME_NUMBERS[random.randint(min_index, max_index)]
    if q == 0:
        q = -1
        while True:
            q = PRIME_NUMBERS[random.randint(min_index, max_index)]
            if q != p:
                break
    n = p * q
    z = -1
    if is_prime(n):
        z = n-1
    else:
        z = (p-1) * (q-1)
    
    """
    2: Si sceglie poi un numero e chiamato esponente pubblico, coprimo con z e più piccolo di z stesso 
       (e non deve necessariamente essere primo).
    """
    e = -1
    while(True):
        e = random.randint(1, z-1)
        # Utilizziamo l'algoritmo di Euclide M.C.D per verificare che e, z siano coprimi
        if gcd(e, z) == 1:
            break
    """
    3: Si sceglie il numero d chiamato esponente privato tale che il suo prodotto con e sia congruo a 1 mod(z),
       cioè d ∙ e ≡ 1 mod(z)
    """
    d = multiplicative_inverse(e, z)
    public_key = (n, e)
    private_key = (n, d)
    return {"public_key": public_key, "private_key": private_key}

def encrypt_message(public_key, plain_message):
    (n, e) = public_key
    cipher = [pow(ord(char), e, n) for char in plain_message]
    return cipher

def decrypt_message(private_key, cipher_message):
    (n, d) = private_key
    aux = [str(pow(char, d, n)) for char in cipher_message]
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain) 

def rsa_attack(public_key, cipher_message, factorization_algorithm_name):
    n = public_key[0]
    e = public_key[1]
    fattori_n = []
    if factorization_algorithm_name == 'fattorizzazione_classica':
        fattori_n = utils.fattorizzazione_classica(n)
    p = fattori_n[0]
    q = fattori_n[1]
    print(p, q)
    z = -1
    if is_prime(n):
        z = n-1
    else:
        z = (p-1) * (q-1)
    print(z)
    d = multiplicative_inverse(e, z)
    print(d)
    private_key_obtained = (n, d)
    print(private_key_obtained)
    hacked_message = decrypt_message(private_key_obtained, cipher_message)
    return (private_key_obtained, hacked_message)

print("Esempio 1:")
print("Uso RSA:")
keys = keys_generation(89, 97)
plain_message = "Hello, World!"
cipher_message = encrypt_message(keys["public_key"], plain_message)
post_decrypt_message = decrypt_message(keys["private_key"], cipher_message)

print(f"Messaggio da inviare: {plain_message}")
print(f"Messaggio cifrato: {cipher_message}")
print(f"Messaggio decifrato ottenuto: {post_decrypt_message}")

print("\nProva attacco RSA:")
(private_key_obtained, hacked_message) = rsa_attack(keys['public_key'], cipher_message, 'fattorizzazione_classica')
print(f"Messaggio da hackerare: {cipher_message}")
print(f"Chiave privata ottenuta: {private_key_obtained}")
print(f"Messaggio hackerato: {hacked_message}")