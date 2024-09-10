from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
import numpy as np
from sklearn.datasets import make_blobs
import pandas as pd
def get_random_binary_number(num_bit, backend):
    if not isinstance(num_bit, int) or num_bit <= 0:
        return None
    qr = QuantumRegister(num_bit, 'qr')
    cr = ClassicalRegister(num_bit, 'cr')
    random_binary_number_circuit = QuantumCircuit(qr, cr)
    for index in range(0, num_bit):
        random_binary_number_circuit.h(qr[index])
    random_binary_number_circuit.measure(qr, cr)
    job = transpile(random_binary_number_circuit, backend=backend)
    shots = 1
    result = backend.run(job, shots=shots).result()
    counts = result.get_counts(random_binary_number_circuit)
    binary_number = list(counts.keys())[0]
    return binary_number

def from_binary_to_decimal(binary_number):
    if not isinstance(binary_number, str) or binary_number == "":
        return None
    n = len(binary_number)
    decimal_number = 0
    for index in range(n):
        decimal_number += int(binary_number[n - 1 - index]) * (2 ** index)
    return decimal_number

def get_random_points(n_samples, centers, cluster_std, random_state, color_points, file_name):
    X, y_true = make_blobs(n_samples=n_samples, centers=centers, cluster_std=cluster_std, random_state=random_state)
    X = X[:, ::-1]
    X_min, X_max = X.min(axis=0), X.max(axis=0)
    X = 1.8 * (X - X_min) / (X_max - X_min) - 0.9
    X = np.round(X, 4)
    data = {
        'ID': np.arange(1, n_samples + 1),
        'X': X[:, 0],
        'Y': X[:, 1],
        'Cluster': [color_points] * n_samples
    }
    points = list(zip(data['ID'], data['X'], data['Y'], data['Cluster']))
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    return points

def plt_show_points_and_centroids(k_means_data, plt, bc, gc, oc, pc):
    colors = {'White': "#FFFFFFFF", 'Blue': "#0000FF", 'Green': "#00FF00", 'Orange': "#FE4C10", 'Purple': "#D025DB"}
    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.set(xlabel='X', ylabel='Y')
    ax.set_ylabel('X', rotation=0)
    ax.set_ylabel('Y', rotation=0)
    plt.plot(bc[0], bc[1], 'x', color=colors['Blue'],   markersize=10, markeredgewidth=2)
    plt.plot(gc[0], gc[1], 'x', color=colors['Green'],  markersize=10, markeredgewidth=2)
    plt.plot(oc[0], oc[1], 'x', color=colors['Orange'], markersize=10, markeredgewidth=2)
    plt.plot(pc[0], pc[1], 'x', color=colors['Purple'], markersize=10, markeredgewidth=2)
    for cluster, group in k_means_data.groupby('Cluster'):
        marker = 's' if cluster == 'White' else 'o'
        plt.scatter(group['X'], group['Y'], c=group['Cluster'].map(colors), alpha=0.5, marker=marker)
    plt.axis([-1, 1, -1, 1])
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.show()

def get_clusters_data(k_means_data):
    isWhite = k_means_data['Cluster'] == 'White'
    isBlue = k_means_data['Cluster'] == 'Blue'
    isGreen = k_means_data['Cluster'] == 'Green'
    isOrange = k_means_data['Cluster'] == 'Orange'
    isPurple = k_means_data['Cluster'] == 'Purple'
    
    whiteData = k_means_data[isWhite].drop([], axis=1)
    blueData = k_means_data[isBlue].drop([], axis=1)
    greenData = k_means_data[isGreen].drop([], axis=1)
    orangeData = k_means_data[isOrange].drop([], axis=1)
    purpleData = k_means_data[isPurple].drop([], axis=1)
    return (whiteData, blueData, greenData, orangeData, purpleData)

def get_random_decimal_number(num_bit, backend, min_value, max_value):
    binary_number = get_random_binary_number(num_bit, backend)
    decimal_number = from_binary_to_decimal(binary_number)
    max_binary_value = 2 ** num_bit - 1
    normalized_value = decimal_number / max_binary_value
    scaled_value = (max_value - min_value) * normalized_value + min_value
    return round(scaled_value, 4)

def get_quantum_point_classification(theta_list, phi_list):
    qr = QuantumRegister(3, 'qr')
    cr = ClassicalRegister(1, 'cr')
    quantum_point_classification_circuit = QuantumCircuit(qr, cr)
    results_list = []
    for i in range(1, 5):
        quantum_point_classification_circuit.h(qr[2])
        quantum_point_classification_circuit.u(theta_list[0], phi_list[0], 0, qr[0])      
        quantum_point_classification_circuit.u(theta_list[i], phi_list[i], 0, qr[1])
        quantum_point_classification_circuit.cswap(qr[2], qr[0], qr[1])
        quantum_point_classification_circuit.h(qr[2])
        quantum_point_classification_circuit.measure(qr[2], cr[0])
        quantum_point_classification_circuit.reset(qr)
        backend = Aer.get_backend('qasm_simulator')
        job = transpile(quantum_point_classification_circuit, backend=backend)
        shots = 1024
        result = backend.run(job, shots=shots).result()
        counts = result.get_counts(quantum_point_classification_circuit)
        if '1' in counts:
            results_list.append(counts['1'])
        else:
            results_list.append(0)
    class_list = ['Blue', 'Green', 'Orange', 'Purple']
    quantum_point_classification = class_list[results_list.index(min(results_list))]
    return quantum_point_classification
    
def get_new_centroid(clusterData, current_centroid):
    clusterData = clusterData[['X', 'Y']]
    if not clusterData.empty:
        # Calcola la media manualmente
        sum_x = 0
        sum_y = 0
        for x, y in zip(clusterData['X'], clusterData['Y']):
            sum_x += x
            sum_y += y
        mean_x = sum_x / len(clusterData)
        mean_y = sum_y / len(clusterData)
        return (mean_x, mean_y)
    else:
        return current_centroid