import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from numpy import pi
import csv
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit_aer import Aer
import utils as utils

warnings.filterwarnings('ignore')

backend = Aer.get_backend('statevector_simulator')
num_bit = 5
k = 4

# Creazione di un singolo punto
x = 0.7500
y = 0.7500
data = {
    'ID': [1],
    'X': [x],
    'Y': [y],
    'Cluster': ['White']
}
points = list(zip(data['ID'], data['X'], data['Y'], data['Cluster']))
df = pd.DataFrame(data)
file_name = "k_means_data.csv"
df.to_csv(file_name, index=False)
(bc, gc, oc, pc) = (-0.5000, 0.5000), (0.5000, 0.5000), (-0.5000, -0.5000), (0.5000, -0.5000)
# Otteniamo e visualizziamo i punti e i centroidi
k_means_data = pd.read_csv('k_means_data.csv', usecols=['ID', 'X', 'Y', 'Cluster'])
utils.plt_show_points_and_centroids(k_means_data, plt, bc, gc, oc, pc)

phi_list = [((x + 1) * pi / 2) for x in [float(points[0][1]), bc[0], gc[0], oc[0], pc[0]]]
theta_list = [((x + 1) * pi / 2) for x in [float(points[0][2]), bc[1], gc[1], oc[1], pc[1]]]
# Creazione del circuito quantistico
qr = QuantumRegister(3, 'qr')
cr = ClassicalRegister(1, 'cr')
quantum_point_classification_circuit = QuantumCircuit(qr, cr)
# Creazione di una lista per contenere i risultati
results_list = []
# Stima delle distanze dal nuovo punto ai centroidi
for i in range(1, 5):
    quantum_point_classification_circuit.h(qr[2])
    quantum_point_classification_circuit.u(theta_list[0], phi_list[0], 0, qr[0])        
    quantum_point_classification_circuit.u(theta_list[i], phi_list[i], 0, qr[1])
    quantum_point_classification_circuit.cswap(qr[2], qr[0], qr[1])
    quantum_point_classification_circuit.h(qr[2])
    quantum_point_classification_circuit.measure(qr[2], cr[0])
    # Resettiamo il qubit in modo da poterlo riutilizzare di nuovo, poiché consuma meno memoria e spazio.
    quantum_point_classification_circuit.reset(qr)
    # Esecuzione del circuito quantistico
    job = transpile(quantum_point_classification_circuit, backend=backend)
    shots = 1024
    result = backend.run(job, shots=shots).result()
    counts = result.get_counts(quantum_point_classification_circuit) # counts su |1>
    # Aggiungi un controllo per verificare se la chiave '1' esiste
    if '1' in counts:
        results_list.append(counts['1'])
    else:
        results_list.append(0)
# Creazione di una lista contenente le classi possibili
class_list = ['Blue', 'Green', 'Orange', 'Purple']
# Scopriamo a quale classe appartiene il nuovo punto dati secondo il nostro algoritmo quantistico di stima della distanza
quantum_point_classification = class_list[results_list.index(min(results_list))]
new_cluster = quantum_point_classification
points[0] = (points[0][0], points[0][1], points[0][2], new_cluster)
with open('k_means_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'X', 'Y', 'Cluster'])
    for i, point in enumerate(points, start=1):
        writer.writerow(point)
k_means_data = pd.read_csv('k_means_data.csv', usecols=['ID', 'X', 'Y', 'Cluster'])

quantum_point_classification_circuit.draw(output = 'mpl')

utils.plt_show_points_and_centroids(k_means_data, plt, bc, gc, oc, pc)

# Generiamo casualmente 64 punti
n_samples = 64
centers = 1
cluster_std = 0.60
random_state = 1
color_points = new_cluster
file_name = "k_means_data.csv"
points = utils.get_random_points(n_samples, centers, cluster_std, random_state, color_points, file_name)
k_means_data = pd.read_csv('k_means_data.csv', usecols=['ID', 'X', 'Y', 'Cluster'])
(c1, c2) = ((2.0000, 2.0000), (2.0000, 2.0000))
if color_points == "Blue":
    c1 = bc
    utils.plt_show_points_and_centroids(k_means_data, plt, c1, c2, c2, c2)
elif color_points == "Green":
    c1 = gc
    utils.plt_show_points_and_centroids(k_means_data, plt, c2, c1, c2, c2)
elif color_points == "Orange":
    c1 = oc
    utils.plt_show_points_and_centroids(k_means_data, plt, c2, c2, c1, c2)
elif color_points == "Purple":
    c1 = pc
    utils.plt_show_points_and_centroids(k_means_data, plt, c2, c2, c2, c1)

# Selezioniamo i dati per il clustering
cluster_data = k_means_data[['X', 'Y']]
num_qubits = int(np.ceil(np.log2(len(cluster_data))))
# otteniamo il nuovo centroide
c1 = utils.get_new_centroid(k_means_data, c1)
if color_points == "Blue":
    utils.plt_show_points_and_centroids(k_means_data, plt, c1, c2, c2, c2)
elif color_points == "Green":
    utils.plt_show_points_and_centroids(k_means_data, plt, c2, c1, c2, c2)
elif color_points == "Orange":
    utils.plt_show_points_and_centroids(k_means_data, plt, c2, c2, c1, c2)
elif color_points == "Purple":
    utils.plt_show_points_and_centroids(k_means_data, plt, c2, c2, c2, c1)




