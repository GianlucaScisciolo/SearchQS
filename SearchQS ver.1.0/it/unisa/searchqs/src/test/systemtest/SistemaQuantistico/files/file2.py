from qiskit import *
circuito = QuantumCircuit(2,2)
circuito.h([0,1])
circuito.x(0)
circuito.y(1)
print(circuito)
