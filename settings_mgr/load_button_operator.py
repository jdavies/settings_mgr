import bpy
import json
import os

# Get the operator for the button
class LoadButtonOperator(bpy.types.Operator):
    """Load the JSON file"""
    bl_idname = "setmgr.load"
    bl_label = "Settings Manager"

    data = {}

    def execute(self, context):
        filename = context.scene.my_tool.load_filename
        self.readJSONFile(context, filename)
        self.applyData()
        return {'FINISHED'}
    
    def readJSONFile(self, context, filename):
        filename = bpy.path.ensure_ext(filename, '.json', case_sensitive=False)
        print('loading the file: ' + filename + '...')
        # DO LOAD HERE
        f = open(filename, 'r')
        self.data = json.load(f)
        f.close()
        print('JSON Read')
        print(self.data)

        x = self.data['output_props']['metadata']['stamp_note_text']
        print('x = ' + x)
        print('File Loaded and applied')

    def applyData(self):
        # Metadata
        if(self.data['output_props']['metadata']['use_stamp_note']):
            bpy.context.scene.render.use_stamp_note = True
            bpy.context.scene.render.stamp_note_text = self.data['output_props']['metadata']['stamp_note_text']
            x = self.data['output_props']['metadata']['stamp_note_text']
        print('applyData() x = ' + x)