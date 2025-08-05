from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell

class IdQ(IQCSmell):
    def __init__(self):
        self.name = "Idle Qubits"
        self.acronym = "IdQ"
        self.value = 0

    def get_result(self, matrix):
        [num_rows, num_columns] = matrix.shape
        for bit in range(1, num_rows):
            if matrix[bit][0].startswith('qb-') == False:
                break
            counter = -1
            max_num_ops_in_between = 0
            for time_stamp in range(1, num_columns):
                operation = matrix[bit][time_stamp]
                if operation.lower().startswith('barrier'):
                    continue
                if operation == '': 
                    if counter == -1:
                        pass
                    elif counter != -1:
                        counter += 1
                elif operation != '':
                    if counter == -1:
                        counter = 0
                    elif counter != -1:
                        if counter >= max_num_ops_in_between:
                            max_num_ops_in_between = counter
                        counter = 0
            if max_num_ops_in_between >= self.value:
                self.value = max_num_ops_in_between
        return self.value
        """
        Questa funzione analizza una matrice che rappresenta un circuito quantistico. 
        Conta il numero massimo di operazioni consecutive tra due operazioni non vuote per ciascun qubit. 
        Ignora le operazioni di tipo “barrier”. 
        Restituisce il valore massimo trovato tra tutte le operazioni consecutive.
        """



        









