# -*- coding: utf-8 -*-
"""
Created on Sat Aug  13 21:56:35 2016

@author: Elena
"""

import re

field_dict = {}

def get_field_from_dict(regexp):
    global field_dict
    if field_dict.get(unicode(regexp.group(1))) != None:
        return field_dict.get(regexp.group(1))
    else:
        return regexp.group(0)

def set_field_dict(val):
    global field_dict    # Needed to modify global copy of globvar
    field_dict = val

def fill_fields_from_dict(field_dict, html_template):
    set_field_dict(field_dict)
    field_regexp = r'%%([A-Za-z_]*)'
    return re.sub(field_regexp, get_field_from_dict, html_template)

def get_field_list(html_template):	
    field_regexp = r'%%([A-Za-z_]*)'
    return re.findall(field_regexp, html_template)
