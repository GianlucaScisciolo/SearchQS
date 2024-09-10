print("Scomposizione in fattori di un numero n")
n = int(input("n? "))
fattori = []
d = 2
while n > 1:
    if n % d == 0:
        print(n, "\t |", d)
        n //= d   
        fattori.append(d)
    else:
        d += 1
print(n)
print(fattori)

