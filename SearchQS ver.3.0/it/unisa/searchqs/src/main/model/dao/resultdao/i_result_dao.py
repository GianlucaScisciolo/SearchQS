from abc import ABC, abstractmethod

class IResultDAO(ABC):
    # Create

    @abstractmethod
    def create(self, r):
        """ """

    # Read

    @abstractmethod
    def read_by_id_analysis(self, id_a):
        """ """

    @abstractmethod
    def read_id_source_files_by_id_analysis(self, id_a):
        """ """

    @abstractmethod
    def read_num_results_by_id_source_file(self, id_sf):
        """ """

    @abstractmethod
    def read_id_by_params(self, r):
        """ """

    # Update

    # Delete