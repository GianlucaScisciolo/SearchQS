from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell

class LC(IQCSmell):
    def __init__(self):
        self.name = "Long Circuit"
        self.acronym = "LC"
        self.value = 0

    def get_result(self, matrix):
        [num_rows, num_columns] = matrix.shape
        for bit in range(1, num_rows):
            if matrix[bit][0].startswith('cb-'):
                num_rows = bit
                break
        max_num_ops_qubit = 0
        for bit in range(1, num_rows):
            counter = 0
            for time_stamp in range(1, num_columns):
                operation = matrix[bit][time_stamp]
                if operation == "" or operation.lower().startswith('barrier'):
                    continue
                counter = counter + 1
            if max_num_ops_qubit < counter:
                max_num_ops_qubit = counter
        max_num_ops_time_stamp = 0
        for time_stamp in range(1, num_columns):
            counter = 0
            for bit in range(1, num_rows):
                operation = matrix[bit][time_stamp]
                if operation == "" or operation.lower().startswith('barrier'):
                    continue
                counter = counter + 1
            if max_num_ops_time_stamp < counter:
                max_num_ops_time_stamp = counter
        self.value = max_num_ops_qubit * max_num_ops_time_stamp
        return self.value 
        """
        Questa funzione analizza una matrice che rappresenta un circuito quantistico. 
        Conta il numero massimo di operazioni per qubit e per timestamp, ignorando le operazioni di tipo “barrier”. 
        Calcola il prodotto tra il massimo numero di operazioni per qubit e il massimo numero di operazioni per timestamp, e restituisce questo valore.
        """
        






        









