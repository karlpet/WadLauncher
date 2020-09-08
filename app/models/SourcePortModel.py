from config import Config

class SourcePortModel:
    def __init__(self):
        config = Config.Instance()

        self.source_ports = [source_port for source_port in config['SOURCEPORTS']]
        self.selected_source_port_index = 0

    def get_source_ports(self):
        return self.source_ports

    def get_selected_source_port_index(self):
        return self.selected_source_port_index

    def select_source_port(self, index):
        self.select_source_port_index = index
