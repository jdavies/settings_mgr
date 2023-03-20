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
        filename = context.scene.my_props.load_filename
        self.readJSONFile(context, filename)
        self.applyData(context)
        return {'FINISHED'}
    
    # Reads the JSON file into the class-level data object
    def readJSONFile(self, context, filename):
        filename = bpy.path.ensure_ext(filename, '.json', case_sensitive=False)
        print('loading the file: ' + filename + '...')
        # DO LOAD HERE
        filename = curDir = bpy.path.abspath(filename) ## In case it starts wth //
        print('loading the file: ' + filename + '...')
        f = open(filename, 'r')
        self.data = json.load(f)
        f.close()
        print('JSON Read')
        print(self.data)
        print('File Loaded and applied')

    # Now that the data is loaded into our class variable. We can apply
    # the selected portions to the current file
    def applyData(self, context):
        scene = context.scene
        my_props = scene.my_props

        if(my_props.load_pref_output_metadata == True):
            # Metadata
            if(self.data['render_props']['engine'] == 'CYCLES'):
                # Load the Cycles self.data
                self.loadCycles(context)
            else:
                # Load the EEVEE self.data
                self.loadEevee(context)
            if(self.data['output_props']['metadata']['use_stamp_note']):
                bpy.context.scene.render.use_stamp_note = True
                bpy.context.scene.render.stamp_note_text = self.data['output_props']['metadata']['stamp_note_text']
                x = self.data['output_props']['metadata']['stamp_note_text']
        print('applyData() complete!')

    def loadCycles(self, context):
        scene = context.scene
        my_props = scene.my_props

        # =================
        # Render Properties
        # =================
        # Always load the core Render Properties
        context.scene.render.engine = self.data['render_props']['engine']
        context.scene.cycles.device = self.data['render_props']['device']
        context.scene.cycles.feature_set = self.data['render_props']['feature_set']
        # Bake
        bpy.context.scene.render.use_bake_multires = self.data['render_props']['bake']['use_bake_multires']
        bpy.context.scene.render.bake_type = self.data['render_props']['bake']['bake_type']
        bpy.context.scene.render.use_bake_clear = self.data['render_props']['bake']['output']['use_bake_clear']
        bpy.context.scene.render.use_bake_lores_mesh = self.data['render_props']['bake']['output']['use_bake_lores_mesh']
        bpy.context.scene.render.bake_margin_type = self.data['render_props']['bake']['margin']['bake_margin_type']
        bpy.context.scene.render.bake_margin = self.data['render_props']['bake']['margin']['bake_margin']
        # Color Management
        bpy.context.scene.display_settings.display_device = self.data['render_props']['color_management']['display_device']
        bpy.context.scene.view_settings.view_transform = self.data['render_props']['color_management']['view_transform']
        bpy.context.scene.view_settings.look = self.data['render_props']['color_management']['look']
        bpy.context.scene.view_settings.exposure = self.data['render_props']['color_management']['exposure']
        bpy.context.scene.view_settings.gamma = self.data['render_props']['color_management']['gamma']
        bpy.context.scene.sequencer_colorspace_settings.name = self.data['render_props']['color_management']['name']
        bpy.context.scene.view_settings.use_curve_mapping = self.data['render_props']['color_management']['curves']['use_curve_mapping']
        # Curves
        bpy.context.scene.cycles_curves.shape = self.data['render_props']['curves']['shape']
        bpy.context.scene.cycles_curves.subdivision = self.data['render_props']['curves']['subdivisions']
        bpy.context.scene.render.hair_type = self.data['render_props']['curves']['viewport_display']['hair_type']
        bpy.context.scene.render.hair_subdiv = self.data['render_props']['curves']['viewport_display']['hair_subdiv']
        # Film
        bpy.context.scene.cycles.film_exposure = self.data['render_props']['film']['film_exposure']
        bpy.context.scene.cycles.pixel_filter_type = self.data['render_props']['film']['pixel_filter']['pixel_filter_type']
        if(bpy.context.scene.cycles.pixel_filter_type != 'BOX'):
            # does not apply to the Box type
            bpy.context.scene.cycles.filter_width = self.data['render_props']['film']['pixel_filter']['filter_width']
            bpy.context.scene.render.film_transparent = self.data['render_props']['film']['transparent']['film_transparent']
            bpy.context.scene.cycles.film_transparent_glass = self.data['render_props']['film']['transparent']['film_transparent_glass']
            bpy.context.scene.cycles.film_transparent_roughness = self.data['render_props']['film']['transparent']['film_transparent_roughness']
        # Render Properties - Freestyle
        bpy.context.scene.render.use_freestyle = self.data['render_props']['freestyle']['use_freestyle']
        bpy.context.scene.render.line_thickness_mode = self.data['render_props']['freestyle']['line_thickness_mode']
        bpy.context.scene.render.line_thickness = self.data['render_props']['freestyle']['line_thickness']
        # Render Properties - Grease Pencil
        # Render Properties - Light Paths
        # Render Properties - Motion Blue
        # Render Properties - Performance
        # Render Properties - Sampling
        # Render Properties - Simplify
        # Render Properties - Volumes

    def loadEevee(self):
        self.data['render_props']['engine']
