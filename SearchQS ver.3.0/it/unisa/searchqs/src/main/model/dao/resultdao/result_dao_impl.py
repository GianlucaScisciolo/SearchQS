from src.main.model.dao.resultdao.i_result_dao import IResultDAO
from src.main.model.dao.dao.dao_impl import DAOImpl
from src.main.model.entity.result import Result

class ResultDAOImpl(DAOImpl, IResultDAO):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    """ Queries """

    # Create

    CREATE = """
INSERT INTO result (result_static_analysis, id_analysis, id_source_file) 
VALUES (%s, %s, %s);
    """

    # Read
    READ_BY_ID_ANALYSIS = """
SELECT 
    id, result_static_analysis, id_analysis, id_source_file 
FROM 
    result 
WHERE 
    id_analysis = %s;
    """

    READ_ID_SOURCE_FILES_BY_ID_ANALYSIS = """
SELECT 
    id_source_file 
FROM 
    result 
WHERE 
    id_analysis = %s;
    """

    READ_NUM_RESULTS_BY_ID_SOURCE_FILE = """
SELECT 
    COUNT(*) AS num_results 
FROM 
    result 
WHERE 
    id_source_file = %s;
    """

    READ_ID_BY_PARAMS = """
SELECT 
    id 
FROM 
    result 
WHERE result_static_analysis = %s AND id_analysis = %s AND id_source_file = %s;
    """

    # Update

    # Delete

    """ Methods """

    # Create

    def create(self, r):
        is_created = self.execute_action(self.CREATE, (r.result_static_analysis, r.id_analysis, r.id_source_file), 1)
        if is_created:
            return is_created
        raise Exception

    # Read

    def read_by_id_analysis(self, id_a):
        results = self.execute_select(self.READ_BY_ID_ANALYSIS, (id_a,))
        if results is None:
            raise Exception
        for index in range(0, len(results)):
            r = Result()
            (r.id, r.result_static_analysis, r.id_analysis, r.id_source_file) = results[index]
            results[index] = r
        return results

    def read_id_source_files_by_id_analysis(self, id_a):
        id_source_files = self.execute_select(self.READ_ID_SOURCE_FILES_BY_ID_ANALYSIS, (id_a,))
        if id_source_files is None:
            raise Exception
        for index in range(0, len(id_source_files)):
            id_source_files[index] = id_source_files[index][0]
        return id_source_files

    def read_num_results_by_id_source_file(self, id_sf):
        num_results = self.execute_select(self.READ_NUM_RESULTS_BY_ID_SOURCE_FILE, (id_sf,))
        if num_results is None:
            raise Exception
        if num_results == []:
            num_results = 0
        else:
            num_results = num_results[0][0]
        return num_results

    def read_id_by_params(self, r):
        id = self.execute_select(self.READ_ID_BY_PARAMS, (r.result_static_analysis, r.id_analysis, r.id_source_file))
        if id is None:
            raise Exception
        if id == []:
            id = 0
        else:
            id = id[0][0]
        return id

    # Update

    # Delete









