from abc import ABC, abstractmethod

class IAuthenticationService(ABC):
    @abstractmethod
    def display_form_registration(self):
        """ """
    
    @abstractmethod
    def registration(self, attributes):
        """ """
    
    @abstractmethod
    def display_form_login(self):
        """ """

    @abstractmethod
    def login(self, attributes):
        """ """
    
    @abstractmethod
    def logout(self):
        """ """









