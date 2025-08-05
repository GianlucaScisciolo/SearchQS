from abc import ABC, abstractmethod

class IAnalysisDAO(ABC):

    # Create

    @abstractmethod
    def create(self, a):
        """ """
    
    # Read
    
    @abstractmethod
    def read_by_id_q_system_without_transpilation(self, id_qs):
        """ """

    @abstractmethod
    def read_by_name_transpilation_and_id_q_system(self, name_transpilation, id_qs):
        """ """

    @abstractmethod
    def read_id_analyses_by_id_q_system(self, id_qs):
        """ """

    @abstractmethod
    def read_num_analyses_by_id_q_system(self, id_qs):
        """ """

    @abstractmethod
    def read_id_by_params(self, a):
        """ """

    @abstractmethod
    def read_id_by_params_with_name_transpilation_none(self, a):
        """ """

    # Update

    # Delete
    
    @abstractmethod
    def delete_by_id(self, id):
        """ """









