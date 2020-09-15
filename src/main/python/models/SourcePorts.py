from config import Config
from models import Model

def source_port_loader():
    config = Config.Instance()
    source_ports_config = config['SOURCEPORTS']

    source_ports = [{'name': source_port,
                     'template': source_ports_config[source_port]}
                     for source_port in source_ports_config]
    
    return source_ports

class SourcePorts(Model):
    def __init__(self):
        Model.__init__(self, loader=source_port_loader)
        self.load()
