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
        """
        Questo metodo analizza un albero di sintassi astratta (AST) per contare quante volte le funzioni execute e run vengono chiamate, 
        con particolare attenzione a quelle chiamate all’interno di loop (for o while). 
        Inoltre, conta quante volte viene chiamata la funzione bind_parameters. Ecco come funziona:
        1.  Identificazione delle linee dei loop:
                Scorre tutti i nodi dell’AST.
                Se il nodo è un loop (for o while), aggiunge le linee di codice del loop a una lista loops_lines.
        2.  Conteggio delle chiamate a execute e run:
                Inizializza un contatore num_executions a 0.
                Scorre tutti i nodi dell’AST.
                Se il nodo è una chiamata di funzione (ast.Call):
                Controlla se la funzione chiamata è execute o run.
                Incrementa il contatore num_executions per ogni chiamata trovata.
                Se la chiamata si trova all’interno di un loop, incrementa ulteriormente il contatore.
        3.  Conteggio delle chiamate a bind_parameters:
                Inizializza un contatore num_bind_parameters a 0.
                Scorre tutti i nodi dell’AST.
                Se il nodo è una chiamata di funzione (ast.Call) e la funzione chiamata è bind_parameters, incrementa il contatore num_bind_parameters.
        4.  Calcolo del risultato:
                Inizializza self.value a 0.
                Se il numero di chiamate a execute e run è maggiore del numero di chiamate a bind_parameters, assegna a self.value la differenza 
                tra num_executions e num_bind_parameters.
        """









