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

            if isinstance(obj, QComboBox):
                values = []  # the list that will hold all values from QCombobox
                name = obj.objectName()  # get the QCombobox object's name
                for i in range(obj.count()):  # QCombobox contains a number of items
                    itemData = obj.itemText(i)
                    values.append(itemData)  # put those items into a list for saving
                index = obj.findText(obj.currentText())  # return the index of the item, assign to selected
                self.settings.setValue(name + "Values", values)  # save all the values in settings
                self.settings.setValue(name + "Index", index)  # save the indexed value in settings

    def guirestore(self):

        # Restore geometry  
        # self.ui.resize(self.settings.value('size', QtCore.QSize(500, 500)))
        # self.ui.move(self.settings.value('pos', QtCore.QPoint(60, 60)))

        for name, obj in inspect.getmembers(self.ui):
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

            if isinstance(obj, QComboBox):
                name = obj.objectName()
                values = self.settings.value(name + "Values")  # values will be a list.
                # clear all the objects
                # so that we don't run into issues
                # with restoring the list of values
                obj.clear()
                for i in range(len(values)):
                    value = values[i]
                    if not (value == '' or value == ""):
                        # if there are some values in the list, we should add them to the Combobox
                            obj.insertItem(i, value)

                index = self.settings.value(
                    name + "Index")  # next we want to select the item in question by getting it's index, pull the index from the .ini file
                obj.setCurrentIndex(int(index))