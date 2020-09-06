from views.LaunchBarView import LaunchBarView

class LaunchBarController:
    def __init__(self, parentView):
        self.view = LaunchBarView(parentView.verticalLayout, parentView.verticalLayoutWidget)