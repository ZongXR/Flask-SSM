# -*- coding: utf-8 -*-
import os
from package.name.utils.StringUtils import to_snake
from package.name.utils.DirUtils import recurse_files
from package.name.service.BaseService import BaseService


for file in os.listdir(os.path.dirname(__file__)):
    if file.startswith("__"):
        continue
    full_file = os.path.join(os.path.dirname(__file__), file)
    if os.path.isfile(full_file):
        module_name = file[:-3]
        exec("from %s.%s import %s" % (__name__, module_name, module_name))
        var_name = to_snake(module_name)
        exec("%s = %s()" % (var_name, module_name))
    else:
        files = recurse_files(full_file)
        for sub_file in files:
            module_name = os.path.basename(sub_file)
            path_name = os.path.dirname(sub_file)
            if module_name.startswith("__"):
                continue
            package_name = __name__ + path_name.replace(os.path.dirname(__file__), "").replace(os.sep, ".")
            if "__" in package_name:
                continue
            module_name = module_name[:-3]
            exec("from %s.%s import %s" % (package_name, module_name, module_name))
            var_name = to_snake(module_name)
            exec("%s = %s()" % (var_name, module_name))