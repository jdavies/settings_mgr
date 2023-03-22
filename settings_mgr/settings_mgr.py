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
        row.prop(my_props, "load_filename")
        loadFileOp = row.operator(ImportSomeData.bl_idname, text="", icon='FILEBROWSER')
        loadFileOp.isSaveFile = False   # False = We are loading data
        row = box.row()
        box.label(text = "Render Properties")

        row = box.row()
        row.prop(my_props, "load_pref_render_bake")
        row.prop(my_props, "load_pref_render_colormanagement")

        row = box.row()
        row.prop(my_props, "load_pref_render_curves")
        row.prop(my_props, "load_pref_render_film")

        row = box.row()
        row.prop(my_props, "load_pref_render_freestyle")
        row.prop(my_props, "load_pref_render_greasepencil")

        row = box.row()
        row.prop(my_props, "load_pref_render_lightpaths")
        row.prop(my_props, "load_pref_render_motionblur")

        row = box.row()
        row.prop(my_props, "load_pref_render_performance")
        row.prop(my_props, "load_pref_render_sampling")

        row = box.row()
        row.prop(my_props, "load_pref_render_simplify")
        row.prop(my_props, "load_pref_render_volumes")


        # Output Props
        row = box.row()
        box.label(text = "Output Properties")
        row = box.row()
        row.prop(my_props, "load_pref_output_format")
        row.prop(my_props, "load_pref_output_frame_range")

        row = box.row()
        row.prop(my_props, "load_pref_output_metadata")
        row.prop(my_props, "load_pref_output_output")

        row = box.row()
        row.prop(my_props, "load_pref_output_postprocessing")
        row.prop(my_props, "load_pref_output_stereoscopy")

        row = box.row()
        row.operator(LoadButtonOperator.bl_idname, text="Load Settings", icon='LINENUMBERS_ON')

    # def execute(self, context):
    #     save_file = self.save_file_name
    #     print("save_file = " + save_file)

class SubPanel(BasePanel, bpy.types.Panel):
    """Creates an N-Panel in the Object properties window"""
    bl_options = {"DEFAULT_CLOSED"}
    # Panel Text
    bl_parent_id = "OBJECT_PT_settings" # Use the bl_idname of the parent!
    bl_label = "Subpanel"
    bl_idname = "OBJECT_PT_subpanel"

    def draw(self, context):
        # Do the layout
        layout = self.layout
        scene = context.scene
        # obj = context.object
        my_props = scene.my_props
        
        # Save file section
        box = layout.box()
        box.label(text = "SubPanel Settings")