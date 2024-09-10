from abc import ABC, abstractmethod

class IResidentialAddressDAO(ABC):

    # Create
    
    @abstractmethod
    def create(self, ra):
        """ """
    
    # Read

    @abstractmethod
    def read_by_id(self, id):
        """ """ 

    @abstractmethod
    def read_id_by_params(self, ra):
        """ """
    
    # Update

    # Delete

    @abstractmethod
    def delete_by_id(self, id):
        """ """









