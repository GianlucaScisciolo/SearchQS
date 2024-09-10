from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell

class ROC(IQCSmell):
    def __init__(self):
        self.name = "Repeated set of Operations on Circuit"
        self.acronym = "ROC"
        self.value = 0

    def get_result(self, matrix):
        self.value = 0
        [num_rows, num_columns] = matrix.shape
        num_repetitions = 0
        time_stamp = 1
        while time_stamp < num_columns:
            max_slice_size_with_a_match = 0
            for slice_size in range(1, num_columns):
                slice = []
                for i1_ss in range(0, slice_size):
                    if time_stamp + i1_ss < num_columns:
                        for bit in range(1, num_rows):
                            operation = matrix[bit][time_stamp + i1_ss]
                            slice.append(operation)
                next_slice = []
                for i2_ss in range(0, slice_size):
                    if time_stamp + i1_ss + i2_ss + 1 < num_columns:
                        for bit in range(1, num_rows):
                            operation = matrix[bit][time_stamp + i1_ss + i2_ss + 1]
                            next_slice.append(operation)
                if slice == next_slice:
                    num_repetitions += 1
                    if slice_size > max_slice_size_with_a_match:
                        max_slice_size_with_a_match = slice_size
                    break
            if max_slice_size_with_a_match > 0:
                time_stamp += max_slice_size_with_a_match
            else:
                time_stamp += 1
        self.value = num_repetitions
        return self.value









