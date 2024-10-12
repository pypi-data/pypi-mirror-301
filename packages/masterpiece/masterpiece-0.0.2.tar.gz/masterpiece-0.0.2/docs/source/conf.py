"""
Configuration file for the Sphinx documentation builder.

TODO: as a professional python developer not going to copy & paste this to
every plugin and project.

 For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sys
import os

# Find the directory of the main conf.py file
conf_path = os.path.abspath('../../src/masterpiece/sphinx/conf.py')

# Open the main conf.py file and execute its content in this context
with open(conf_path, 'r') as conf_file:
    exec(conf_file.read())
