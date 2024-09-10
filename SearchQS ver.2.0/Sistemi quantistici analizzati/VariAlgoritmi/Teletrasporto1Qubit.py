from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_aer import Aer
from matplotlib import style

style.use('dark_background')

# Otteniamo e stampiamo il circuito quantistico del teletrasporto quantistico
value = "1"
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
teleportation_circuit.draw(output='mpl')

# Esecuzione circuito quantistico
backend = Aer.get_backend('statevector_simulator')
job = transpile(teleportation_circuit, backend=backend)
shots = 1024
result = backend.run(job, shots=shots).result()
counts = result.get_counts(teleportation_circuit)

# Visualizzazione istogramma
plot_histogram(counts, color='green')

state = result.get_statevector()
plot_bloch_multivector(state)

print(f"valore da teletrasportare: {value}")
print(f"valore teletrasportato: {max(counts, key=counts.get)[0]}")

