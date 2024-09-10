from abc import ABC, abstractmethod

class IDAO(ABC):
    @abstractmethod
    def execute_select(self, select_query, attributes=()):
        """ """
    
    @abstractmethod
    def execute_action(self, query, attributes=(), num_tuples_consider=0):
        """ """









