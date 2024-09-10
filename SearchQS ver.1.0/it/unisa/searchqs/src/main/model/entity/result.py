class Result:
    def __init__(self, id=0, result_static_analysis="", id_analysis=0, id_source_file=0):
        self.id = id
        self.result_static_analysis = result_static_analysis
        self.id_analysis = id_analysis
        self.id_source_file = id_source_file

    def __str__(self):
        return (f"Result(id={self.id}, result_static_analysis={self.result_static_analysis}, " 
                f"id_analysis={self.id_analysis}, id_source_file={self.id_source_file})")
    
    def __eq__(self, other):
        if isinstance(other, Result):
            return (
                self.id == other.id
                and self.result_static_analysis == other.result_static_analysis
                and self.id_analysis == other.id_analysis
                and self.id_source_file == other.id_source_file
            )
        return False









