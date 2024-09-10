import numpy as np
import pandas as pd

class ResultDynamicAnalysis:
    def __init__(self, id=0, name_q_circuit="", number_q_circuit=0, name_method=None, matrix=[], result="", id_result=0):
        self.id = id
        self.name_q_circuit = name_q_circuit
        self.number_q_circuit = number_q_circuit
        self.name_method = name_method
        self.matrix = matrix
        self.result = result
        self.id_result = id_result

    def __str__(self):
        return (f"ResultDynamicAnalysis(id={self.id}, name_q_circuit={self.name_q_circuit}, " 
                f"number_q_circuit={self.number_q_circuit}, name_method={self.name_method}, matrix={self.matrix}, " 
                f"result='{self.result}, id_result='{self.id_result}')")
    
    def __eq__(self, other):
        if isinstance(other, ResultDynamicAnalysis):
            return (
                self.id == other.id
                and self.name_q_circuit == other.name_q_circuit
                and self.number_q_circuit == other.number_q_circuit 
                and self.name_method == other.name_method 
                and np.array_equal(self.matrix, other.matrix)
                and self.result == other.result
                and self.id_result == other.id_result
            )
        return False










