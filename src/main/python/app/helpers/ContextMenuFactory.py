from PyQt5.QtWidgets import QMenu

def make_context_menu(root, menu_items):
    menu = QMenu(root)

    callbacks_dict = {}
    for title, callback in menu_items.items():
        menu_action = menu.addAction(title)
        callbacks_dict[menu_action] = callback

    def execute_menu(mouse_position):
        action = menu.exec_(root.mapToGlobal(mouse_position))
        if action:
            callbacks_dict[action]()

    return execute_menu