from config import Config

class SourcePortModel:
    def __init__(self):
        self.config = Config.Instance()

        self.source_ports = [source_port for source_port in self.config['SOURCEPORTS']]
        self.selected_source_port_index = 0

    def get_source_ports(self):
        return self.source_ports

    def get_selected_source_port_index(self):
        return self.selected_source_port_index

    def select_source_port(self, index):
        self.selected_source_port_index = index

    def get_source_port_template(self):
        selected_source_port = self.source_ports[self.selected_source_port_index]

        return self.config['SOURCEPORTS'][selected_source_port]