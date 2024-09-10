from abc import ABC, abstractmethod

class IUserAreaService(ABC):
    @abstractmethod
    def display_user_area(self):
        """ """
        
    @abstractmethod
    def display_form_deletion_account(self, attributes):
        """ """
    
    @abstractmethod
    def deletion_account(self):
        """ """
    
    @abstractmethod
    def display_personal_data(self):
        """ """

    @abstractmethod
    def modification_personal_data(self, attributes):
        """ """









