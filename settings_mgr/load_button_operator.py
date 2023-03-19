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
        print('File Loaded and applied')

    def applyData(self):
        # Metadata
        context.scene.render.engine = self.data['render_props']['engine']
        if(self.data['render_props']['engine'] == 'CYCLES'):
            # Load the Cycles settings
            loadCycles()
        else:
            # Load the EEVEE settings
            loadEevee()
        if(self.data['output_props']['metadata']['use_stamp_note']):
            bpy.context.scene.render.use_stamp_note = True
            bpy.context.scene.render.stamp_note_text = self.data['output_props']['metadata']['stamp_note_text']
            x = self.data['output_props']['metadata']['stamp_note_text']
        print('applyData() x = ' + x)

    def loadCycles(self):
        context.scene.render.device = self.data['render_props']['device']
        context.scene.render.feature_set = self.data['render_props']['feature_set']
        # Film
        bpy.context.scene.cycles.film_exposure = self.data['render_props']['film']['film_exposure']
        bpy.context.scene.cycles.pixel_filter_type = self.data['render_props']['film']['pixel_filter']['pixel_filter_type']
        if(bpy.context.scene.cycles.pixel_filter_type != 'BOX'):
            # does not apply to the Box type
            bpy.context.scene.cycles.filter_width = self.data['render_props']['film']['pixel_filter']['filter_width']
            bpy.context.scene.render.film_transparent = self.data['render_props']['film']['transparent']['film_transparent']
            bpy.context.scene.cycles.film_transparent_glass = self.data['render_props']['film']['transparent']['film_transparent_glass']
            bpy.context.scene.cycles.film_transparent_roughness = self.data['render_props']['film']['transparent']['film_transparent_roughness']

    def loadEevee(self):
        self.data['render_props']['engine']
