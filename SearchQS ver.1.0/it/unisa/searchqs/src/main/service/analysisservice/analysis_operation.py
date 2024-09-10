from src.main.service.analysisservice.transpilation import Transpilation
from src.main.model.entity.source_file import SourceFile
from src.main.model.entity.analysis import Analysis
from src.main.model.entity.result_dynamic_analysis import ResultDynamicAnalysis
from src.main.service.analysisservice.qcsmell.idq import IdQ
from src.main.service.analysisservice.qcsmell.iq import IQ
from src.main.service.analysisservice.qcsmell.im import IM
from src.main.service.analysisservice.qcsmell.lc import LC
from src.main.service.analysisservice.qcsmell.roc import ROC
from src.main.service.analysisservice.qcsmell.cg import CG
from src.main.service.analysisservice.qcsmell.lpq import LPQ
from src.main.service.analysisservice.qcsmell.nc import NC
import numpy as np
import ast
from qiskit.circuit import QuantumCircuit, ClassicalRegister, Qubit, Clbit, Instruction

def get_names_q_circuits_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            qiskit_code = file.read()
            tree = ast.parse(qiskit_code)
            names_q_circuits = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                    func = node.value.func
                    if isinstance(func, ast.Name) and func.id == 'QuantumCircuit':
                        if node.targets[0].id not in names_q_circuits:
                            names_q_circuits.append(node.targets[0].id)
                    elif isinstance(func, ast.Attribute) and func.attr == 'QuantumCircuit':
                        if node.targets[0].id not in names_q_circuits:
                            names_q_circuits.append(node.targets[0].id)
            return names_q_circuits
    except FileNotFoundError:
        raise Exception
    
def get_matrix(file_path, name_qc):
    with open(file_path, "r") as file:
        qiskit_code = file.read()
    local_vars = {}
    exec(qiskit_code, {}, local_vars)
    if isinstance(local_vars.get(name_qc), QuantumCircuit):
        q_circuit = local_vars[name_qc]
        qubits = q_circuit.qubits
        clbits = q_circuit.clbits
        time_stamps  = q_circuit.data
        num_rows  = len(qubits) + len(clbits) + 1
        num_columns = len(time_stamps) + 1
        matrix = np.full((num_rows, num_columns), "", dtype='<U100')
        matrix[0][0] = None
        for index_col in range(1, num_columns):
            matrix[0][index_col] = str(index_col)
        for index_row in range(0, len(qubits)):
            matrix[index_row+1][0] = "qb-" + str(index_row) 
        for index_row in range(0, len(clbits)):
            matrix[index_row+len(qubits)+1][0] = "cb-" + str(index_row) 
        for index_col in range(1, num_columns):
            circuit_instruction = time_stamps[index_col-1]
            operation = circuit_instruction[0]
            operation_name = get_id_operation(operation)
            operation_qubits = circuit_instruction[1]
            for operation_qubit in operation_qubits:
                matrix[get_id_qubit(operation_qubit)+1][index_col] = operation_name
    return matrix

def get_id_qubit(qubit: Qubit):
    return qubit.index

def get_id_operation(operation: Instruction):
    params_types = []
    for param in operation.params:
        params_types.append(str(type(param).__name__))
    id = "%s(%s)" % (operation.name, ','.join(params_types))
    return(id)

def add_transpilation_code_to_source_file(file_path, current_code, names_qc, name_transpilation, optimization):
    t = Transpilation()
    new_code = ""
    new_code += "from qiskit import transpile\n"
    new_code += current_code
    for n_qc in names_qc:
        new_code += f"\n{n_qc} = transpile({n_qc}, basis_gates={t.LIST_GATES[name_transpilation]}, optimization_level={optimization})"
    with open(file_path, 'w') as file:
        file.write(new_code)
    
def get_result_static_analysis(file_path, current_code, names_qc: str, name_transpilation: str, optimization: int):
    (lpq, nc) = (LPQ(), NC())
    if (name_transpilation is not None) and (name_transpilation != 'None'):
        add_transpilation_code_to_source_file(file_path, current_code, names_qc, name_transpilation, optimization)
    tree = None
    with open(file_path, "r") as fp:
        tree = ast.parse(fp.read())
    result_sa = ""
    result_sa += f"Risultato quantum smell LPQ: {lpq.get_result(tree)}\n"
    result_sa += f"Risultato quantum smell NC: {nc.get_result(tree)}\n"
    return result_sa

def get_results_dynamic_analysis(file_path, current_code, names_qc: str, name_transpilation: str, optimization: int, id_r: int):
    (idq, iq, im, lc, roc, cg) = (IdQ(), IQ(), IM(), LC(), ROC(), CG())
    if (name_transpilation is not None) and (name_transpilation != 'None'):
        add_transpilation_code_to_source_file(file_path, current_code, names_qc, name_transpilation, optimization)
    results_da = []
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    for index in range (0, len(names_qc)):
        matrix = get_matrix(file_path, names_qc[index])
        result = ""
        result += f"Risultato quantum smell IdQ: {idq.get_result(matrix)}\n"
        result += f"Risultato quantum smell IQ: {iq.get_result(matrix)}\n"
        result += f"Risultato quantum smell IM: {im.get_result(matrix)}\n"
        result += f"Risultato quantum smell LC: {lc.get_result(matrix)}\n"
        result += f"Risultato quantum smell ROC: {roc.get_result(matrix)}\n"
        result += f"Risultato quantum smell CG: {cg.get_result(matrix)}\n"
        formatter_matrix = {'numpystr': lambda x: f'{x:<5}' if x.strip() else "''"}
        matrix = np.array2string(matrix, formatter=formatter_matrix)
        rda = ResultDynamicAnalysis()
        (rda.id, rda.name_q_circuit, rda.number_q_circuit, rda.matrix, rda.result, rda.id_result) = (
            0, names_qc[index], index + 1, matrix, result, id_r
        )
        results_da.append(rda)
    return results_da
        

    
    
    
    
        









