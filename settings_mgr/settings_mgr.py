import bpy
import json
import os

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
        obj = context.object
        mytool = scene.my_tool
        
        row = layout.row()
        row.label(text="Save File:")

#        row = layout.row()
        layout.prop(mytool, "filename")
        
        row = layout.row()
        row.operator(SaveButtonOperator.bl_idname, text="Save Settings", icon='GREASEPENCIL')
        
        # Load File
        row = layout.row()
        row.label(text="Load File:")
        
        layout.prop(mytool, "load_filename")
        row = layout.row()
        row.operator(LoadButtonOperator.bl_idname, text="Load:", icon='LINENUMBERS_ON')
    
# I discovered this class at https://b3d.interplanety.org/en/creating-pop-up-panels-with-user-ui-in-blender-add-on/
# class MessageBox(bpy.types.Operator):
#     bl_idname = "message.messagebox"
#     bl_label = ""
 
#     def execute(self, context):
#         # self.report({'INFO'}, self.message)
#         self.report({'INFO'}, context.scene.my_tool.message)
#         # print(self.message)
#         print(context.scene.my_tool.message)
#         return {'FINISHED'}
 
#     def invoke(self, context, event):
#         return context.window_manager.invoke_props_dialog(self, width = 400)

#     def draw(self, context):
#         # self.layout.label(self.message)
#         mymsg = context.scene.my_tool.message
#         self.layout.label(mymsg)
#         # context.scene.my_tool.message
#         self.layout.label("")
