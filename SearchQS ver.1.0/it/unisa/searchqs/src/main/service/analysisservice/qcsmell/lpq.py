from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell
import ast

class LPQ(IQCSmell):

    def __init__(self):
        self.name = "no-alignment between the Logical and Physical Qubits"
        self.acronym = "LPQ"
        self.value = 0

    def is_initial_layout_used(self, key_words):
        for kw in key_words:
            if kw.arg == 'initial_layout':
                return True
        return False

    def get_result(self, tree):
        num_transpiles_without_initial_layout = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                function = node.func
                arguments = node.args
                key_words = node.keywords
                if isinstance(function, ast.Name):
                    id = function.id
                    if id == 'transpile' and len(arguments) >= 2:
                        if self.is_initial_layout_used(key_words) == False:
                            num_transpiles_without_initial_layout += 1
                elif isinstance(function, ast.Attribute):
                    attribute = function.attr
                    if attribute == 'transpile' and len(arguments) >= 1:
                        if self.is_initial_layout_used(key_words) == False:
                            num_transpiles_without_initial_layout += 1
            elif isinstance(node, ast.Expr):
                value = node.value
                if isinstance(value, ast.Call):
                    function = value.func
                    arguments = value.args
                    key_words = value.keywords
                    if isinstance(function, ast.Attribute):
                        attribute = function.attr
                        if attribute == 'transpile' and len(arguments) >= 1:
                            if self.is_initial_layout_used(key_words) == False:
                                num_transpiles_without_initial_layout += 1
        
        self.value = num_transpiles_without_initial_layout
        return self.value
    
    
    
    
    

                            





                        









