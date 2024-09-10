from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell

class IQ(IQCSmell):
    def __init__(self):
        self.name = "Initialization of Qubits"
        self.acronym = "IQ"
        self.value = 0

    def get_result(self, matrix):
        [num_rows, num_columns] = matrix.shape
        for bit in range(1, num_rows):
            if matrix[bit][0].startswith('qb-') == False:
                break
            max_num_ops_between_init_and_use = 0
            counter = -1
            for time_stamp in range(1, num_columns):
                operation = matrix[bit][time_stamp]
                if operation.lower().startswith('barrier'):
                    continue
                if operation == '':
                    if counter == -1:
                        pass
                    else:
                        counter = counter + 1
                else:
                    if counter == -1:
                        counter = 0
                    else:
                        if max_num_ops_between_init_and_use < counter:
                            max_num_ops_between_init_and_use = counter
                        break
            if self.value < max_num_ops_between_init_and_use:
                self.value = max_num_ops_between_init_and_use
        return self.value







        








