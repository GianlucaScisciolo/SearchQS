from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell

class CG(IQCSmell):
    def __init__(self):
        self.name = "use of Customized Gates"
        self.acronym = "CG"
        self.value = 0
        self.unitary_calls = ['unitary', 'hamiltonian', 'singlequbitunitary'] 

    def get_result(self, matrix):
        [num_rows, num_columns] = matrix.shape
        for bit in range(1, num_rows):
            if (matrix[bit][0]).startswith('qb-') == False:
                break
            for time_stamp in range(1, num_columns):
                operation = (matrix[bit][time_stamp]).lower().split('(')[0]
                if operation in self.unitary_calls:
                    self.value += 1
        return self.value
        """
        Questa funzione analizza una matrice che rappresenta un circuito quantistico. 
        Conta il numero di operazioni unitarie eseguite sui qubit, incrementando un valore ogni volta che trova un’operazione unitaria. 
        Restituisce il valore totale delle operazioni unitarie trovate.
        """













