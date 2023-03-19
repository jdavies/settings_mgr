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
from bpy.props import (StringProperty, PointerProperty)
from bpy.types import (Panel, Operator, PropertyGroup)
from . import settings_mgr
from . import save_button_operator
from . import load_button_operator
from . import updater

print('Loading Settings Manager...')
print(bl_info)
print("update avail: " + isUpdateAvailable("0.0.2"))
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

    message = StringProperty(
        name = "message",
        description = "message",
        default = ''
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
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)


def unregister():
    for cls in _classes:
        unregister_class(cls)


if __name__ == "__main__":
    register()

    
#class AnimLayersSceneSettings(bpy.types.PropertyGroup):
#    blend_type : bpy.props.EnumProperty(name = 'Default Blend Type', description="Default Blend Type when adding layers",  default = 'COMBINE',
#        items = [('COMBINE', 'Combine', 'Use Combine as the default blend type'), ('ADD', 'Add', 'Use Add as the default blend type'), ('REPLACE', 'Replace', 'Use Replace as the default blend type'), 
#            ('SUBTRACT', 'Subtract', 'Use as an Subtract Layer')], update = anim_layers.blend_type_update , override = {'LIBRARY_OVERRIDABLE'})
#        
#class AnimLayersSettings(bpy.types.PropertyGroup):
#    turn_on: bpy.props.BoolProperty(name="Turn Animation Layers On", description="Turn on and start Animation Layers", default=False, options={'HIDDEN'}, update = anim_layers.turn_animlayers_on, override = {'LIBRARY_OVERRIDABLE'})
#    layer_index: bpy.props.IntProperty(update = anim_layers.update_layer_index, options={'LIBRARY_EDITABLE'}, default = 0, override = {'LIBRARY_OVERRIDABLE'})
#    linked: bpy.props.BoolProperty(name="Linked", description="Duplicate a layer with a linked action", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'})
#    smartbake: bpy.props.BoolProperty(name="Smart Bake", description="Stay with the same amount of keyframes after merging and baking", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'})
#    onlyselected: bpy.props.BoolProperty(name="Only selected Bones", description="Bake only selected Armature controls", default=True, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'})
#    clearconstraints: bpy.props.BoolProperty(name="Clear constraints", description="Clear constraints during bake", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'})
#    mergefcurves: bpy.props.BoolProperty(name="Merge Cyclic & Fcurve modifiers", description="Include Fcurve modifiers in the bake", default = True, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'})
#    view_all_keyframes: bpy.props.BoolProperty(name="View", description="View keyframes from multiple layers, use lock and mute to exclude layers", default=False, update = anim_layers.view_all_keyframes, override = {'LIBRARY_OVERRIDABLE'})
#    edit_all_keyframes: bpy.props.BoolProperty(name="Edit", description="Edit keyframes from multiple layers", default=False, update = anim_layers.unlock_edit_keyframes, override = {'LIBRARY_OVERRIDABLE'})
#    only_selected_bones: bpy.props.BoolProperty(name="Only Selected Bones", description="Edit and view only selected bones", default=False, update = anim_layers.only_selected_bones, override = {'LIBRARY_OVERRIDABLE'})
#    view_all_type: bpy.props.EnumProperty(name="Type", description="Select visibiltiy type of keyframes", update = anim_layers.view_all_keyframes, override = {'LIBRARY_OVERRIDABLE'},
#        items = [
#            ('BREAKDOWN', 'Breakdown', 'select Breakdown visibility'),
#            ('JITTER', 'Jitter', 'select Jitter visibility'),
#            ('MOVING_HOLD', 'Moving Hold', 'select Moving Hold visibility'),
#            ('EXTREME', 'Extreme', 'select Extreme visibility'),
#            ('KEYFRAME', 'Keyframe', 'select Keyframe visibility')
#        ]
#    )
#    baketype : bpy.props.EnumProperty(name = '', description="Type of Bake", items = [('AL', 'Anim Layers','Use Animation Layers Bake',0), ('NLA', 'NLA Bake', 'Use Blender internal NLA Bake',1)], override = {'LIBRARY_OVERRIDABLE'})
#    direction: bpy.props.EnumProperty(name = '', description="Select direction of merge", items = [('UP', 'Up','Merge upwards','TRIA_UP',1), ('DOWN', 'Down', 'Merge downwards','TRIA_DOWN',0), ('ALL', 'All', 'Merge all layers')], override = {'LIBRARY_OVERRIDABLE'})
#    operator : bpy.props.EnumProperty(name = '', description="Type of bake", items = [('NEW', 'New Baked Layer','Bake into a New Layer','NLA',1), ('MERGE', 'Merge', 'Merge Layers','NLA_PUSHDOWN',0)], override = {'LIBRARY_OVERRIDABLE'})
#    blend_type :  bpy.props.EnumProperty(name = 'Blend Type', description="Blend Type", 
#        items = [('REPLACE', 'Replace', 'Use as a Base Layer'), ('ADD', 'Add', 'Use as an Additive Layer'), ('SUBTRACT', 'Subtract', 'Use as an Subtract Layer')], update = anim_layers.blend_type_update , override = {'LIBRARY_OVERRIDABLE'})
#    data_type :  bpy.props.EnumProperty(name = 'Data Type', description="Select type of action data", default = 'OBJECT', update = anim_layers.data_type_update,
#        items = [('KEY', 'Shapekey', 'Switch to shapekey animation layers'), ('OBJECT', 'Object', 'Switch to object animation')], override = {'LIBRARY_OVERRIDABLE'})#, update = anim_layers.blend_type_update
#    auto_rename: bpy.props.BoolProperty(name="Auto Rename Layer", description="Rename layer to match to selected action", default=False, update = anim_layers.auto_rename, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'})
#    auto_blend: bpy.props.BoolProperty(name="Auto Blend", description="Apply blend type automatically based on scale and rotation values", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'})
#    fcurves: bpy.props.IntProperty(name='fcurves', description='helper to check if fcurves are changed', default=0, override = {'LIBRARY_OVERRIDABLE'})
#    upper_stack : bpy.props.BoolProperty(name="Upper Stack Evaluation", description="Checks if tweak mode uses upper stack", default=False, override = {'LIBRARY_OVERRIDABLE'})
#    inbetweener : bpy.props.FloatProperty(name='Inbetween Keyframe', description="Adds an inbetween Keyframe between the Layer's neighbor keyframes", soft_min = 0, soft_max = 1, default=0.5, options = set(), override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.add_inbetween_key)
#    
#class AnimLayersItems(bpy.types.PropertyGroup):
#    name: bpy.props.StringProperty(name="AnimLayer", override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_name_update)
#    mute: bpy.props.BoolProperty(name="Mute", description="Mute Animation Layer", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_mute)
#    lock: bpy.props.BoolProperty(name="Lock", description="Lock Animation Layer", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_lock)
#    solo: bpy.props.BoolProperty(name="Solo", description="Solo Animation Layer", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_solo)
#    influence: bpy.props.FloatProperty(name="Layer Influence", description="Layer Influence", min = 0.0, options={'ANIMATABLE'}, max = 1.0, default = 1.0, precision = 3, update = anim_layers.influence_update, override = {'LIBRARY_OVERRIDABLE'})
#    influence_mute: bpy.props.BoolProperty(name="Animated Influence", description="Turn Animated influence On/Off", default=False, options={'HIDDEN'}, update = anim_layers.influence_mute_update, override = {'LIBRARY_OVERRIDABLE'})
#    #action_list: bpy.props.EnumProperty(name = 'Actions', description = "Select action", update = anim_layers.load_action, items =  anim_layers.action_items, override = {'LIBRARY_OVERRIDABLE'})
#    action: bpy.props.PointerProperty(name = 'action', description = "Select action", type=bpy.types.Action, update = anim_layers.load_action, override = {'LIBRARY_OVERRIDABLE'})
#    action_range: bpy.props.FloatVectorProperty(name='action range', description="used to check if layer needs to update frame range", override = {'LIBRARY_OVERRIDABLE'}, size = 2)
#    frame_range: bpy.props.BoolProperty(name="Custom Frame Range", description="Use a custom frame range per layer instead of the scene frame range", default=False, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_frame_range)
#    action_start: bpy.props.FloatProperty(name='Action Start Frame', description="First frame of the layer's action",min = 0, default=0, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_action_start)
#    action_end: bpy.props.FloatProperty(name='Action End Frame', description="End frame of the layer's action", default=0, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_action_end)
#    speed: bpy.props.FloatProperty(name='Speed of the action', description="Speed of the action strip", default = 1, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_speed)
#    offset: bpy.props.FloatProperty(name='Offset when the action starts', description="Offseting the whole layer animation", default = 0, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_offset)
#    repeat: bpy.props.FloatProperty(name="Repeat", description="Repeat the action", min = 0.1, default = 1, options={'HIDDEN'}, override = {'LIBRARY_OVERRIDABLE'}, update = anim_layers.layer_repeat)


#class AnimLayersObjects(bpy.types.PropertyGroup):

#    object: bpy.props.PointerProperty(name = "object", description = "objects with animation layers turned on", type=bpy.types.Object, override = {'LIBRARY_OVERRIDABLE'})


## Add-ons Preferences Update Panel
## Define Panel classes for updating
#panels = (anim_layers.ANIMLAYERS_PT_List, anim_layers.ANIMLAYERS_PT_Ops, anim_layers.ANIMLAYERS_PT_Tools, anim_layers.ANIMLAYERS_PT_Multikey, anim_layers.ANIMLAYERS_PT_Settings) #anim_layers.ANIMLAYERS_PT_Panel,

#def update_panel(self, context):
#    message = "AnimationLayers: Updating Panel locations has failed"
#    try:
#        for panel in panels:
#            if "bl_rna" in panel.__dict__:
#                bpy.utils.unregister_class(panel)

#        for panel in panels:
#            #print (panel.bl_category)
#            panel.bl_category = context.preferences.addons[__name__].preferences.category
#            bpy.utils.register_class(panel)

#    except Exception as e:
#        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
#        pass
#    
#@addon_updater_ops.make_annotations
#class AnimLayersAddonPreferences(bpy.types.AddonPreferences):
#    # this must match the addon name, use '__package__'
#    # when defining this in a submodule of a python package.
#    bl_idname = __package__

#    category: bpy.props.StringProperty(
#        name="Tab Category",
#        description="Choose a name for the category of the panel",
#        default="Animation",
#        update=update_panel
#    )
#    
#    # addon updater preferences from `__init__`, be sure to copy all of them
#    auto_check_update: bpy.props.BoolProperty(
#        name = "Auto-check for Update",
#        description = "If enabled, auto-check for updates using an interval",
#        default = False,
#    )

#    updater_interval_months: bpy.props.IntProperty(
#        name='Months',
#        description = "Number of months between checking for updates",
#        default=0,
#        min=0
#    )
#    updater_interval_days: bpy.props.IntProperty(
#        name='Days',
#        description = "Number of days between checking for updates",
#        default=7,
#        min=0,
#    
#    )
#    updater_interval_hours: bpy.props.IntProperty(
#        name='Hours',
#        description = "Number of hours between checking for updates",
#        default=0,
#        min=0,
#        max=23
#    )
#    updater_interval_minutes: bpy.props.IntProperty(
#        name='Minutes',
#        description = "Number of minutes between checking for updates",
#        default=0,
#        min=0,
#        max=59
#    )

#    def draw(self, context):
#        layout = self.layout
#        addon_updater_ops.update_settings_ui(self, context)
#        
#        row = layout.row()
#        col = row.column()

#        col.label(text="Tab Category:")
#        col.prop(self, "category", text="")

#classes = (AnimLayersSettings, AnimLayersSceneSettings, AnimLayersItems, AnimLayersObjects)
#    
#addon_keymaps = []
#    
#def register():
#    from bpy.utils import register_class
#    addon_updater_ops.register(bl_info)
#    register_class(AnimLayersAddonPreferences)
#    addon_updater_ops.make_annotations(AnimLayersAddonPreferences) # to avoid blender 2.8 warnings
#    if bpy.app.version < (3, 2, 0):
#        return
#    for cls in classes:
#        register_class(cls)
#    bake_ops.register()
#    anim_layers.register()
#    multikey.register()
#    bpy.types.Object.als = bpy.props.PointerProperty(type = AnimLayersSettings, options={'LIBRARY_EDITABLE'}, override = {'LIBRARY_OVERRIDABLE'})
#    bpy.types.Scene.als = bpy.props.PointerProperty(type = AnimLayersSceneSettings, options={'LIBRARY_EDITABLE'}, override = {'LIBRARY_OVERRIDABLE'})
#    bpy.types.Object.Anim_Layers = bpy.props.CollectionProperty(type = AnimLayersItems, override = {'LIBRARY_OVERRIDABLE', 'USE_INSERTION'})
#    bpy.types.Scene.AL_objects = bpy.props.CollectionProperty(type = AnimLayersObjects, options={'LIBRARY_EDITABLE'}, override = {'LIBRARY_OVERRIDABLE', 'USE_INSERTION'})
#    update_panel(None, bpy.context)
#    #update_tweak_keymap()
#    
#    #Make sure TAB hotkey in the NLA goes into full stack mode
#    wm = bpy.context.window_manager
#    kc = wm.keyconfigs.addon
#    km = kc.keymaps.new(name= 'NLA Generic', space_type= 'NLA_EDITOR')
#    if 'nla.tweakmode_enter' not in km.keymap_items:
#        kmi = km.keymap_items.new('nla.tweakmode_enter', type= 'TAB', value= 'PRESS')
#        kmi.properties.use_upper_stack_evaluation = True
#        addon_keymaps.append((km, kmi))
#        
#    
#def unregister():
#    addon_updater_ops.unregister()
#    from bpy.utils import unregister_class
#    unregister_class(AnimLayersAddonPreferences)
#    if bpy.app.version < (3, 2, 0):
#        return
#    
#    for cls in classes:
#        unregister_class(cls)
#    bake_ops.unregister()
#    anim_layers.unregister()
#    multikey.unregister()
#    del bpy.types.Object.als
#    del bpy.types.Object.Anim_Layers
#    del bpy.types.Scene.AL_objects
#    #removing keymaps
#    for km, kmi in addon_keymaps:
#        km.keymap_items.remove(kmi)
#    addon_keymaps.clear()

#if __name__ == "__main__":
#    register()




#=================================================
#=================================================
#=================================================
