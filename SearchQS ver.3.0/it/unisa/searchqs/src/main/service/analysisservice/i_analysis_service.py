from abc import ABC, abstractmethod

class IAnalysisService(ABC):
    @abstractmethod
    def display_analysis_area(self):
        """ """
    
    @abstractmethod
    def display_form_loading_q_system(self, attributes):
        """ """

    @abstractmethod
    def loading_q_system(self, attributes):
        """ """

    @abstractmethod
    def execution_analyses(self, attributes):
        """ """
    
    @abstractmethod
    def display_names_transpilation(self):
        """ """
    
    @abstractmethod
    def display_analyses_transpilation_selected(self, attributes):
        """ """
    
    @abstractmethod
    def display_analysis(self, attributes):
        """ """

    @abstractmethod
    def display_form_deletion_analysis(self):
        """ """

    @abstractmethod
    def deletion_analysis(self, attributes):
        """ """













