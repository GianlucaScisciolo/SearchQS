import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from numpy.random import randint
import utils as utils

a = 7
n_count = 8
shor_15_circuit = QuantumCircuit(n_count+4, n_count)
shor_15_circuit = utils.get_shor_15_circuit(a, n_count)
shor_15_circuit.draw(output = 'mpl', fold=-1)

VALID_A = [2, 7, 8, 11, 13]
N_COUNT = 8 # numero di qubit di conteggio da utilizzare
tries = 0 # traccia il numero di tentativi
guesses = [0, 0] # ipotesi prodotte dalla prova
# ripetere fino a quando non si trovano ipotesi soddisfacenti
# dovrebbero in realtà essere fattori di 15 e non essere 1 e 15
while (not guesses[0]*guesses[1]==15) or 15 in guesses:
    tries += 1
    # scegliamo a caso un a con cui possiamo lavorare
    i = randint(len(VALID_A))
    a = VALID_A[i]
    print(f"Prova: {tries}")
    print(f"a: {a}")
    # utilizziamo l'algoritmo di Shor per indovinare i fattori
    guesses = utils.run_shor_15(a, N_COUNT)
    print("guess:", guesses)
    print("\n")
# Fattori trovati
print("Fattori trovati!")
print(f"I fattori di 15 sono: {guesses[0]} e {guesses[1]}!")

