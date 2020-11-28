from PyQt5.QtWidgets import QTreeView

class DeselectableTreeView(QTreeView):
    def mousePressEvent(self, event):
        self.clearSelection()
        QTreeView.mousePressEvent(self, event)
