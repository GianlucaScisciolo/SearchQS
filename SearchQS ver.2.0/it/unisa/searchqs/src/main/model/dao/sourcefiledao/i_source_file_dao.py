from abc import ABC, abstractmethod

class ISourceFileDAO(ABC):
    
    # Create

    @abstractmethod
    def create(self, sf):
        """ """
        
    # Read

    @abstractmethod
    def read_by_id(self, id: int):
        """ """
    
    @abstractmethod
    def read_by_params(self, sf):
        """ """
    
    # Update

    # Delete

    @abstractmethod
    def delete_by_id(self, id):
        """ """









