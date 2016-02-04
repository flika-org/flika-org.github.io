---
title: How Flika reads plugins
category: Plugins
---
# How Flika reads plugins
Plugins are handled in Flika with the plugins.txt file in the FLIKA_plugins repository. This text file is outlined like a python dictionary, where each key-value pair is a plugin name and another dictionary of information about that plugin.  An example plugins.text file would look like:


```python
{
'Plugin1 Name' : {
    'description': 'Short paragraph(s) about the plugin, written by the plugin author to show in the plugin manager dialog',
    'url': 'www.url_download.com/path/to/zip_file.zip', # Github encouraged
    'docs': 'www.url_docs.com/docs',
    'author': 'Author Name',
    'date': 'MM/DD/YY',
    },
'Plugin2 Name': {
    'description': 'etc.. etc..',
    'url': 'www.url_download.com/path/to/zip_file.zip',
    'docs': 'www.url_docs.com/docs',
    'author': 'Author Name',
    'date': 'MM/DD/YY',
    }
}
```

IMPORTANT: 
    url zip files must have a single folder containing the plugin code, as well as an \_\_init\_\_.py file. To see the outline of an init file check 'How to write plugins for FLIKA'
    The names listed must match EXACTLY to the names listed in the \_\_init\_\_.py files of FLIKA plugins.
    Update Availability relies on dates listed in plugins.txt and \_\_init\_\_.py files of FLIKA plugins.

The names listed must match EXACTLY to the names listed in the __init__.py files of FLIKA plugins.
    Update Availability relies on dates listed in plugins.txt and __init__.py files of FLIKA plugins.
