import bpy
import json
import os
from .save_button_operator import (SaveButtonOperator)
from .load_button_operator import (LoadButtonOperator)
from .operator_file_import import (ImportSomeData)

class BasePanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Set Mgr" # Tab name
    bl_options = {"DEFAULT_CLOSED"}

class NPanel(BasePanel, bpy.types.Panel):
    """Creates an N-Panel in the Object properties window"""
    # bl_space_type = 'VIEW_3D'
    # bl_region_type = 'UI'
    # bl_category = "SetMgr" # Tab name
    # bl_options = {"DEFAULT_OPEN"}
    # Panel Text
    bl_label = "Settings Manager"
    bl_idname = "OBJECT_PT_settings"

    saveFilePath = ''

    def draw(self, context):
        # Do the layout
        layout = self.layout
        scene = context.scene
        # obj = context.object
        my_props = scene.my_props
        
        # Save file section
        box = layout.box()
        box.label(text = "Save Settings")
        #layout.prop(my_props, "save_filename")
        row = box.row()
        row.prop(my_props, "save_filename")
        saveFileOp = row.operator(ImportSomeData.bl_idname, text="", icon='FILEBROWSER')
        saveFileOp.isSaveFile = True
        box.operator(SaveButtonOperator.bl_idname, text="Save Settings", icon='GREASEPENCIL')

        # Load File
        box = layout.box()
        box.label(text = "Load Settings")

        row = box.row()
        row.prop(my_props, "load_pref_workspace")
        row.prop(my_props, "load_pref_render")
        row = box.row()
        row.prop(my_props, "load_pref_output")
        row.prop(my_props, "load_pref_view_layer")
        row = box.row()
        row.prop(my_props, "load_pref_scene")
        row.prop(my_props, "load_pref_world")
        row = box.row()
        row.prop(my_props, "load_pref_collection")
        row.prop(my_props, "load_pref_texture")

        row = box.row()
        row.prop(my_props, "load_dummy")
        
        row = box.row()
        row.prop(my_props, "load_filename")
        loadFileOp = row.operator(ImportSomeData.bl_idname, text="", icon='FILEBROWSER')
        loadFileOp.isSaveFile = False   # False = We are loading data
        
        row = box.row()
        row.operator(LoadButtonOperator.bl_idname, text="Load Settings", icon='LINENUMBERS_ON')

    # def execute(self, context):
    #     save_file = self.save_file_name
    #     print("save_file = " + save_file)

# class RenderPropsSubPanel(BasePanel, bpy.types.Panel):
#     """Creates a child N-Panel in the Object properties window"""
#     bl_options = {"DEFAULT_CLOSED"}
#     # Panel Text
#     bl_parent_id = "OBJECT_PT_settings" # Use the bl_idname of the parent!
#     bl_label = "Render Properties"
#     bl_idname = "OBJECT_PT_renderprops"

#     def draw(self, context):
#         # Do the layout
#         layout = self.layout
#         scene = context.scene
#         # obj = context.object
#         my_props = scene.my_props
        
#         # Render Props section
#         box = layout.box()

#         row = box.row()
#         row.prop(my_props, "load_pref_render")
#         row.prop(my_props, "load_pref_output")
#         row.prop(my_props, "load_pref_view_layer")
#         row.prop(my_props, "load_pref_scene")
#         row.prop(my_props, "load_pref_world")
#         row.prop(my_props, "load_pref_collection")
#         row.prop(my_props, "load_pref_texture")
