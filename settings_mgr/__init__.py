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

# I found this routine in DECALMchin3. Great hack for
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
from bpy.props import (StringProperty, PointerProperty, BoolProperty)
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

    load_pref_render_bake : BoolProperty(
        name = "Bake",
        description = "Load the Bake portion of the Render Properties",
        default = True
        )

    load_pref_render_colormanagement : BoolProperty(
        name = "Color Management",
        description = "Load the Color Management portion of the Render Properties",
        default = True
        )

    load_pref_render_curves : BoolProperty(
        name = "Curves",
        description = "Load the Curves portion of the Render Properties",
        default = True
        )

    load_pref_render_film : BoolProperty(
        name = "Film",
        description = "Load the Film portion of the Render Properties",
        default = True
        )

    load_pref_render_freestyle : BoolProperty(
        name = "Freestyle",
        description = "Load the Freestyle portion of the Render Properties",
        default = True
        )

    load_pref_render_greasepencil : BoolProperty(
        name = "Grease Pencil",
        description = "Load the Grease Pencil portion of the Render Properties",
        default = True
        )

    load_pref_render_lightpaths : BoolProperty(
        name = "Light Paths",
        description = "Load the Light Paths portion of the Render Properties",
        default = True
        )

    load_pref_render_motionblur : BoolProperty(
        name = "Motion Blur",
        description = "Load the Motion Blue portion of the Render Properties",
        default = True
        )

    load_pref_render_performance : BoolProperty(
        name = "Performance",
        description = "Load the Performance portion of the Render Properties",
        default = True
        )

    load_pref_render_sampling : BoolProperty(
        name = "Sampling",
        description = "Load the Sampling portion of the Render Properties",
        default = True
        )

    load_pref_render_simplify : BoolProperty(
        name = "Simplify",
        description = "Load the Simplify portion of the Render Properties",
        default = True
        )

    load_pref_render_volumes : BoolProperty(
        name = "Volumes",
        description = "Load the Volumes portion of the Render Properties",
        default = True
        )

    # Output Properties
    load_pref_output_format : BoolProperty(
        name = "Format",
        description = "Load the Format portion of the Output Properties",
        default = True
        )

    load_pref_output_frame_range : BoolProperty(
        name = "Frame Range",
        description = "Load the Frame Range portion of the Output Properties",
        default = True
        )

    load_pref_output_metadata : BoolProperty(
        name = "Metadata",
        description = "Load the Metadata portion of the Output Properties",
        default = True
        )

    load_pref_output_output : BoolProperty(
        name = "Output",
        description = "Load the Output portion of the Output Properties",
        default = True
        )

    load_pref_output_postprocessing : BoolProperty(
        name = "Post Processing",
        description = "Load the Post Processing portion of the Output Properties",
        default = True
        )

    load_pref_output_stereoscopy : BoolProperty(
        name = "Stereoscopy",
        description = "Load the Stereoscopy portion of the Output Properties",
        default = True
        )

_classes = [
    save_button_operator.SaveButtonOperator,
    load_button_operator.LoadButtonOperator,
    operator_file_import.ImportSomeData,
    MyProperties,
    settings_mgr.NPanel
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