import utils as utils

def from_string_to_binary(string):
    return ' '.join(format(ord(char), '08b') for char in string)

def from_binary_to_string(binary_string):
    binary_values = binary_string.split(' ')
    ascii_characters = [chr(int(bv, 2)) for bv in binary_values]
    return ''.join(ascii_characters)

frase_stringa = "Hello, World!"
frase_binaria = from_string_to_binary(frase_stringa)
frase_binaria_teletrasportata = ""
for bit in frase_binaria:
    if bit == ' ':
        frase_binaria_teletrasportata += ' '
    else:
        frase_binaria_teletrasportata += utils.get_teleported_value(bit)
frase_stringa_teletrasportata = from_binary_to_string(frase_binaria_teletrasportata)
print(f"Frase da teletrasportare: {frase_stringa} = {frase_binaria}")
print(f"Frase teletrasportata: {frase_binaria_teletrasportata} = {frase_stringa_teletrasportata}")

