from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def from_binary_to_decimal(binary_number):
    if not isinstance(binary_number, str) or binary_number == "":
        return None
    n = len(binary_number)
    decimal_number = 0
    for index in range(n):
        decimal_number += int(binary_number[n - 1 - index]) * (2 ** index)
    return decimal_number

def get_teleported_value(value):
    teleportation_circuit = QuantumCircuit(3,3)
    if value == "1":
        teleportation_circuit.x(0)
    teleportation_circuit.barrier()
    teleportation_circuit.h(1)
    teleportation_circuit.cx(1,2)
    teleportation_circuit.cx(0,1)
    teleportation_circuit.h(0)
    teleportation_circuit.barrier()
    teleportation_circuit.measure([0, 1], [0, 1])
    teleportation_circuit.barrier()
    teleportation_circuit.cx(1, 2)
    teleportation_circuit.cz(0, 2)
    teleportation_circuit.measure([2], [2])
    # Esecuzione circuito quantistico
    backend = Aer.get_backend('statevector_simulator')
    job = transpile(teleportation_circuit, backend=backend)
    shots = 1024
    result = backend.run(job, shots=shots).result()
    counts = result.get_counts(teleportation_circuit)
    return max(counts, key=counts.get)[0]

