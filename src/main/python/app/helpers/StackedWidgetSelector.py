from PyQt5.QtWidgets import QStackedWidget

class WidgetIndices:
    IDGAMES_SEARCH = 0
    IDGAMES_DETAIL = 0
    WELCOME = 0

def add_widget(root, widget, widget_index):
    main_stack = root.findChild(QStackedWidget, 'main_stack')
    index = main_stack.addWidget(widget)
    setattr(WidgetIndices, widget_index, index)

def display_widget(root, widget_index):
    main_stack = root.findChild(QStackedWidget, 'main_stack')
    main_stack.setCurrentIndex(widget_index)