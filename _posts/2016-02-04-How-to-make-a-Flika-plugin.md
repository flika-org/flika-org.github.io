---
title: How to make a Flika plugin
category: Plugins
---

# How to make a Flika plugin

Plugins are software that extend Flika's functionality.  In this tutorial, we will describe how to create your own plugin to add to Flika.

In your plugin, if you'd like to import software from another Flika plugin, you can import by referencing the plugin directory.  For example, if the plugin is called 'puffs', the file containing the desired function is called 'threshold_cluster', and the function in that plugin is 'threshold_cluster', use the following syntax:



	from plugins.puffs.threshold_cluster import threshold_cluster


To add the plugin to the FLIKA database, it must be organized in a way that FLIKA can read.



	-PluginFolder
	    -__init__.py
	    -my_code.py
	    -more_code.py
	    -info.xml
	    -optional_docs
	        -docs_files...

Where the info.xml file must be be structured as follows:



	<plugin name="Plugin Name">
		<base_dir>
			PluginDirectory
		</base_dir>
		<date>
			MM/DD/YYYY
		</date>
		<author>
			Author Name
		</author>
		<description>
			A description about your plugin that will show in the plugin manager. This text body can contain paragraphs and links, but will only be parsed as plain text
		</description>
		<url>
			http://github.com/path/to/plugin.zip
		</url>
		<menu_layout>
			<action location="module" function="gui">Action Text</action>
			<!-- Subaction "Action Text" runs "gui()" imported by "from module import gui" -->
			
			<menu name="Menu 1">
				<action location="module.submodule" function="obj.func">Action 1</action>
				<!-- trigger found by from module.submodule import obj and running obj.func() -->

				<action location="loc2" function="f2">Action 2</action>
			</menu>
			
			<menu name="Menu 2">
				<action location="loc3" function="f3">Action 3</action>
				<menu name="Submenu">
					<action location="loc3.5" function="f3.5">Action Here</action>
				</menu>
			</menu>
		</menu_layout>
	</plugin>


It should be noted that the above info.xml file will create a Menu titled "Plugin Name" and add subaction "ActionText" and submenus "Menu 1", "Menu 2" with their child actions/menus.  The location and function attributes of the action tags help define what method is executed when the action is triggered.


### IMPORTANT: 
	URL zip files must have a single folder containing the plugin code, as well as an __init__.py and a sample.xml file.
	The base_dir and name must match EXACTLY with import statements in code and with the Flika plugin_data.txt file.
	When the author makes an update to a Plugin, he/she should set the date attribute to the current date and update the info.xml file.  FLIKA will automatically refer to this file to alert users if updates are available.

