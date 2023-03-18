import bpy
import json
import os
from .save_button_operator import (SaveButtonOperator)
from .load_button_operator import (LoadButtonOperator)

class NPanel(bpy.types.Panel):
    """Creates an N-Panel in the Object properties window"""
    # Panel Text
    bl_label = "Settings Manager"
    bl_idname = "OBJECT_PT_random"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # Tab name
    bl_category = "SetMgr"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # obj = context.object
        mytool = scene.my_tool
        
        row = layout.row()
        #layout.prop(mytool, "save_filename")
        row.prop(mytool, "save_filename")

        row = layout.row()
        row.operator(SaveButtonOperator.bl_idname, text="Save Settings", icon='GREASEPENCIL')
        
        # Load File
        layout.prop(mytool, "load_filename")
        row = layout.row()
        row.operator(LoadButtonOperator.bl_idname, text="Load:", icon='LINENUMBERS_ON')

    def execute(self, context):
        save_file = self.save_file_name