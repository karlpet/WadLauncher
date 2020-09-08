from views.LaunchBarView import LaunchBarView

class LaunchBarController:
    def __init__(self, root, iwad_model, source_port_model):
        self.view = LaunchBarView(root,
                                  iwad_model.get_iwads(),
                                  iwad_model.get_selected_iwad_index(),
                                  iwad_model.select_iwad,
                                  source_port_model.get_source_ports(),
                                  source_port_model.get_selected_source_port_index(),
                                  source_port_model.select_source_port
                                  )