class Analysis:
    def __init__(self, id=0, name_transpilation=None, optimization=0, save_date="", id_q_system=0):
        self.id = id
        self.name_transpilation = name_transpilation
        self.optimization = optimization
        self.save_date = save_date
        self.id_q_system = id_q_system

    def __str__(self):
        return (f"Analysis(id={self.id}: {type(self.id)}, name_transpilation={self.name_transpilation}: {type(self.name_transpilation)}, " 
                f"optimization={self.optimization}: {type(self.optimization)}, save_date={self.save_date}: {type(self.save_date)}, "
                f"id_q_system={self.id_q_system})")
    
    def __eq__(self, other):
        if isinstance(other, Analysis):
            return (
                self.id == other.id
                and self.name_transpilation == other.name_transpilation
                and self.optimization == other.optimization
                and self.save_date == other.save_date
                and self.id_q_system == other.id_q_system
            )
        return False










