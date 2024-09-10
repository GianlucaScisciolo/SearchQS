import sys
sys.path.append("../../../../../..")

import unittest
from unittest.mock import Mock
import ast
import numpy as np
from src.main.service.analysisservice.qcsmell.lpq import LPQ

class TestLPQ(unittest.TestCase):

    def test_1_init(self):
        lpq = LPQ()
        oracle = ["no-alignment between the Logical and Physical Qubits", "LPQ", 0]
        self.assertEqual(lpq.name, oracle[0])
        self.assertEqual(lpq.acronym, oracle[1])
        self.assertEqual(lpq.value, oracle[2])
    
    def test_2_is_initial_layout_used_true(self):
        lpq = LPQ()
        mock_key_words = Mock()
        mock_key_words.arg = 'initial_layout'
        self.assertTrue(lpq.is_initial_layout_used([mock_key_words]))

    def test_3_is_initial_layout_used_false(self):
        lpq = LPQ()
        mock_key_words = Mock()
        mock_key_words.arg = 'not_initial_layout'
        self.assertFalse(lpq.is_initial_layout_used([mock_key_words]))

    def test_4_result_ast_name(self):
        file_path = "SistemaQuantistico/file_test_1.py"
        tree = None
        with open(file_path, "r") as source:
            tree = ast.parse(source.read())
        lpq = LPQ()
        oracle = 4
        result = lpq.get_result(tree)
        self.assertEqual(result, oracle)

    def test_5_result_ast_attribute(self):
        file_path = "SistemaQuantistico/file_test_2.py"
        tree = None
        with open(file_path, "r") as source:
            tree = ast.parse(source.read())
        lpq = LPQ()
        oracle = 5
        result = lpq.get_result(tree)
        self.assertEqual(result, oracle)

    def test_6_result_ast_call(self):
        file_path = "SistemaQuantistico/file_test_3.py"
        tree = None
        with open(file_path, "r") as source:
            tree = ast.parse(source.read())
        lpq = LPQ()
        oracle = 4
        result = lpq.get_result(tree)
        self.assertEqual(result, oracle)










