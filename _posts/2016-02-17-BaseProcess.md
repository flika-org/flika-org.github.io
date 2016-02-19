---
layout: documentation
title: BaseProcess
category: Documentation
---
# BaseProcess.py
--------------
This file creates the abstract classes and components to create Process Dialogs for user defined analysis parameters.
## class WindowSelector(QWidget):
>    Widget for selecting a Window to be referred to by a process
    Signals
        -valueChanged: emitted when a window is selected by the user

## class FileSelector(QWidget):
>    Widget that opens a dialog to allow the user to select a file
    Signals
        -valueChanged: emitted when a file is selected by the user

## class SliderLabel(QWidget):
>    Widget instance of QSpinBox with visible Label next to it.
    Signals
        -valueChanged: emitted when the slider is moved
    Functions:
```python
    def __init__(self,decimals=0)
        -decimals represents resolution. 0 for integers, 1 for tens place, etc.
    def setRange(self,minn,maxx)
    def setMinimum(self,minn)
    def setMaximum(self,maxx)
    def setValue(self,value)
    def setSingleStep(self,value)
```

## class SliderLabelOdd(SliderLabel):
>    SliderLabel subclass that forces the user to pick an odd value
    refer to SliderLabel

## class CheckBox(QCheckBox):
>    Overwritten QCheckBox class to give it the 'setValue' method
        def setValue(self,value):

## class BaseDialog(QDialog):
>    Dialog for users to manipulate widgets to set analysis parameters.  Items aligned in a FormLayout with cancel, ok, and a docstring displayed at the top of the dialog.
    Signals
        -changeSignal: emitted when any item widget value in the BaseDialog is changed
        -closeSignal: emitted when the base dialog box is closed, whether accepted or cancelled
#### def __init__(self,items,title,docstring):
    Parameters:
        -items: list of dicts specifying widgets. Each dict comprised of
            {'string': 'Label Text',
             'object': widgetItem,
             'name': 'name used to get item value'}
        -title: Title displayed at the top of the dialog window
        -docstring: Information to display above the widget items

## class BaseProcess(object):
>    Abstract class provided for process creation. Contains methods for displaying a BaseDialog of items, manipulating an image stack, and outputting a new window with the applied changes.  IMPORTANT: BaseProcess requires the user to have a currentWindow selected. For processes that don't need initial windows, refer to BaseProcess_noPriorWindow
####  def gui(self):
    Create a gui to display the widgets for analysis arguments. General template:
```python
    self.gui_reset()
    #... build self.items list
    super().gui() # this shows the gui dialog
```
####  def __call__(self, *args):
    Called when BaseDialog is accepted. self.items widgets are passed in by (name, value) pairs, parameter names must match names stated in gui function.
    NOTE:
        -To create a new window with manipulated image, use this template:
```python
        #... get widget values and apply manipulation
        self.newtif = resulting image
        self.newname = "Name of Image after manipulation"
        self.command = "command as string used to create window" (Optional: used in scripts)
        return self.end()
```
#### def getValue(self,name):
    Get the value of a widget item "name" in the self.items dict

## class BaseProcess_noPriorWindow(BaseProcess):
    Abstract class of type BaseProcess that ignores g.m.currentWindow