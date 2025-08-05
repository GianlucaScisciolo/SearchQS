class Transpilation:
    LIST_GATES = {
        'original': ['u1', 'u2', 'u3', 'rz', 'sx', 'x', 'cx', 'id'],
        'simple': ['cx', 'u3'],
        'ibm_perth': ['cx', 'id', 'rz', 'sx', 'x'],
        'ibm_sherbroke': ['ecr', 'id', 'rz', 'sx', 'x'],
        'rpcx': ['cx', 'rx', 'ry', 'rz', 'p']
    }

    LIST_NAMES_TRANSPILATION = ['original', 'simple', 'ibm_perth', 'ibm_sherbroke', 'rpcx']









