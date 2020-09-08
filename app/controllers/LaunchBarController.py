from views.LaunchBarView import LaunchBarView

class LaunchBarController:
    def __init__(self, root, wad_model, iwad_model, source_port_model):
        self.view = LaunchBarView(root,
                                  iwad_model.get_iwads(),
                                  iwad_model.get_selected_iwad_index(),
                                  iwad_model.select_iwad,
                                  source_port_model.get_source_ports(),
                                  source_port_model.get_selected_source_port_index(),
                                  source_port_model.select_source_port)

        wad_model.subscribe(self.wad_model_subscription)

    def wad_model_subscription(self, data):
        action, data = data

        if action == 'SELECT_WAD':
            self.view.update_selected_wad_name(data)
