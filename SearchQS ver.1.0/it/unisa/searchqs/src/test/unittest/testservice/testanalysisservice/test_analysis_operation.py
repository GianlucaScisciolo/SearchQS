import sys
sys.path.append("../../../../..")

import unittest
import numpy as np
import src.main.service.analysisservice.analysis_operation as a_op
from qiskit.circuit import QuantumCircuit, Instruction
from src.main.model.entity.result_dynamic_analysis import ResultDynamicAnalysis

class TestAnalysisOperation(unittest.TestCase):
    matrix_circuit = np.array(
            [
                ['None', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29'],
                ['qb-0', '', 'barrier()', 'h()', '', '', '', '', '', '', 'barrier()', 'cx()', '', '', '', 'barrier()', 'h()', '', '', '', '', '', '', 'barrier()', 'measure()', '', '', '', '', ''],
                ['qb-1', '', 'barrier()', '', 'h()', '', '', '', '', '', 'barrier()', '', '', '', '', 'barrier()', '', 'h()', '', '', '', '', '', 'barrier()', '', 'measure()', '', '', '', ''],
                ['qb-2', '', 'barrier()', '', '', 'h()', '', '', '', '', 'barrier()', '', 'cx()', '', '', 'barrier()', '', '', 'h()', '', '', '', '', 'barrier()', '', '', 'measure()', '', '', ''],
                ['qb-3', '', 'barrier()', '', '', '', 'h()', '', '', '', 'barrier()', '', '', '', '', 'barrier()', '', '', '', 'h()', '', '', '', 'barrier()', '', '', '', 'measure()', '', ''],
                ['qb-4', '', 'barrier()', '', '', '', '', 'h()', '', '', 'barrier()', '', '', 'cx()', '', 'barrier()', '', '', '', '', 'h()', '', '', 'barrier()', '', '', '', '', 'measure()', ''],
                ['qb-5', '', 'barrier()', '', '', '', '', '', 'h()', '', 'barrier()', '', '', '', 'cx()', 'barrier()', '', '', '', '', '', 'h()', '', 'barrier()', '', '', '', '', '', 'measure()'],
                ['qb-6', 'x()', 'barrier()', '', '', '', '', '', '', 'h()', 'barrier()', 'cx()', 'cx()', 'cx()', 'cx()', 'barrier()', '', '', '', '', '', '', 'h()', 'barrier()', '', '', '', '', '', ''],
                ['cb-0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['cb-1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['cb-2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['cb-3', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['cb-4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                ['cb-5', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            ]
        )
    matrix_qc = np.array(
            [
                ['None', '1', '2'],
                ['qb-0', 'h()', 'cx()'],
                ['qb-1', '', 'cx()']
            ]
        )
    file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
    current_code = """from IPython.display import IFrame
s = '110101'
from qiskit import *
n = len(s)
circuit = QuantumCircuit(n+1,n)
# Step 0
circuit.x(n) # the n+1 qubits are indexed 0...n, so the last qubit is index    <--
circuit.barrier() # just a visual aid for now
# Step 1
circuit.h(range(n+1)) # range(n+1) returns [0,1,2,...,n] in Python. This covers all the qubits    <--
circuit.barrier() # just a visual aid for now
# Step 2
for ii, yesno in enumerate(reversed(s)):
    if yesno == '1': 
        circuit.cx(ii, n)
circuit.barrier() # just a visual aid for now
# Step 3
circuit.h(range(n+1)) # range(n+1) returns [0,1,2,...,n] in Python. This covers all the qubits
circuit.barrier() # just a visual aid for now
circuit.measure(range(n), range(n)) # measure the qubits indexed from 0 to n-1 and store them into the classical bits indexed 0 to n-1
qc = QuantumCircuit(2)
# Applica una porta Hadamard al primo qubit
qc.h(0)
# Applica una porta CNOT tra il primo e il secondo qubit
qc.cx(0, 1)
        """
    names_qc = ['circuit', 'qc']
    
    def test_1_get_names_q_circuits_from_file(self):
        file_path = "SistemaQuantistico/bernstein_vazirani_algorithm.py"
        result = a_op.get_names_q_circuits_from_file(file_path)
        oracle = ["circuit", "qc"]
        self.assertEqual(result, oracle)

    def test_2_get_matrix(self):
        with open(self.file_path, 'w') as file:
            file.write(self.current_code)
        names_qc = ["circuit", "qc"]
        self.assertTrue(np.array_equal(a_op.get_matrix(self.file_path, names_qc[0]), self.matrix_circuit))
        self.assertTrue(np.array_equal(a_op.get_matrix(self.file_path, names_qc[1]), self.matrix_qc))
        
    def test_3_id_qubit(self):
        qc = QuantumCircuit(6)
        qubit = qc.qregs[0][5]
        oracle = 5
        result = a_op.get_id_qubit(qubit)
        self.assertEqual(result, oracle)

    def test_4_get_id_operation(self):
        test_operation = Instruction('test_operation', num_qubits=3, num_clbits=0, params=[1, 2, 3])
        oracle = 'test_operation(int,int,int)'
        result = a_op.get_id_operation(test_operation)
        self.assertEqual(result, oracle)

    def test_5_add_transpilation_code_to_source_file(self):
        self.file_path
        self.current_code
        self.names_qc
        name_transpilation = 'ibm_perth'
        optimization = 2
        a_op.add_transpilation_code_to_source_file(self.file_path, self.current_code, self.names_qc, 
                                                            name_transpilation, optimization)
        new_code = ""
        with open(self.file_path, 'r') as file:
            new_code = file.read()
        
        oracle = ""
        oracle += "from qiskit import transpile\n"
        oracle += "from IPython.display import IFrame\n"
        oracle += "s = '110101'\n"
        oracle += "from qiskit import *\n"
        oracle += "n = len(s)\n"
        oracle += "circuit = QuantumCircuit(n+1,n)\n"
        oracle += "# Step 0\n"
        oracle += "circuit.x(n) # the n+1 qubits are indexed 0...n, so the last qubit is index    <--\n"
        oracle += "circuit.barrier() # just a visual aid for now\n"
        oracle += "# Step 1\n"
        oracle += "circuit.h(range(n+1)) # range(n+1) returns [0,1,2,...,n] in Python. This covers all the qubits    <--\n"
        oracle += "circuit.barrier() # just a visual aid for now\n"
        oracle += "# Step 2\n"
        oracle += "for ii, yesno in enumerate(reversed(s)):\n"
        oracle += "    if yesno == '1': \n"
        oracle += "        circuit.cx(ii, n)\n"
        oracle += "circuit.barrier() # just a visual aid for now\n"
        oracle += "# Step 3\n"
        oracle += "circuit.h(range(n+1)) # range(n+1) returns [0,1,2,...,n] in Python. This covers all the qubits\n"
        oracle += "circuit.barrier() # just a visual aid for now\n"
        oracle += "circuit.measure(range(n), range(n)) # measure the qubits indexed from 0 to n-1 and store them into the classical bits indexed 0 to n-1\n"
        oracle += "qc = QuantumCircuit(2)\n"
        oracle += "# Applica una porta Hadamard al primo qubit\n"
        oracle += "qc.h(0)\n"
        oracle += "# Applica una porta CNOT tra il primo e il secondo qubit\n"
        oracle += "qc.cx(0, 1)\n"
        oracle += "        \ncircuit = transpile(circuit, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=2)\n"
        oracle += "qc = transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=2)"
        with open(self.file_path, 'w') as file:
            file.write(self.current_code)
        self.assertEqual(new_code, oracle)

    def test_6_get_result_static_analysis(self):
        file_path = "SistemaQuantistico/file_test_1.py"
        current_code = ""
        current_code += "from qiskit import QuantumCircuit, transpile, BasicAer\n"
        current_code += "qc = QuantumCircuit(2)\n"
        current_code += "qc.h(0)\n"
        current_code += "qc.cx(0, 1)\n"
        current_code += "simulator = BasicAer.get_backend('statevector_simulator')\n"
        current_code += "transpiled_circuit = transpile(qc, simulator)\n"
        current_code += "transpiled_circuit = transpile(qc, simulator)\n"
        current_code += "transpiled_circuit = transpile(qc, simulator)\n"
        current_code += "transpiled_circuit = transpile(qc, simulator)\n"
        names_qc = ["qc"]
        names_transpilation = "ibm_perth"
        optimization = 2
        result = a_op.get_result_static_analysis(file_path, current_code, names_qc, names_transpilation, optimization)
        with open(file_path, 'w') as file:
            file.write(current_code)
        oracle = ""
        oracle += f"Risultato quantum smell LPQ: 4\n"
        oracle += f"Risultato quantum smell NC: 0\n"
        self.assertEqual(result, oracle)

    def test_7_get_results_dynamic_analysis(self):
        name_transpilation = 'ibm_perth'
        optimization = 2
        id_r = 10
        results_da = a_op.get_results_dynamic_analysis(self.file_path, self.current_code, self.names_qc, 
                                                      name_transpilation, optimization, id_r)
        matrix_circuit = """[[None  1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17    18    19    20    21    22    23    24    25    26    27    28    29    30    31    32    33    34    35    36    37    38    39    40    41    42    43    44    45    46    47    48    49    50    51    52    53    54    55    56    57   ]
 [qb-0  '' barrier() rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' barrier() cx()  '' '' '' barrier() rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' barrier() measure() '' '' '' '' '']
 [qb-1  '' barrier() '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' barrier() '' '' '' '' barrier() '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' barrier() '' measure() '' '' '' '']
 [qb-2  '' barrier() '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' '' '' '' barrier() '' cx()  '' '' barrier() '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' '' '' '' barrier() '' '' measure() '' '' '']
 [qb-3  '' barrier() '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' barrier() '' '' '' '' barrier() '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' '' '' '' barrier() '' '' '' measure() '' '']
 [qb-4  '' barrier() '' '' '' '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' barrier() '' '' cx()  '' barrier() '' '' '' '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' '' '' '' barrier() '' '' '' '' measure() '']
 [qb-5  '' barrier() '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' barrier() '' '' '' cx()  barrier() '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) '' '' '' barrier() '' '' '' '' '' measure()]
 [qb-6  x()   barrier() '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) barrier() cx()  cx()  cx()  cx()  barrier() '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' rz(float) sx()  rz(float) barrier() '' '' '' '' '' '']
 [cb-0  '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '']
 [cb-1  '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '']
 [cb-2  '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '']
 [cb-3  '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '']
 [cb-4  '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '']
 [cb-5  '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '']]"""
        matrix_qc = """[[None  1     2     3     4    ]
 [qb-0  rz(float) sx()  rz(float) cx() ]
 [qb-1  '' '' '' cx() ]]"""
        result_circuit = ""
        result_circuit += "Risultato quantum smell IdQ: 22\n"
        result_circuit += "Risultato quantum smell IQ: 18\n"
        result_circuit += "Risultato quantum smell IM: 0\n"
        result_circuit += "Risultato quantum smell LC: 22\n"
        result_circuit += "Risultato quantum smell ROC: 0\n"
        result_circuit += "Risultato quantum smell CG: 0\n"

        result_qc = ""
        result_qc += "Risultato quantum smell IdQ: 22\n"
        result_qc += "Risultato quantum smell IQ: 18\n"
        result_qc += "Risultato quantum smell IM: 0\n"
        result_qc += "Risultato quantum smell LC: 8\n"
        result_qc += "Risultato quantum smell ROC: 0\n"
        result_qc += "Risultato quantum smell CG: 0\n"

        oracle = [
            ResultDynamicAnalysis(0, 'circuit', 1, matrix_circuit, result_circuit, id_r),
            ResultDynamicAnalysis(0, 'qc', 2, matrix_qc, result_qc, id_r)
        ]
        self.assertEqual(results_da, oracle)










