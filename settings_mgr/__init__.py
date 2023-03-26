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
    "version": (0, 0, 2),
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

    from . import settings_mgr
    importlib.reload(settings_mgr)

    from . import save_button_operator
    importlib.reload(save_button_operator)
    print("reload_modules called!")

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
    
# Define our custom properties
class MyProperties(PropertyGroup):
    save_filename: StringProperty(
        name="Save As",
        description="The name of the settings file you want to save. Do not add a file extension",
        default="",
        maxlen=1024,
        )
        
    load_filename: StringProperty(
        name="Load File",
        description="The name of the settings file you want to load.",
        default="",
        maxlen=1024
        )

    # ================================
    # Load Preferences - Render - Main
    # ================================
    
    load_pref_workspace : BoolProperty(
        name = "Use Workspace settings",
        description = "Load the workspace properties",
        default = True
        )

    load_pref_render : BoolProperty(
        name = "Use Render settings",
        description = "Load the render properties",
        default = True
        )

    load_pref_output : BoolProperty(
        name = "Use Output settings",
        description = "Load the output properties",
        default = True
        )

    load_pref_view_layer : BoolProperty(
        name = "Use View Layer settings",
        description = "Load the view  layer properties",
        default = True
        )

    load_pref_scene : BoolProperty(
        name = "Use Scene settings",
        description = "Load the scene properties",
        default = True
        )

    load_pref_world : BoolProperty(
        name = "Use World settings",
        description = "Load the world properties",
        default = True
        )
    
    load_pref_collection : BoolProperty(
        name = "Use Collection settings",
        description = "Load the collection properties",
        default = True
        )

    load_pref_texture : BoolProperty(
        name = "Use Texture settings",
        description = "Load the texture properties",
        default = True
        )



_classes = [
    save_button_operator.SaveButtonOperator,
    load_button_operator.LoadButtonOperator,
    operator_file_import.ImportSomeData,
    MyProperties,
    settings_mgr.NPanel,
]

def register():
    for cls in _classes:
        register_class(cls)
    # Register our properties
    bpy.types.Scene.my_props = PointerProperty(type=MyProperties)


def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()