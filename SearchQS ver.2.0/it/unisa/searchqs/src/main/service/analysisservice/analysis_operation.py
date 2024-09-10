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
import inspect 
from math import pi
import ast
import sys
import importlib
import os
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import importlib.util
import tempfile


def import_user_module(module_name, file_path):
    module_dir = os.path.dirname(file_path)
    module_path = os.path.join(module_dir, module_name + '.py')
    
    """ 
    1.  Otteniamo la directory che contiene il file specificato da file_path e creiamo un percorso completo per un modulo Python 
        combinando module_dir e module_name con l’estensione .py 
    """
    if os.path.exists(module_path):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    else:
        print(f"Impossibile trovare il modulo {module_name}")
        return None
    """
    2.  Se riusciamo a trovare il modulo module_name allora:
            carichiamo dinamicamente un modulo Python e restituiamo il modulo caricato.
        altrimenti: 
            stampiamo la frase f"Impossibile trovare il modulo {module_name}" e ritorniamo come output None. 
    """

def get_function_calls(file_path):
    sys.path.append(os.path.dirname(file_path))
    sys.path.append(file_path.split('\\')[0])
    tree = None
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
    defined_functions = set()
    function_calls = []
    """
    1.  Aggiungiamo la directory che contiene file_path e la radice del percorso di file_path alla lista dei percorsi di ricerca dei moduli 
        facendo in modo di impostare i moduli dalla directory file_path e in modo da assicurarsi che il percorso di ricerca includa 
        la radice del percorso di file_path. 
        Successivamente, apriamo il file specificato da file_path in lettura e lo assegnamo alla variabile file all’interno del blocco with. 
        Nel blocco with assegnamo alla variabile tree l'albero sintattico (Abstract Syntax Tree) del file specificato da file_path.
    """
    class FunctionDefVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            defined_functions.add(node.name)
            self.generic_visit(node)
    def_visitor = FunctionDefVisitor()
    def_visitor.visit(tree)
    global_vars = globals()
    local_vars = locals()
    """
    2.  Il metodo visit_FunctionDef della classe FunctionDefVisitor identifica e memorizzare tutti i nomi delle funzioni e dei metodi 
        definiti nel file specificato da file_path. Creiamo quindi un'istanza del metodo visit_FunctionDef e lo assegnamo alla variabile def_visitor.
        Con def_visitor.visit(tree) iniziamo la visita dell'albero sintattico tree utilizzando l'istanza def_visitor.
        alle variabili global_vars e local_vars assegnamo rispettivamente il dizionario delle variabili globali e il dizionario delle variabili locali.
    """
    def trace_calls(frame, event, arg):
        if event != 'call':
            return
        code = frame.f_code
        func_name = code.co_name
        if func_name in defined_functions:
            args = frame.f_locals
            function_calls.append((func_name, list(args.values())))
        return trace_calls
    """
    3.  La funzione trace_calls monitora le chiamate di funzione durante l’esecuzione del programma. 
        Quando una funzione definita nel file specificato viene chiamata, trace_calls registra il nome della funzione e i valori degli argomenti 
        passati a quella funzione in una lista chiamata function_calls.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                try:
                    global_vars[alias.asname or alias.name] = importlib.import_module(alias.name)
                except ImportError as e:
                    print(f"Errore di importazione: {e}")
                    user_module = import_user_module(alias.name, file_path)
                    if user_module:
                        global_vars[alias.asname or alias.name] = user_module
        elif isinstance(node, ast.ImportFrom):
            try:
                module = importlib.import_module(node.module)
                if node.names[0].name == '*':
                    for attr in dir(module):
                        if not attr.startswith('_'):
                            global_vars[attr] = getattr(module, attr)
                else:
                    for alias in node.names:
                        global_vars[alias.asname or alias.name] = getattr(module, alias.name)
            except ImportError as e:
                print(f"Errore di importazione: {e}")
                user_module = import_user_module(node.module, file_path)
                if user_module:
                    if node.names[0].name == '*':
                        for attr in dir(user_module):
                            if not attr.startswith('_'):
                                global_vars[attr] = getattr(user_module, attr)
                    else:
                        for alias in node.names:
                            global_vars[alias.asname or alias.name] = getattr(user_module, alias.name)
            except AttributeError as e:
                print(f"Errore di attributo: {e}")
    """
    4.  Il ciclo for esterno attraversa tutti i nodi dell’albero sintattico del file Python. 
        Se trova un'istruzione di importazione (Import), tenta di importare i moduli e li assegna a variabili globali. 
        Se trova un’istruzione di importazione da un modulo (ImportFrom), importa gli attributi specificati o tutti gli attributi del modulo 
        e li assegna a variabili globali. Gestisce anche eventuali errori di importazione o di attributo, tentando di importare i moduli con 
        una funzione personalizzata se necessario. 
    """
    function_defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    for node in function_defs:
        exec(compile(ast.Module([node]), filename="<ast>", mode="exec"), global_vars, local_vars)
    non_function_defs = [node for node in tree.body if not isinstance(node, ast.FunctionDef)]
    try:
        exec(compile(ast.Module(non_function_defs), filename="<ast>", mode="exec"), global_vars, local_vars)
    except ImportError as e:
        missing_module = str(e).split("'")[1]
        print(f"Modulo mancante: {missing_module}")
        user_module = import_user_module(missing_module, file_path)
        if user_module:
            global_vars[missing_module] = user_module
            exec(compile(ast.Module(non_function_defs), filename="<ast>", mode="exec"), global_vars, local_vars)
    """
    5.  Eseguiamo le definizioni di funzione e il resto del codice separatamente. 
        Prima compiliamo ed eseguiamo le definizioni di funzione, poi compiliamo ed eseguiamo il codice rimanente, 
        gestendo eventuali errori di importazione e tentando di importare moduli mancanti. 
    """
    sys.settrace(trace_calls)
    try:
        exec(compile(tree, filename="<ast>", mode="exec"), global_vars, local_vars)
    finally:
        sys.settrace(None)
    function_calls_without_duplicates = []
    for item in function_calls:
        if not any(np.array_equal(item, unique_item) for unique_item in function_calls_without_duplicates):
            function_calls_without_duplicates.append(item)
    return function_calls_without_duplicates
    """
    6.  Impostiamo la funzione di tracciamento: Utilizza trace_calls per monitorare le chiamate di funzione.
        Eseguiamo l’intero albero sintattico (AST): Compiliamo ed eseguiamo il codice, gestendo eventuali errori e assicurandosi di rimuovere 
        la funzione di tracciamento alla fine.
        Rimuoviamo le chiamate di funzione duplicate: Filtriamo le chiamate di funzione per eliminare i duplicati e restituiamo la lista senza duplicati.
    """

def get_names_q_circuits_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            qiskit_code = file.read()
            tree = ast.parse(qiskit_code)
            names_q_circuits = set()
            # Funzione per verificare se un nodo è all'interno di una funzione
            def is_inside_function(node):
                while node:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        return True
                    node = getattr(node, 'parent', None)
                return False
            # Aggiungiamo il riferimento al nodo padre per ogni nodo
            for node in ast.walk(tree):
                for child in ast.iter_child_nodes(node):
                    child.parent = node
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name_function = node.name
                    for sub_node in ast.walk(node):
                        if isinstance(sub_node, ast.Assign) and isinstance(sub_node.value, ast.Call):
                            func = sub_node.value.func
                            if (isinstance(func, ast.Name) and func.id == 'QuantumCircuit') or \
                               (isinstance(func, ast.Attribute) and func.attr == 'QuantumCircuit'):
                                name_q_circuit = sub_node.targets[0].id
                                names_q_circuits.add((name_q_circuit, name_function))
                elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                    if not is_inside_function(node):
                        func = node.value.func
                        if (isinstance(func, ast.Name) and func.id == 'QuantumCircuit') or \
                           (isinstance(func, ast.Attribute) and func.attr == 'QuantumCircuit'):
                            name_q_circuit = node.targets[0].id
                            names_q_circuits.add((name_q_circuit, None))
            return list(names_q_circuits)
    except FileNotFoundError:
        raise Exception("File non trovato")
    """
    Questo blocco di codice legge un file Python contenente codice Qiskit, analizza l’albero sintattico (AST) per trovare tutte le istanze 
    di QuantumCircuit e raccoglie i nomi dei circuiti quantistici definiti, sia all’interno che all’esterno delle funzioni. 
    Restituisce una lista di tuple contenenti i nomi dei circuiti e i nomi delle funzioni in cui sono definiti, se presenti. 
    Se il file non viene trovato, solleva un’eccezione. 
    """

def get_method_parameters(file_path, method_name):
    # Leggi il contenuto del file
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Esegui il contenuto del file in un namespace separato
    namespace = {}
    exec(file_content, namespace)
    
    # Ottieni il metodo dal namespace
    method = namespace.get(method_name)
    
    if method is None:
        return f"Il metodo {method_name} non è stato trovato nel file."
    
    # Ottieni i parametri del metodo
    parameters = inspect.signature(method).parameters
    return list(parameters.keys())

def get_function_body_code(file_path, function_name):
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    # Parse il contenuto del file
    tree = ast.parse(file_content)
    
    # Trova la funzione specificata
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Ottieni il codice della funzione
            start_line = node.body[0].lineno - 1
            end_line = node.body[-1].end_lineno
            function_body = file_content.splitlines()[start_line:end_line]
            
            # Calcola la lunghezza dello spazio nella prima riga del corpo
            indent_length = len(function_body[0]) - len(function_body[0].lstrip())
            
            # Rimuovi l'indentazione
            function_body = [line[indent_length:] for line in function_body]
            
            # Sostituisci 'return' con 'sys.exit()' mantenendo l'argomento
            function_body = [line.replace('return ', 'sys.exit(') + ')' if line.strip().startswith('return ') else line for line in function_body]
            
            return '\n'.join(function_body)
    
    return f"La funzione {function_name} non è stata trovata nel file."

def make_matrix(circuit):
    num_qubits = circuit.num_qubits
    num_clbits = circuit.num_clbits
    num_columns = len(circuit.data)
    matrix = np.full((num_qubits + num_clbits + 1, num_columns + 1), "", dtype='<U100')
    matrix[0][0] = None
    for index_col in range(1, num_columns + 1):
        matrix[0][index_col] = index_col
    for index_row in range(0, num_qubits):
        matrix[index_row+1][0] = f'qb-{index_row}'
    for index_row in range(num_qubits + 1, num_clbits + num_qubits + 1):
        matrix[index_row][0] = f'cb-{((index_row-1) % num_clbits)}'
    time_stamps  = circuit.data
    for index_col in range(1, num_columns + 1):
        circuit_instruction = time_stamps[index_col-1]
        operation = circuit_instruction[0]
        operation_name = get_id_operation(operation)
        operation_qubits = circuit_instruction[1]
        for operation_qubit in operation_qubits:
            matrix[get_id_qubit(operation_qubit)+1][index_col] = operation_name
    return matrix
    """
    Questo blocco di codice crea una matrice che rappresenta un circuito quantistico. 
    La matrice include informazioni sui qubit, i bit classici e le operazioni eseguite nel circuito. 
    Ogni colonna rappresenta un’operazione nel circuito, mentre le righe rappresentano i qubit e i bit classici. 
    La matrice viene popolata con i nomi delle operazioni eseguite su ciascun qubit in ogni colonna. 
    """

def get_matrices_method(file_path, name_qc, name_method, function_calls):
    matrices = set()
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    for function_call in function_calls:
        if function_call[0] != name_method:
            continue
        params = function_call[1]
        method = getattr(foo, name_method)
        circuit = method(*params)
        # Ottieni la matrice del circuito
        matrix = make_matrix(circuit)
        matrices.add(tuple(map(tuple, matrix)))
    matrices = [np.array(matrix) for matrix in matrices]
    return (matrices, function_calls)

def get_matrix(file_path, name_qc):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    foo = importlib.util.module_from_spec(spec)
    sys.path.append(os.path.dirname(file_path))
    try:
        spec.loader.exec_module(foo)
    except Exception as e:
        print(f"Errore durante il caricamento del modulo: {e}")
    circuit = getattr(foo, name_qc)
    matrices = []
    matrix = make_matrix(circuit)
    matrices.append(matrix)
    return matrices
    """
    Questo blocco di codice carica dinamicamente un modulo Python da un file specificato, estrae un circuito quantistico dal modulo, 
    crea una matrice che rappresenta il circuito e restituisce una lista contenente questa matrice. 
    Se c'è un errore durante il caricamento del modulo, stampa un messaggio di errore.
    """
    
def get_id_qubit(qubit: Qubit):
    return qubit.index
    """
    Questa funzione prende un oggetto Qubit e restituisce il suo indice (index).
    """

def get_id_operation(operation: Instruction):
    params_types = []
    for param in operation.params:
        params_types.append(str(type(param).__name__))
    id = "%s(%s)" % (operation.name, ','.join(params_types))
    return(id)
    """
    Questa funzione prende un’istruzione (Instruction), raccoglie i tipi dei parametri dell’operazione, e restituisce una stringa 
    che rappresenta l’operazione con i tipi dei parametri inclusi.
    """

def get_num_spaces_and_spaces(string):
    count = 0
    spaces = ''
    for char in string:
        if char == ' ':
            spaces += ' '
            count += 1
        else:
            break
    return {'num_spaces': count, 'spaces': spaces}
    """
    Questa funzione conta il numero di spazi all’inizio di una stringa e restituisce un dizionario con il numero di spazi (num_spaces) 
    e una stringa contenente quegli spazi (spaces). 
    """

def add_transpilation_code_to_source_file(file_path, current_code, names_qc, name_transpilation, optimization):
    t = Transpilation()
    old_code = current_code.split('\n')
    new_code = "from qiskit import transpile\n"
    methods_stack = []
    for current_line in old_code:
        if current_line == '':
            new_code += current_line + '\n'
            continue
        spaces_current_line = get_num_spaces_and_spaces(current_line)
        while methods_stack != []:
            if spaces_current_line['num_spaces'] <= methods_stack[-1]['num_spaces']:
                methods_stack.pop()
            else:
                break
        if current_line.startswith(f'{spaces_current_line['spaces']}def'):
            method_name = current_line.strip().split('(')[0].split()[1]
            methods_stack.append({
                'method_name': method_name, 
                'num_spaces': spaces_current_line['num_spaces'], 
                'spaces': spaces_current_line['spaces']
            })
            new_code += current_line + '\n'
        elif current_line.startswith(f'{spaces_current_line['spaces']}return'):
            additional_code = ""
            for name_qc in names_qc:
                if (methods_stack != []) and (name_qc[1] == methods_stack[-1]['method_name']):
                    new_line = f"{spaces_current_line['spaces']}{name_qc[0]} = transpile({name_qc[0]}, basis_gates={t.LIST_GATES[name_transpilation]}, optimization_level={optimization})\n"
                    additional_code += new_line
                if (methods_stack == []) and (name_qc[1] is None):
                    new_line = f"{spaces_current_line['spaces']}{name_qc[0]} = transpile({name_qc[0]}, basis_gates={t.LIST_GATES[name_transpilation]}, optimization_level={optimization})\n"
                    additional_code += new_line
            current_line = additional_code + current_line
            new_code += current_line + '\n'
        else:
            new_code += current_line + '\n'
    for name_qc in names_qc:
        if name_qc[1] is None:
            new_line = f"{name_qc[0]} = transpile({name_qc[0]}, basis_gates={t.LIST_GATES[name_transpilation]}, optimization_level={optimization})\n"
            new_code += new_line
    with open(file_path, 'w') as file:
        file.write(new_code)
    """
    Questa funzione aggiunge codice di traspilazione a un file sorgente Python contenente codice Qiskit. 
    Analizza il codice esistente, identifica le definizioni di funzione e le istruzioni return, e inserisce il codice di traspilazione 
    per i circuiti quantistici specificati. Infine, scrive il nuovo codice nel file sorgente. 
    """

def add_transpilation_code_to_code(current_code, names_qc, name_transpilation, optimization):
    t = Transpilation()
    # Dividi il codice corrente in righe
    old_code = current_code.split('\n')
    new_code = "from qiskit import transpile\n"
    methods_stack = []
    i=0
    for current_line in old_code:
        i=i+1
        if current_line == '':
            new_code += current_line + '\n'
            continue
        spaces_current_line = get_num_spaces_and_spaces(current_line)
        while methods_stack != []:
            if spaces_current_line['num_spaces'] <= methods_stack[-1]['num_spaces']:
                methods_stack.pop()
            else:
                break
        if current_line.startswith(f'{spaces_current_line['spaces']}def'):
            method_name = current_line.strip().split('(')[0].split()[1]
            methods_stack.append({
                'method_name': method_name, 
                'num_spaces': spaces_current_line['num_spaces'], 
                'spaces': spaces_current_line['spaces']
            })
            new_code += current_line + '\n'
        elif current_line.startswith(f'{spaces_current_line['spaces']}return'):
            additional_code = ""
            for name_qc in names_qc:
                if (methods_stack != []) and (name_qc[1] == methods_stack[-1]['method_name']):
                    new_line = f"{spaces_current_line['spaces']}{name_qc[0]} = transpile({name_qc[0]}, basis_gates={t.LIST_GATES[name_transpilation]}, optimization_level={optimization})\n"
                    additional_code += new_line
                if (methods_stack == []) and (name_qc[1] is None):
                    new_line = f"{spaces_current_line['spaces']}{name_qc[0]} = transpile({name_qc[0]}, basis_gates={t.LIST_GATES[name_transpilation]}, optimization_level={optimization})\n"
                    additional_code += new_line
            current_line = additional_code + current_line
            new_code += current_line + '\n'
        else:
            new_code += current_line + '\n'
    for name_qc in names_qc:
        if name_qc[1] is None:
            new_line = f"{name_qc[0]} = transpile({name_qc[0]}, basis_gates={t.LIST_GATES[name_transpilation]}, optimization_level={optimization})\n"
            new_code += new_line
    return new_code

def get_result_static_analysis(file_path, current_code, names_qc, name_transpilation: str, optimization: int):
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
    """
    Questa funzione esegue un’analisi statica su un file sorgente Python contenente codice Qiskit. 
    Se specificato, aggiunge codice di traspilazione al file. Poi, legge e analizza l’albero sintattico del file, 
    esegue dei controlli per verificare se siano presenti i quantum code smells LPQ e NC e restituisce i risultati ottenuti.
    """

def format_matrix(matrix):
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*matrix)]
    formatted_matrix = []
    for row in matrix:
        formatted_row = "  ".join(f"{str(cell) if cell else '\' \'':<{col_widths[i]}}" for i, cell in enumerate(row))
        formatted_matrix.append(formatted_row)
    return "\n".join(formatted_matrix)


def get_results_dynamic_analysis(file_path, current_code, names_qc, function_calls, 
                                     name_transpilation, optimization, id_r):
    (idq, iq, im, lc, roc, cg) = (IdQ(), IQ(), IM(), LC(), ROC(), CG())
    if (name_transpilation is not None) and (name_transpilation != 'None'):
        add_transpilation_code_to_source_file(file_path, current_code, names_qc, name_transpilation, optimization)
    results_da = []
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    for index in range (0, len(names_qc)):
        matrices = []
        if names_qc[index][1] is not None:
            (matrices, function_calls) = get_matrices_method(file_path, names_qc[index][0], names_qc[index][1], function_calls)
        else:
            matrices = get_matrix(file_path, names_qc[index][0])
        if matrices == []:
            continue
        for matrix in matrices:
            result = ""
            result += f"Risultato quantum smell IdQ: {idq.get_result(matrix)}\n"
            result += f"Risultato quantum smell IQ: {iq.get_result(matrix)}\n"
            result += f"Risultato quantum smell IM: {im.get_result(matrix)}\n"
            result += f"Risultato quantum smell LC: {lc.get_result(matrix)}\n"
            result += f"Risultato quantum smell ROC: {roc.get_result(matrix)}\n"
            result += f"Risultato quantum smell CG: {cg.get_result(matrix)}\n"
            matrix = format_matrix(matrix)
            rda = ResultDynamicAnalysis()
            (rda.id, rda.name_q_circuit, rda.number_q_circuit, rda.name_method, rda.matrix, rda.result, rda.id_result) = (
                0, names_qc[index][0], index + 1, names_qc[index][1], matrix, result, id_r
            )
            results_da.append(rda)
    return results_da
    """
    Questa funzione esegue un’analisi dinamica su un circuito quantistico di un file sorgente Python contenente codice Qiskit. 
    Se specificato, aggiunge codice di traspilazione al file. Poi, per ogni circuito quantistico, crea una matrice che rappresenta il circuito, 
    esegue dei controlli per verificare se siano presenti i quantum code smells IdQ, IQ, IM, LC, ROC, CG 
    e restituisce i risultati ottenuti con l'analisi dinamica in una lista di oggetti entity ResultDynamicAnalysis chiamata results_da.
    """









