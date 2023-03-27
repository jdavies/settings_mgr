# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Settings Manager",
    "author": "Jeff Davies - Cybernautic Studios",
    "version": (0, 0, 3),
    "blender": (3, 4, 1),
    "location": "View3D",
    "description": "Saves the Blender settings for easy loading in other projects",
    "warning": "Tested only with Blender v3.4.1",
    "doc_url": "",
    "category": "System",
}


#if "bpy" in locals():
#    import importlib
#    print('bpy is in locals!')
#    if "settings_mgr" in locals():
#        importlib.reload(settings_mgr)
#    if "file_settings" in locals():
#        importlib.reload(file_settings)

# I found this routine in DECALMachin3. Great for
# fully reloading all modules in the addon!
def reload_modules(name):
    import os
    import importlib

    # utils_modules = sorted([name[:-3] for name in os.listdir(os.path.join(__path__[0], "utils")) if name.endswith('.py')])

    # for module in utils_modules:
    #     impline = "from . utils import %s" % (module)

    #     print("reloading %s" % (".".join([name] + ['utils'] + [module])))

    #     exec(impline)
    #     importlib.reload(eval(module))

    print("reload_modules called!")

    from . import app_properties
    importlib.reload(app_properties)

    from . import settings_mgr
    importlib.reload(settings_mgr)

    from . import save_button_operator
    importlib.reload(save_button_operator)

    from . import load_button_operator
    importlib.reload(load_button_operator)

    from . import operator_file_import
    importlib.reload(operator_file_import)

    from . import updater
    importlib.reload(updater)

    # from . import registration
    # importlib.reload(registration)

    # modules = []

    # for label in registration.classes:
    #     entries = registration.classes[label]
    #     for entry in entries:
    #         path = entry[0].split('.')
    #         module = path.pop(-1)

    #         if (path, module) not in modules:
    #             modules.append((path, module))

    # for path, module in modules:
    #     if path:
    #         impline = "from . %s import %s" % (".".join(path), module)
    #     else:
    #         impline = "from . import %s" % (module)

    #     print("reloading %s" % (".".join([name] + path + [module])))

    #     exec(impline)
    #     importlib.reload(eval(module))


if 'bpy' in locals():
    reload_modules(bl_info['name'])

import bpy
import sys
import json
from bpy.utils import register_class, unregister_class
from random import randint
from bpy.props import (StringProperty, PointerProperty, BoolProperty, FloatProperty, IntProperty)
from bpy.types import (Panel, Operator, PropertyGroup)
from . import app_properties
from . import settings_mgr
from . import save_button_operator
from . import load_button_operator
from . import operator_file_import
from . import updater

print('Loading Settings Manager...')
print(bl_info)
print("update avail: " + str(updater.isUpdateAvailable(bl_info['version'])))
for p in sys.path:
    print(p)

_classes = [
    app_properties.AppProperties,
    settings_mgr.NPanel,
    save_button_operator.SaveButtonOperator,
    load_button_operator.LoadButtonOperator,
    operator_file_import.ImportSomeData,
]

def register():
    for cls in _classes:
        register_class(cls)
    # Register our properties
    bpy.types.Scene.my_props = PointerProperty(type=app_properties.AppProperties)
    # bpy.types.Context.my_props = PointerProperty(type=app_properties.AppProperties)


def unregister():
    for cls in _classes:
        unregister_class(cls)
        print("Unregistering " + cls)
    del bpy.types.Scene.my_props
    # del bpy.types.Context.my_props


if __name__ == "__main__":
    register()