from src.main.service.analysisservice.qcsmell.i_q_c_smell import IQCSmell
import ast

class NC(IQCSmell):

    def __init__(self):
        self.name = "Non-parameterized Circuit"
        self.acronym = "NC"
        self.value = 0
    
    def get_result(self, tree):
        loops_lines = []
        for node in ast.walk(tree):
            if isinstance(node, ast.For) or isinstance(node, ast.While):
                loop_start = node.lineno
                loop_end = node.body[-1].lineno
                loops_lines.extend(range(loop_start, loop_end+1))
        num_executions = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                function = node.func
                arguments = node.args
                if isinstance(function, ast.Name):
                    id = function.id
                    if id == 'execute' and len(arguments) >= 2:
                        num_executions += 1
                        if node.lineno in loops_lines:
                            num_executions += 1
                elif isinstance(function, ast.Attribute):
                    attribute = function.attr
                    if attribute == 'execute' and len(arguments) >= 1:
                        num_executions += 1
                        if node.lineno in loops_lines:
                            num_executions += 1
            elif isinstance(node, ast.Expr):
                value = node.value
                if isinstance(value, ast.Call):
                    function = value.func
                    arguments = value.args
                    if isinstance(function, ast.Attribute):
                        attribute = function.attr
                        if attribute == 'run' and len(arguments) >= 1:
                            num_executions += 1
                            if node.lineno in loops_lines:
                                num_executions += 1
        num_bind_parameters = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node, ast.Expr):
                    value = node.value
                    if isinstance(value, ast.Call):
                        function = value.func
                        arguments = value.args
                        if isinstance(function, ast.Attribute):
                            attribute = function.attr
                            if attribute == 'bind_parameters' and len(arguments) >= 1:
                                num_bind_parameters += 1
        self.value = 0
        if num_executions > num_bind_parameters:
            self.value = num_executions - num_bind_parameters
        return self.value









