import inspect
from distutils.util import strtobool
from PyQt4 import QtCore

from PyQt4.QtGui import *


class Qtickle(object):
    def __init__(self, ui, settings):
        self.ui = ui
        self.settings = settings

    def guisave(self):

        # Save geometry
        # self.settings.setValue('size', self.ui.size())
        # self.settings.setValue('pos', self.ui.pos())

        for name, obj in inspect.getmembers(self.ui):
            # if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
            if isinstance(obj, QComboBox):
                name = obj.objectName()  # get combobox name
                index = obj.currentIndex()  # get current index from combobox
                text = obj.itemText(index)  # get the text for current index
                self.settings.setValue(name, text)  # save combobox selection to registry

            if isinstance(obj, QLineEdit):
                name = obj.objectName()
                value = obj.text()
                self.settings.setValue(name, value)  # save self.ui values, so they can be restored next time

            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                state = obj.isChecked()
                self.settings.setValue(name, state)

            if isinstance(obj, QRadioButton):
                name = obj.objectName()
                value = obj.isChecked()  # get stored value from registry
                self.settings.setValue(name, value)

            if isinstance(obj, QSpinBox):
                name = obj.objectName()
                value = obj.value()  # get stored value from registry
                self.settings.setValue(name, value)

            if isinstance(obj, QSlider):
                name = obj.objectName()
                value = obj.value()  # get stored value from registry
                self.settings.setValue(name, value)

            if isinstance(obj, QLabel):
                name = obj.objectName()
                value = obj.text()
                self.settings.setValue(name, value)

    def guirestore(self):

        # Restore geometry  
        # self.ui.resize(self.settings.value('size', QtCore.QSize(500, 500)))
        # self.ui.move(self.settings.value('pos', QtCore.QPoint(60, 60)))

        for name, obj in inspect.getmembers(self.ui):
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current region from combobox
                # text   = obj.itemText(index)   # get the text for new selected index
                name = obj.objectName()

                value = (self.settings.value(name))

                if value == "":
                    continue

                index = obj.findText(value)  # get the corresponding index for specified string in combobox

                if index == -1:  # add to list if not found
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)  # preselect a combobox value by index

            if isinstance(obj, QLineEdit):
                name = obj.objectName()
                value = (self.settings.value(name).decode('utf-8'))  # get stored value from registry
                obj.setText(value)  # restore lineEditFile

            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                value = self.settings.value(name)  # get stored value from registry
                if value != None:
                    obj.setChecked(strtobool(value))  # restore checkbox

            if isinstance(obj, QRadioButton):
                name = obj.objectName()
                value = self.settings.value(name)  # get stored value from registry
                if value != None:
                    obj.setChecked(strtobool(value))

            if isinstance(obj, QSlider):
                name = obj.objectName()
                value = self.settings.value(name)  # get stored value from registry
                if value != None:
                    obj.setValue(int(value))  # restore value from registry

            if isinstance(obj, QSpinBox):
                name = obj.objectName()
                value = self.settings.value(name)  # get stored value from registry
                if value != None:
                    obj.setValue(int(value))  # restore value from registry

            if isinstance(obj, QLabel):
                name = obj.objectName()
                value = self.settings.value(name)
                if value != None:
                    obj.setText(value)
