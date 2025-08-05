from src.main.model.dao.dao.dao_impl import DAOImpl
from src.main.model.dao.residentialaddressdao.i_residential_address_dao import IResidentialAddressDAO
from src.main.model.entity.residential_address import ResidentialAddress

class ResidentialAddressDAOImpl(DAOImpl, IResidentialAddressDAO):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    """ Queries """

    # Create

    CREATE = """
INSERT INTO residential_address (name, number, city, province, cap) 
VALUES (%s, %s, %s, %s, %s);
    """

    # Read

    READ_BY_ID = """
SELECT 
    id, name, number, city, province, cap 
FROM 
    residential_address 
WHERE
    id = %s;
    """

    READ_ID_BY_PARAMS = """
SELECT 
    id 
FROM 
    residential_address 
WHERE 
    name = %s AND number = %s AND city = %s AND province = %s AND cap = %s;
    """

    # Update

    # Delete

    DELETE_BY_ID = """
DELETE FROM residential_address 
WHERE 
    id = %s;
    """

    """ Methods """

    # Create

    def create(self, ra):
        attributes = (ra.name, ra.number, ra.city, ra.province, ra.cap) 
        create = self.execute_action(self.CREATE, attributes, 1)
        if create:
            return create
        raise Exception
    
    # Read

    def read_by_id(self, id):
        residential_address = self.execute_select(self.READ_BY_ID, (id,))
        if residential_address is None:
            raise Exception
        if residential_address != []:
            ra = ResidentialAddress()
            (ra.id, ra.name, ra.number, ra.city, ra.province, ra.cap) = residential_address[0]
            residential_address = ra
        return residential_address 

    def read_id_by_params(self, ra):
        params = (ra.name, ra.number, ra.city, ra.province, ra.cap)
        id = self.execute_select(self.READ_ID_BY_PARAMS, params)
        if id is None:
            raise Exception
        if id != []:
            id = (id[0])[0]
        return id

    # Update

    # Delete

    def delete_by_id(self, id):
        delete = self.execute_action(self.DELETE_BY_ID, (id,), 1)
        if delete:
            return delete
        raise Exception









