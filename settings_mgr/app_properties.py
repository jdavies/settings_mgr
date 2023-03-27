import bpy
import sys
from bpy.types import (PropertyGroup)
from bpy.props import (StringProperty, PointerProperty, BoolProperty, FloatProperty, IntProperty)

# Define our custom properties
class AppProperties(PropertyGroup):
    save_filename: StringProperty(name="Save As", description="The name of the settings file you want to save. Do not add a file extension", default="", maxlen=128)
    load_filename: StringProperty(name="Load File", description="The name of the settings file you want to load.", default="", maxlen=128)
    load_dummy: StringProperty(name="Dummy Prop", description="The name of the settings file you want to load.", default="foobar", maxlen=128)
    load_pref_workspace: BoolProperty(name = "Use Workspace settings", description = "Load the workspace properties", default = True)
    load_pref_render: BoolProperty(name="Use Render settings", description = "Load the render properties", default = True)
    load_pref_output: BoolProperty(name="Use Output settings", description = "Load the output properties", default = True)

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