from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
import pandas as pd
import math
from fractions import Fraction
from math import gcd

def fattorizzazione_classica(n):
    fattori = []
    d = 2
    while n > 1:
        if n % d == 0:
            n //= d   
            fattori.append(d)
        else:
            d += 1
    return fattori

# funzione che Crea delle stringhe casuali di lunghezza string_length
def randomStringGen(string_length):
    # variabili di output utilizzate per accedere ai risultati del computer quantistico alla fine della funzione
    output_list = []
    output = ''
    # avviamo le informazioni sul circuito quantistico
    backend = Aer.get_backend('qasm_simulator')  
    circuits = ['rs']
    # eseguiamo il circuito in lotti di 10 qubit per risultati più rapidi. 
    # I risultati di ogni esecuzione verranno aggiunti e poi ridotti alla giusta dimensione n.
    n = string_length
    temp_n = 10
    temp_output = ''
    for i in range(math.ceil(n/temp_n)):
        q = QuantumRegister(temp_n, name='q')
        c = ClassicalRegister(temp_n, name='c')
        rs = QuantumCircuit(q, c, name='rs')
        for i in range(temp_n):
            rs.h(q[i])
            rs.measure(q[i],c[i])
        job = transpile(rs, backend=backend)
        shots = 1
        result = backend.run(job, shots=shots).result()
        counts = result.get_counts(rs)
        result_key = list(result.get_counts(rs).keys())
        temp_output = result_key[0]
        output += temp_output
    # restituiamo l'output tagliato alla dimensione della lunghezza della stringa desiderata
    return output[:n]

def get_a_mod_15_circuit(a, power):
    if a not in [2,7,8,11,13]:
        raise ValueError("'a' deve essere 2,7,8,11 o 13")
    a_mod_15_circuit = QuantumCircuit(4)
    for i in range(power):
        if a == 2:
            a_mod_15_circuit.swap(0,1)
            a_mod_15_circuit.swap(1,2)
            a_mod_15_circuit.swap(2,3)
        elif a == 7:
            a_mod_15_circuit.swap(2,3)
            a_mod_15_circuit.swap(1,2)
            a_mod_15_circuit.swap(0,1)
            for q in range(4):
                a_mod_15_circuit.x(q)
        elif a == 8:
            a_mod_15_circuit.swap(2,3)
            a_mod_15_circuit.swap(1,2)
            a_mod_15_circuit.swap(0,1)
        elif a == 11:
            a_mod_15_circuit.swap(1,3)
            a_mod_15_circuit.swap(0,2)
            for q in range(4):
                a_mod_15_circuit.x(q)
        elif a == 13:
            a_mod_15_circuit.swap(0,1)
            a_mod_15_circuit.swap(1,2)
            a_mod_15_circuit.swap(2,3)
            for q in range(4):
                a_mod_15_circuit.x(q)
    return a_mod_15_circuit

def get_c_a_mod_15_gate(a, power):
    a_mod_15_circuit = get_a_mod_15_circuit(a, power)
    c_a_mod_15_gate = a_mod_15_circuit.to_gate()
    c_a_mod_15_gate.name = "%i^%i mod 15" % (a, power)
    c_a_mod_15_gate = c_a_mod_15_gate.control(1)
    return c_a_mod_15_gate

def get_qft_inverse_circuit(n_count):
    qft_inverse_circuit = QuantumCircuit(n_count)
    # Invertiamo l'ordine dei qubit (secondo la convenzione)
    for qubit in range(n_count//2):
        qft_inverse_circuit.swap(qubit, n_count-qubit-1)
    # Esaminiamo e "srotoliamo" ogni qubit, in base alle fasi dei qubit di potenza superiore
    for j in range(n_count):
        for m in range(j):
            qft_inverse_circuit.cp(-np.pi/float(2**(j-m)), m, j)
        # Convertiamo da base hardaman a base standard
        qft_inverse_circuit.h(j)
    return qft_inverse_circuit

def get_qft_inverse_gate(n_count):
    qft_inverse_gate = get_qft_inverse_circuit(n_count).to_gate()
    qft_inverse_gate.name = "QFT†"
    return qft_inverse_gate

def get_shor_15_circuit(a, n_count):
    qft_inverse_gate = get_qft_inverse_gate(n_count)
    shor_15_circuit = QuantumCircuit(n_count+4, n_count)
    shor_15_circuit.h(range(n_count))
    shor_15_circuit.x(n_count+3)
    for q in range(n_count):
        power = 2**q
        shor_15_circuit.append(get_c_a_mod_15_gate(a, power), [q]+[i+n_count for i in range(4)])
    shor_15_circuit.append(qft_inverse_gate, range(n_count))
    shor_15_circuit.measure(range(n_count), range(n_count))
    return shor_15_circuit 

def simulator(circuit, n_shots):
    qasm_sim = Aer.get_backend('qasm_simulator')
    trans = transpile(circuit, qasm_sim)
    results = qasm_sim.run(trans, shots=n_shots, memory=True).result()
    return results

def run_shor_15(a, n_count):
    shor_15_circuit = get_shor_15_circuit(a, n_count)
    results = simulator(shor_15_circuit, 1)
    binary_result = results.get_memory()[0]
    result = int(binary_result, 2)
    phase = result/(2**n_count)
    frac = Fraction(phase).limit_denominator(15) # limitare il denominatore a 15 per evitare errori di arrotondamento
    r = frac.denominator
    print("r:", r)
    # utilizziamo l'algoritmo di Euclide per convertire da periodo a fattori
    factors = [gcd(a**(r//2)-1, 15), gcd(a**(r//2)+1, 15)]
    return factors









