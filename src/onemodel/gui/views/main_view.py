from os import path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtCore import pyqtSlot

from onemodel.gui.views.main_view_ui import Ui_MainWindow

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setup_ui(self)
        ####################################################################
        #   connect widgets to controllers
        ####################################################################

        # Return pressed in pathField.
        self._ui.pathField.returnPressed.connect(
                self.on_return_pressed_pathField
                )

        # Editing finished in pathField.
        self._ui.pathField.editingFinished.connect(
                self.on_editing_finished_pathField
                )

        # Double click on item in directoryTree.
        self._ui.directoryTree.tree.doubleClicked.connect(
                self.on_double_click_directoryTree
                )
        ####################################################################
        #   listen for model event signals
        ####################################################################

        # Current path is updated.
        self._model.current_path_changed.connect(self.on_current_path_changed)

    def on_return_pressed_pathField(self):
        new_path = self._ui.pathField.text()

        if path.isdir(new_path):
            self._main_controller.current_path_changed(new_path)
        else:
            # If not, show error message.
            title = 'Error Changing Folder'
            msg = f'Cannot find folder "{new_path}".\n'
            msg += 'Check the spelling and try again.'

            QtWidgets.QMessageBox.about(self, title, msg) 
            

    def on_editing_finished_pathField(self):
        self._ui.pathField.setText(self._model.current_path)

    def on_double_click_directoryTree(self, index):
        item_path = self._ui.directoryTree.model.filePath(index)

        if path.isfile(item_path):
            # TODO: Open file in the textEditor.
            pass

        elif path.isdir(item_path):
            # Change current path.
            self._main_controller.current_path_changed(item_path)

    def on_current_path_changed(self, path):
        print('on_current_path_changed')
        print(path)
        self._ui.pathField.setText(path)
        self._ui.directoryTree.tree.setRootIndex(
                self._ui.directoryTree.model.index(path)
                )


