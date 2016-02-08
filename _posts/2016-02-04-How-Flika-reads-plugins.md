---
title: How Flika reads plugins
category: Plugins
---
# How Flika reads plugins
Plugins are handled in Flika with the plugin_data.txt file in the FLIKA/plugins repository. This text file is outlined like a python dictionary, where each key-value pair is a plugin name and the URL location of its \_\_init\_\_.py.  An example plugin_data.txt file would look like:


```python
{
'Plugin1 Name' : 'http://www.Plugin1/path/to/\_\_init\_\_.py', #usually a raw github url
'Plugin2 Name': 'http://www.Plugin2/path/to/\_\_init\_\_.py'
}
```
