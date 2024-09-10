from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell

class IM(IQCSmell):
    def __init__(self):
        self.name = "Intermediate Measurement"
        self.acronym = "IM"
        self.value = 0

    def get_result(self, matrix):
        [num_rows, num_columns] = matrix.shape
        num_measure_not_end = 0
        for bit in range(1, num_rows):
            num_measure_not_end_bit = 0
            if matrix[bit][0].startswith('qb-') == False:
                break
            measure_found = False
            for time_stamp in range(1, num_columns):
                operation = matrix[bit][time_stamp]
                if operation == '' or operation.lower().startswith('barrier'):
                    pass
                elif operation.lower().startswith('measure'):
                    num_measure_not_end_bit += 1
                    measure_found = True
                elif operation != '' and measure_found:
                    break
                if time_stamp == num_columns - 1:
                    num_measure_not_end_bit = 0
            num_measure_not_end += num_measure_not_end_bit

        self.value = num_measure_not_end
        return self.value
        """
        Questa funzione analizza una matrice che rappresenta un circuito quantistico. 
        Conta il numero di operazioni di misura che non si trovano alla fine del circuito per ciascun qubit. 
        Se un’operazione di misura è seguita da un’altra operazione, viene conteggiata. 
        Restituisce il numero totale di queste operazioni di misura non finali
        """








