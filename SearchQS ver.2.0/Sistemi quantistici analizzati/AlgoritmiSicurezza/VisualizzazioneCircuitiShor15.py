import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from math import gcd
from numpy.random import randint
from fractions import Fraction
import utils as utils

VALID_A = [2, 7, 8, 11, 13]
a = 7
n_count = 8
power = 10

a_mod_15_circuit = QuantumCircuit(4)
a_mod_15_circuit = utils.get_a_mod_15_circuit(a, power)
a_mod_15_circuit.draw(output = 'mpl', fold=-1)

qft_inverse_circuit = QuantumCircuit(n_count)
qft_inverse_circuit = utils.get_qft_inverse_circuit(n_count)
qft_inverse_circuit.draw(output='mpl', scale=4)

