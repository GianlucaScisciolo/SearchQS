from src.main.model.dao.dao.dao_impl import DAOImpl
from src.main.model.dao.resultdynamicanalysisdao.i_result_dynamic_analysis_dao import IResultDynamicAnalysisDAO
from src.main.model.entity.result_dynamic_analysis import ResultDynamicAnalysis

class ResultDynamicAnalysisDAOImpl(DAOImpl, IResultDynamicAnalysisDAO):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    """ Queries """

    # Create

    CREATE = """
INSERT INTO result_dynamic_analysis (name_q_circuit, number_q_circuit, name_method, matrix, result, id_result) 
VALUES (%s, %s, %s, %s, %s, %s);
    """

    # Read
    
    READ_BY_ID_RESULT = """
SELECT 
    id, name_q_circuit, number_q_circuit, name_method, matrix, result, id_result 
FROM 
    result_dynamic_analysis 
WHERE 
    id_result = %s;
    """

    # Update

    # Delete

    """ Methods """

    # Create

    def create(self, rda):
        is_created = self.execute_action(self.CREATE, (rda.name_q_circuit, rda.number_q_circuit, rda.name_method, 
                                                       rda.matrix, rda.result, rda.id_result), 1)
        if is_created:
            return is_created
        raise Exception

    # Read

    def read_by_id_result(self, id_r):
        results_dynamic_analysis = self.execute_select(self.READ_BY_ID_RESULT, (id_r,))
        if results_dynamic_analysis is None:
            raise Exception
        for index in range(0, len(results_dynamic_analysis)):
            rda = ResultDynamicAnalysis()
            (rda.id, rda.name_q_circuit, rda.number_q_circuit, rda.name_method, 
             rda.matrix, rda.result, rda.id_result) = results_dynamic_analysis[index]
            results_dynamic_analysis[index] = rda
        return results_dynamic_analysis
    
    # Update

    # Delete









