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

Where the \_\_init\_\_.py file must be a python dictionary with the following key-value pairs:


```python
{'name': 'Plugin Name',
'author': 'Author Name',
'description': 'Description of what your plugin does',
'base_dir': 'PluginFolderName',
		# Usually Plugin Name without spaces (eg. from PluginFolderName import submodule)
'dependencies': ['list', 'of', 'dependencies'],
		# installed from pypi and Gohkle's wheel library
'date': 'MM/DD/YYYY', 
		# date must be in this format to manage updates
'menu_layout': {'Menu Name': {'SubAction': ['path_to', 'function']}},
'docs': 'Documentation url'	
		# Optional
}
```

It should be noted that the above \_\_init\_\_.py file will add a submenu 'Menu Name' to the Plugins Menu, which has a subaction 'SubAction' that will import 'path_to' and run the 'function' attribute of the resulting import.  For instance if you have a window object in a plugin module, adding the window.show() function to the menu would look like:


```python
{'Menu Name': {'SubAction': ['path_to', 'function'], 'Show Window': ['PluginFolderName.module', 'window.show']}}
```

NOTE: Because this is a .py file, it may be helpful to use a list of tuples to create your menu_layout so the order of the menu is preserved. Above Example:


```python
    menu_layout = {'Menu Name': [('SubAction', ['path_to', 'function']), \
                                             ('Show Window', ['module', 'instance.show'])]}
```

IMPORTANT: 
	url zip files must have a single folder containing the plugin code, as well as an \_\_init\_\_.py file. To see the outline of an init file check 'How to write plugins for FLIKA'
	The names listed must match EXACTLY to the names listed in the \_\_init\_\_.py files of FLIKA plugins.
	When the author makes an update to a Plugin, he/she should set the date attribute to the current date and update this \_\_init\_\_ file.  FLIKA will automatically refer to the \_\_init\_\_ file to alert the user if updates are available.

