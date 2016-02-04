---
title: How to make a Flika plugin
category: Plugins
---

# How to make a Flika plugin

Plugins are software that extend Flika's functionality.  In this tutorial, we will describe how to create your own plugin to add to Flika.

In your plugin, if you'd like to import software from another Flika plugin, you can import by referencing the plugin directory.  For example, if the plugin is called 'puffs', the file containing the desired function is called 'threshold_cluster', and the function in that plugin is 'threshold_cluster', use the following syntax:


```python
from plugins.puffs.threshold_cluster import threshold_cluster
```

To add the plugin to the FLIKA database, it must be organized in a way that FLIKA can read.


```python
-PluginFolder
    -__init__.py
    -my_code.py
    -more_code.py
    -optional_docs
        -docs_files...
```

Where the \_\_init\_\_.py file must contain:


```python
dependencies = ['list', 'of', 'dependencies'] #installed from pypi and Gohkle's wheel library
name = 'Plugin Name'
date = 'MM/DD/YYYY' #date must be in this format to manage updates
base_dir = 'PluginFolderName' #module name used in plugin (eg. from PluginFolderName import submodule)
menu_layout = {'Menu Name': {'SubAction': ['path_to', 'function']}}
```

It should be noted that the above \_\_init\_\_.py file will add a submenu 'Menu Name' to the Plugins Menu, which has a subaction 'SubAction' that will import 'path_to' and run the 'function' attribute of the resulting import.  For instance if you have a window object in a plugin module, adding the window.show() function to the menu would look like:


```python
{'Menu Name': {'SubAction': ['path_to', 'function'], 'Show Window': ['PluginFolderName.module', 'window.show']}}
```

NOTE: Because this is a .py file, it may be helpful to include 'from collections import OrderedDict' in your \_\_init\_\_.py and create your menu_layout as an OrderedDict to maintain ordering. Above Example:


```python
    menu_layout = {'Menu Name': OrderedDict([('SubAction', ['path_to', 'function']), \
                                             ('Show Window', ['module', 'instance.show'])])}
```

When the author makes an update to a Plugin, he/she should set the date attribute to its new value, and alert authors of FLIKA.  Once the database has been updated as well, FLIKA users will be able to see and install the update.
