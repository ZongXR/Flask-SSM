# -*- coding: utf-8 -*-
import os
from package.name.utils.StringUtils import to_snake


for file in os.listdir(os.path.dirname(__file__)):
    module_name = file[:-3]
    if not module_name.startswith("__"):
        exec("from %s.%s import %s" % (__name__, module_name, module_name))
        var_name = to_snake(module_name)
        exec("%s = %s()" % (var_name, module_name))

