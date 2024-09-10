from src.main.model.dao.dao.dao_impl import DAOImpl
from src.main.model.dao.sourcefiledao.i_source_file_dao import ISourceFileDAO
from src.main.model.entity.source_file import SourceFile

class SourceFileDAOImpl(DAOImpl, ISourceFileDAO):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    """ Queries """

    # Create

    CREATE = """
INSERT INTO source_file (path, file) 
VALUES (%s, %s);
    """

    # Read

    READ_BY_ID = """
SELECT 
    id, path, file 
FROM 
    source_file 
WHERE 
    id = %s;
    """

    READ_BY_PARAMS = """
SELECT 
    id, path, file 
FROM 
    source_file 
WHERE 
    path = %s AND file = %s;
    """

    # Update

    # Delete

    DELETE_BY_ID = """
DELETE FROM source_file 
WHERE 
    id = %s;
    """

    """ Methods """

    # Create

    def create(self, sf):
        is_created = self.execute_action(self.CREATE, (sf.path, sf.file), 1)
        if is_created:
            return is_created
        raise Exception
        
    # Read

    def read_by_id(self, id: int):
        source_file = self.execute_select(self.READ_BY_ID, (id,))
        if source_file is None:
            raise Exception
        if source_file != []:
            sf = SourceFile()
            (sf.id, sf.path, sf.file) = source_file[0]
            source_file = sf
        return source_file
    
    def read_by_params(self, sf):
        source_file = self.execute_select(self.READ_BY_PARAMS, (sf.path, sf.file))
        if source_file is None:
            raise Exception
        if source_file != []:
            sf = SourceFile()
            (sf.id, sf.path, sf.file) = source_file[0]
            source_file = sf
        return source_file
    
    # Update

    # Delete

    def delete_by_id(self, id):
        is_deleted = self.execute_action(self.DELETE_BY_ID, (id,), 1)
        if is_deleted:
            return is_deleted
        raise Exception









