from abc import ABC, abstractmethod

class IRegisteredUserDAO(ABC):
    
    # Create

    @abstractmethod
    def create(self, ru):
        """ """

    # Read

    @abstractmethod
    def read_by_email(self, email):
        """ """

    @abstractmethod
    def read_id_residential_address_by_email(self, email):
        """ """

    @abstractmethod
    def read_num_registered_user_by_id_residential_address(self, id_ra):
        """ """

    # Update

    @abstractmethod
    def update_by_params(self, ru, current_email):
        """ """ 
    
    # Delete

    @abstractmethod
    def delete_by_email(self, email):
        """ """