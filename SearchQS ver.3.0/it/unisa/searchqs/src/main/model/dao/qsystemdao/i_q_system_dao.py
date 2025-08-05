from abc import ABC, abstractmethod

class IQSystemDAO(ABC):

    # Create

    @abstractmethod
    def create(self, qs):
        """ """

    # Read
    
    @abstractmethod
    def read_by_email_registered_user(self, email_ru):
        """ """

    @abstractmethod
    def read_by_name_and_email_registered_user(self, name, email_ru):
        """ """
    
    @abstractmethod
    def read_id_q_systems_by_email_registered_user(self, email_ru):
        """ """
    
    @abstractmethod
    def read_id_by_attributes(self, qs):
        """ """

    # Update

    # Delete

    @abstractmethod
    def delete_by_id(self, id):
        """ """









