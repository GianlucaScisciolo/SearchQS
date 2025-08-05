from src.main.model.dao.dao.dao_impl import DAOImpl
from src.main.model.entity.analysis import Analysis
from src.main.model.dao.analysisdao.i_analysis_dao import IAnalysisDAO

class AnalysisDAOImpl(DAOImpl, IAnalysisDAO):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    """ Queries """

    # Create

    CREATE = """
INSERT INTO analysis (name_transpilation, optimization, save_date, id_q_system) 
VALUES (%s, %s, %s, %s);
    """

    # Read
    READ_BY_ID_Q_SYSTEM_WITHOUT_TRANSPILATION = """
SELECT 
    id, name_transpilation, optimization, save_date, id_q_system 
FROM 
    analysis 
WHERE 
    id_q_system = %s and name_transpilation is NULL;
    """

    READ_BY_NAME_TRANSPILATION_AND_ID_Q_SYSTEM = """
SELECT 
    id, name_transpilation, optimization, save_date, id_q_system 
FROM 
    analysis 
WHERE 
    name_transpilation = %s AND id_q_system = %s;
    """

    READ_ID_ANALYSES_BY_ID_Q_SYSTEM = """
SELECT 
    id 
FROM 
    analysis 
WHERE 
    id_q_system = %s;
    """

    READ_NUM_ANALYSES_BY_ID_Q_SYSTEM = """
SELECT 
    COUNT(*) AS num_analysis 
FROM 
    analysis 
WHERE 
    id_q_system = %s;
    """

    READ_ID_BY_PARAMS = """
SELECT 
    id
FROM 
    analysis 
WHERE 
    name_transpilation = %s AND optimization = %s AND save_date = %s AND id_q_system = %s;
    """

    READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE = """
SELECT 
    id
FROM 
    analysis 
WHERE 
    name_transpilation is NULL AND optimization = %s AND save_date = %s AND id_q_system = %s;
    """

    # Update

    # Delete

    DELETE_BY_ID = """
DELETE FROM analysis 
WHERE 
    id = %s;
    """

    """ Methods """

    # Create

    def create(self, a):
        is_created = self.execute_action(self.CREATE, (a.name_transpilation, a.optimization, a.save_date, a.id_q_system), 1)
        if is_created:
            return is_created
        raise Exception
    
    # Read

    def read_by_id_q_system_without_transpilation(self, id_qs):
        analyses = self.execute_select(self.READ_BY_ID_Q_SYSTEM_WITHOUT_TRANSPILATION, (id_qs,))
        if analyses is None:
            raise Exception
        for index in range(0, len(analyses)):
            a = Analysis()
            (a.id, a.name_transpilation, a.optimization, a.save_date, a.id_q_system) = analyses[index]
            analyses[index] = a
        return analyses

    def read_by_name_transpilation_and_id_q_system(self, name_transpilation, id_qs):
        analyses = self.execute_select(self.READ_BY_NAME_TRANSPILATION_AND_ID_Q_SYSTEM, (name_transpilation, id_qs))
        if analyses is None:
            raise Exception
        for index in range(0, len(analyses)):
            a = Analysis()
            (a.id, a.name_transpilation, a.optimization, a.save_date, a.id_q_system) = analyses[index]
            analyses[index] = a
        return analyses

    def read_id_analyses_by_id_q_system(self, id_qs):
        id_analyses = self.execute_select(self.READ_ID_ANALYSES_BY_ID_Q_SYSTEM, (id_qs,))
        if id_analyses is None:
            raise Exception
        for index in range(0, len(id_analyses)):
            id_analyses[index] = id_analyses[index][0]
        return id_analyses

    def read_num_analyses_by_id_q_system(self, id_qs):
        num_analyses = self.execute_select(self.READ_NUM_ANALYSES_BY_ID_Q_SYSTEM, (id_qs,))
        if num_analyses is None:
            raise Exception
        if num_analyses != []:
            num_analyses = num_analyses[0][0]
        else:
            num_analyses = 0
        return num_analyses
    
    def read_id_by_params(self, a):
        id = self.execute_select(self.READ_ID_BY_PARAMS, (a.name_transpilation, a.optimization, a.save_date, a.id_q_system))
        if id is None:
            raise Exception
        if id != []:
            id = id[0][0]
        return id
    
    def read_id_by_params_with_name_transpilation_none(self, a):
        id = self.execute_select(self.READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE, (a.optimization, a.save_date, a.id_q_system))
        if id is None:
            raise Exception
        if id != []:
            id = id[0][0]
        return id
    
    # Update

    # Delete

    def delete_by_id(self, id):
        delete = self.execute_action(self.DELETE_BY_ID, (id,), 1)
        if delete:
            return delete
        return Exception









