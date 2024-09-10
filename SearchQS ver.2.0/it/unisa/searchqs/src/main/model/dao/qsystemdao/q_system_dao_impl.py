from src.main.model.dao.qsystemdao.i_q_system_dao import IQSystemDAO
from src.main.model.dao.dao.dao_impl import DAOImpl
from src.main.model.entity.q_system import QSystem


class QSystemDAOImpl(DAOImpl, IQSystemDAO):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    """ Queries """

    # Create
    CREATE = """
INSERT INTO q_system (name, email_registered_user) 
VALUES (%s, %s);
    """

    # Read
    READ_BY_EMAIL_REGISTERED_USER = """
SELECT 
    id, name, email_registered_user 
FROM 
    q_system 
WHERE 
    email_registered_user = %s;
    """

    READ_BY_NAME_AND_EMAIL_REGISTERED_USER = """
SELECT 
    id, name, email_registered_user 
FROM 
    q_system 
WHERE 
    name = %s AND email_registered_user = %s;
    """

    READ_ID_Q_SYSTEMS_BY_EMAIL_REGISTERED_USER = """
SELECT 
    id 
FROM 
    q_system 
WHERE 
    email_registered_user = %s;
    """

    READ_ID_BY_ATTRIBUTES = """
SELECT 
    id 
FROM 
    q_system 
WHERE 
    name = %s AND email_registered_user = %s;
    """

    # Update

    # Delete

    DELETE_BY_ID = """
DELETE FROM q_system 
WHERE 
    id = %s;
    """

    """ Methods """

    # Create

    def create(self, qs):
        attributes = (qs.name, qs.email_registered_user) 
        create = self.execute_action(self.CREATE, attributes, 1)
        if create:
            return create
        raise Exception
    
    # Read

    def read_by_email_registered_user(self, email_ru):
        q_systems = self.execute_select(self.READ_BY_EMAIL_REGISTERED_USER, (email_ru,))
        if q_systems is None:
            raise Exception
        for index in range(0, len(q_systems)):
            qs = QSystem()
            (qs.id, qs.name, qs.email_registered_user) = q_systems[index]
            q_systems[index] = qs
        return q_systems

    def read_by_name_and_email_registered_user(self, name, email_ru):
        q_system = self.execute_select(self.READ_BY_NAME_AND_EMAIL_REGISTERED_USER, (name, email_ru))
        if q_system is None:
            raise Exception
        if q_system != []:
            qs = QSystem() 
            (qs.id, qs.name, qs.email_registered_user) = q_system[0]
            q_system = qs
        return q_system
    
    def read_id_q_systems_by_email_registered_user(self, email_ru):
        id_q_systems = self.execute_select(self.READ_ID_Q_SYSTEMS_BY_EMAIL_REGISTERED_USER, (email_ru,))
        if id_q_systems is None:
            raise Exception
        for index in range(0, len(id_q_systems)):
            id_q_systems[index] = id_q_systems[index][0]
        return id_q_systems
    
    def read_id_by_attributes(self, qs):
        id = self.execute_select(self.READ_ID_BY_ATTRIBUTES, (qs.name, qs.email_registered_user))
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








