from views.LaunchBarView import LaunchBarView

class LaunchBarController:
    def __init__(self, root, iwad_model):
        self.view = LaunchBarView(root,
                                  iwad_model.get_iwads(),
                                  iwad_model.get_selected_iwad_index(),
                                  iwad_model.select_iwad)