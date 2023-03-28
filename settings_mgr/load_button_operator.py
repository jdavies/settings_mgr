import bpy
import json
import os
from array import *

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
        self.report({'INFO'}, 'loading the file: ' + filename + '...')

        # DO LOAD HERE
        filename = curDir = bpy.path.abspath(filename) ## In case it starts wth //
        # print('loading the file: ' + filename + '...')
        f = open(filename, 'r')
        self.data = json.load(f)
        f.close()
        # print('JSON Read')
        # print(self.data)
        self.report({'INFO'}, 'File Loaded and applied')

    # Now that the data is loaded into our class variable. We can apply
    # the selected portions to the current file
    def applyData(self, context):
        scene = context.scene
        my_props = scene.my_props
        # print("my_props A:")
        # print(my_props.keys())
        # print("LISTING THE KEYS...")
        # print(list(my_props.keys()))
        # print("Load file = " + my_props["load_filename"])
        # print("Load file X = " + my_props.load_filename)
        # print("Load dummy = " + my_props.load_dummy)
        # print("Use Workspace = " + str(my_props.load_pref_workspace))

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
        # print("my_props:")
        # print(list(my_props.keys()))
        if(my_props.load_pref_render == True):
            self.loadCyclesRenderProps(my_props)

        # ====================
        # Workspace Properties
        # ====================
        # if load_pref_render["load_pref_workspace"]:
        if(my_props.load_pref_workspace == True):
            self.loadCyclesWorkspaceProps(my_props)
            
        # ==================
        # Output Properties
        # ==================
        if(my_props.load_pref_output == True):
            self.loadCyclesOutputProps(my_props)

        # =====================
        # View Layer Properties
        # =====================
        if(my_props.load_pref_view_layer == True):
            self.loadCyclesViewLayerProps(my_props)

        # =====================
        # Scene Properties
        # =====================
        if(my_props.load_pref_scene == True):
            self.loadCyclesSceneProps(my_props)

        # =====================
        # World Properties
        # =====================
        if(my_props.load_pref_world == True):
            self.loadCyclesWorldProps(my_props)

        # =====================
        # Collection Properties
        # =====================
        if(my_props.load_pref_collection == True):
            self.loadCyclesCollectionProps(my_props)

        # =====================
        # Texture Properties
        # =====================
        if(my_props.load_pref_texture == True):
            self.loadCyclesTextureProps(my_props)

    def loadCyclesWorkspaceProps(self, props):
        print("Loading Cycles Workspace properties...")
        bpy.context.scene.tool_settings.use_transform_data_origin = self.data['workspace']['options']['transform']['use_transform_data_origin']
        bpy.context.scene.tool_settings.use_transform_pivot_point_align = self.data['workspace']['options']['transform']['use_transform_pivot_point_align']
        bpy.context.scene.tool_settings.use_transform_skip_children = self.data['workspace']['options']['transform']['use_transform_skip_children']
        bpy.data.workspaces["Scripting"].use_pin_scene = self.data['workspace']['workspace']['use_pin_scene']
        bpy.data.workspaces["Scripting"].object_mode = self.data['workspace']['workspace']['object_mode']
        bpy.data.workspaces["Scripting"].use_filter_by_owner = self.data['workspace']['workspace']['filter_addons']['use_filter_by_owner']

    def loadCyclesRenderProps(self, props):
        print("Loading Cycles Render properties...")
        # Bake
        bpy.context.scene.render.use_bake_multires = self.data['render_props']['bake']['use_bake_multires']
        if(bpy.context.scene.render.use_bake_multires == True):
            bpy.context.scene.render.bake_type = self.data['render_props']['bake']['bake_type']

        bpy.context.scene.render.use_bake_clear = self.data['render_props']['bake']['output']['use_bake_clear']
        bpy.context.scene.render.use_bake_lores_mesh = self.data['render_props']['bake']['output']['use_bake_lores_mesh']
        bpy.context.scene.render.bake_margin_type = self.data['render_props']['bake']['margin']['bake_margin_type']
        bpy.context.scene.render.bake_margin = self.data['render_props']['bake']['margin']['bake_margin_size']

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
        if(bpy.context.scene.cycles.pixel_filter_type =='BLACKMAN-HARRIS' or bpy.context.scene.cycles.pixel_filter_type == 'GAUSSIAN'):
            bpy.context.scene.cycles.filter_width = self.data['render_props']['film']['pixel_filter']['filter_width']
        else:
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
        bpy.context.scene.grease_pencil_settings.antialias_threshold = self.data['render_props']['grease_pencil']['antialias_threshold']

        # Render Properties - Light Paths
        bpy.context.scene.cycles.max_bounces = self.data['render_props']['light_paths']['max_bounces']['total']
        bpy.context.scene.cycles.diffuse_bounces = self.data['render_props']['light_paths']['max_bounces']['diffuse_bounces']
        bpy.context.scene.cycles.glossy_bounces = self.data['render_props']['light_paths']['max_bounces']['glossy_bounces']
        bpy.context.scene.cycles.transmission_bounces = self.data['render_props']['light_paths']['max_bounces']['transmission_bounces']
        bpy.context.scene.cycles.volume_bounces = self.data['render_props']['light_paths']['max_bounces']['volume_bounces']
        bpy.context.scene.cycles.transparent_max_bounces = self.data['render_props']['light_paths']['max_bounces']['transparent_max_bounces']
        bpy.context.scene.cycles.sample_clamp_direct = self.data['render_props']['light_paths']['clamping']['sample_clamp_direct']
        bpy.context.scene.cycles.sample_clamp_indirect = self.data['render_props']['light_paths']['clamping']['sample_clamp_indirect']
        bpy.context.scene.cycles.blur_glossy = self.data['render_props']['light_paths']['caustics']['blur_glossy']
        bpy.context.scene.cycles.caustics_reflective = self.data['render_props']['light_paths']['caustics']['caustics_reflective']
        bpy.context.scene.cycles.caustics_refractive = self.data['render_props']['light_paths']['caustics']['caustics_refractive']
        bpy.context.scene.cycles.use_fast_gi = self.data['render_props']['light_paths']['fast_gi']['use_fast_gi']
        bpy.context.scene.cycles.fast_gi_method = self.data['render_props']['light_paths']['fast_gi']['fast_gi_method']
        bpy.context.scene.world.light_settings.ao_factor = self.data['render_props']['light_paths']['fast_gi']['ao_factor']
        bpy.context.scene.world.light_settings.distance = self.data['render_props']['light_paths']['fast_gi']['distance']

        # Render Properties - Motion Blur
        bpy.context.scene.render.use_motion_blur = self.data['render_props']['motion_blur']['use_motion_blur']
        bpy.context.scene.cycles.motion_blur_position = self.data['render_props']['motion_blur']['motion_blur_position']
        bpy.context.scene.render.motion_blur_shutter = self.data['render_props']['motion_blur']['motion_blur_shutter']
        bpy.context.scene.cycles.rolling_shutter_type = self.data['render_props']['motion_blur']['rolling_shutter_type']
        bpy.context.scene.cycles.rolling_shutter_duration = self.data['render_props']['motion_blur']['rolling_shutter_duration']
        # self.data['render_props']['motion_blur']['shutter_curve'] = {} # not available ATM

        # Render Properties - Performance
        bpy.context.scene.render.threads_mode = self.data['render_props']['performance']['threads']['threads_mode']
        bpy.context.scene.render.threads = self.data['render_props']['performance']['threads']['threads']
        bpy.context.scene.cycles.use_auto_tile = self.data['render_props']['performance']['memory']['use_auto_tile']
        bpy.context.scene.cycles.tile_size = self.data['render_props']['performance']['memory']['tile_size']
        bpy.context.scene.render.use_persistent_data = self.data['render_props']['performance']['final_render']['use_persistent_data']
        bpy.context.scene.render.preview_pixel_size =  self.data['render_props']['performance']['viewport']['preview_pixel_size']        

        # Render Properties - Sampling
        bpy.context.scene.cycles.use_preview_adaptive_sampling = self.data['render_props']['sampling']['viewport']['use_preview_adaptive_sampling']
        bpy.context.scene.cycles.preview_adaptive_threshold = self.data['render_props']['sampling']['viewport']['preview_adaptive_threshold']
        bpy.context.scene.cycles.preview_samples = self.data['render_props']['sampling']['viewport']['preview_samples']
        bpy.context.scene.cycles.preview_adaptive_min_samples = self.data['render_props']['sampling']['viewport']['preview_adaptive_min_samples']
        bpy.context.scene.cycles.use_preview_denoising = self.data['render_props']['sampling']['viewport']['use_preview_denoising']
        bpy.context.scene.cycles.preview_denoiser = self.data['render_props']['sampling']['viewport']['preview_denoiser']
        bpy.context.scene.cycles.preview_denoising_input_passes = self.data['render_props']['sampling']['viewport']['preview_denoising_input_passes']
        bpy.context.scene.cycles.preview_denoising_start_sample = self.data['render_props']['sampling']['viewport']['preview_denoising_start_sample']
        bpy.context.scene.cycles.use_adaptive_sampling = self.data['render_props']['sampling']['render']['use_adaptive_sampling']
        bpy.context.scene.cycles.adaptive_threshold = self.data['render_props']['sampling']['render']['adaptive_threshold']
        bpy.context.scene.cycles.samples = self.data['render_props']['sampling']['render']['samples']
        bpy.context.scene.cycles.adaptive_min_samples = self.data['render_props']['sampling']['render']['adaptive_min_samples']
        bpy.context.scene.cycles.time_limit = self.data['render_props']['sampling']['render']['time_limit']
        bpy.context.scene.cycles.use_denoising = self.data['render_props']['sampling']['render']['use_denoising']
        bpy.context.scene.cycles.denoiser = self.data['render_props']['sampling']['render']['denoiser']
        bpy.context.scene.cycles.denoising_prefilter = self.data['render_props']['sampling']['render']['denoising_prefilter']
        bpy.context.scene.cycles.seed = self.data['render_props']['sampling']['advanced']['seed']
        bpy.context.scene.cycles.sampling_pattern = self.data['render_props']['sampling']['advanced']['sampling_pattern']
        bpy.context.scene.cycles.sample_offset = self.data['render_props']['sampling']['advanced']['sample_offset']
        bpy.context.scene.cycles.auto_scrambling_distance = self.data['render_props']['sampling']['advanced']['auto_scrambling_distance']
        bpy.context.scene.cycles.preview_scrambling_distance = self.data['render_props']['sampling']['advanced']['preview_scrambling_distance']
        bpy.context.scene.cycles.scrambling_distance = self.data['render_props']['sampling']['advanced']['scrambling_distance']
        bpy.context.scene.cycles.min_light_bounces = self.data['render_props']['sampling']['advanced']['min_light_bounces']
        bpy.context.scene.cycles.min_transparent_bounces = self.data['render_props']['sampling']['advanced']['min_transparent_bounces']
        bpy.context.scene.cycles.light_sampling_threshold = self.data['render_props']['sampling']['advanced']['light_sampling_threshold']

        # Render Properties - Simplify
        bpy.context.scene.render.use_simplify = self.data['render_props']['simplify']['use_simplify']
        bpy.context.scene.render.simplify_child_particles = self.data['render_props']['simplify']['viewport']['simplify_child_particles']
        bpy.context.scene.cycles.texture_limit = self.data['render_props']['simplify']['viewport']['texture_limit']
        bpy.context.scene.render.simplify_volumes = self.data['render_props']['simplify']['viewport']['simplify_volumes']
        bpy.context.scene.render.simplify_subdivision_render = self.data['render_props']['simplify']['render']['simplify_subdivision_render']
        bpy.context.scene.render.simplify_child_particles_render = self.data['render_props']['simplify']['render']['simplify_child_particles_render']
        bpy.context.scene.cycles.texture_limit_render = self.data['render_props']['simplify']['render']['texture_limit_render']
        bpy.context.scene.cycles.use_camera_cull  = self.data['render_props']['simplify']['culling']['use_camera_cull']
        bpy.context.scene.cycles.camera_cull_margin = self.data['render_props']['simplify']['culling']['camera_cull_margin']
        bpy.context.scene.cycles.use_distance_cull  = self.data['render_props']['simplify']['culling']['use_distance_cull']
        bpy.context.scene.cycles.distance_cull_margin = self.data['render_props']['simplify']['culling']['distance_cull_margin']
        bpy.context.scene.render.simplify_gpencil = self.data['render_props']['simplify']['grease_pencil']['simplify_gpencil']
        bpy.context.scene.render.simplify_gpencil_onplay = self.data['render_props']['simplify']['grease_pencil']['simplify_gpencil_onplay']
        bpy.context.scene.render.simplify_gpencil_view_fill = self.data['render_props']['simplify']['grease_pencil']['simplify_gpencil_view_fill']
        bpy.context.scene.render.simplify_gpencil_modifier = self.data['render_props']['simplify']['grease_pencil']['simplify_gpencil_modifier']
        bpy.context.scene.render.simplify_gpencil_shader_fx = self.data['render_props']['simplify']['grease_pencil']['simplify_gpencil_shader_fx']
        bpy.context.scene.render.simplify_gpencil_tint = self.data['render_props']['simplify']['grease_pencil']['simplify_gpencil_tint']
        bpy.context.scene.render.simplify_gpencil_antialiasing = self.data['render_props']['simplify']['grease_pencil']['simplify_gpencil_antialiasing']
        
        # Render Properties - Volumes
        bpy.context.scene.cycles.volume_step_rate = self.data['render_props']['volumes']['volume_step_rate']
        bpy.context.scene.cycles.volume_preview_step_rate = self.data['render_props']['volumes']['volume_preview_step_rate']
        bpy.context.scene.cycles.volume_max_steps = self.data['render_props']['volumes']['volume_max_steps']

    def loadCyclesOutputProps(self, props):
        print("Loading Cycles Output properties...")
        # Format
        bpy.context.scene.render.resolution_x = self.data['output_props']['format']['resolution_x']
        bpy.context.scene.render.resolution_y = self.data['output_props']['format']['resolution_y']
        bpy.context.scene.render.resolution_percentage = self.data['output_props']['format']['resolution_percentage']
        bpy.context.scene.render.pixel_aspect_x = self.data['output_props']['format']['pixel_aspect_x']
        bpy.context.scene.render.pixel_aspect_y = self.data['output_props']['format']['pixel_aspect_y']
        bpy.context.scene.render.use_border = self.data['output_props']['format']['render_region']
        bpy.context.scene.render.use_crop_to_border = self.data['output_props']['format']['crop_to_render_region']

        # Frame Range
        bpy.context.scene.frame_start = self.data['output_props']['frame_range']['frame_start']
        bpy.context.scene.frame_end = self.data['output_props']['frame_range']['frame_end']
        bpy.context.scene.frame_step = self.data['output_props']['frame_range']['frame_step']
        bpy.context.scene.render.frame_map_old = self.data['output_props']['frame_range']['frame_map_old']
        bpy.context.scene.render.frame_map_new = self.data['output_props']['frame_range']['frame_map_new']

        # Metadata
        bpy.context.scene.render.metadata_input = self.data['output_props']['metadata']['metadata_input']
        bpy.context.scene.render.use_stamp_date = self.data['output_props']['metadata']['use_stamp_date']
        bpy.context.scene.render.use_stamp_time = self.data['output_props']['metadata']['use_stamp_time']
        bpy.context.scene.render.use_stamp_render_time = self.data['output_props']['metadata']['use_stamp_render_time']
        bpy.context.scene.render.use_stamp_frame = self.data['output_props']['metadata']['use_stamp_frame']
        bpy.context.scene.render.use_stamp_frame_range = self.data['output_props']['metadata']['use_stamp_frame_range']
        bpy.context.scene.render.use_stamp_memory = self.data['output_props']['metadata']['use_stamp_memory']
        bpy.context.scene.render.use_stamp_hostname = self.data['output_props']['metadata']['use_stamp_hostname']
        bpy.context.scene.render.use_stamp_camera = self.data['output_props']['metadata']['use_stamp_camera']
        bpy.context.scene.render.use_stamp_lens = self.data['output_props']['metadata']['use_stamp_lens']
        bpy.context.scene.render.use_stamp_scene = self.data['output_props']['metadata']['use_stamp_scene']
        bpy.context.scene.render.use_stamp_marker = self.data['output_props']['metadata']['use_stamp_marker']
        bpy.context.scene.render.use_stamp_filename = self.data['output_props']['metadata']['use_stamp_filename']
        bpy.context.scene.render.use_stamp_sequencer_strip = self.data['output_props']['metadata']['use_stamp_sequencer_strip']
        bpy.context.scene.render.use_stamp_note = self.data['output_props']['metadata']['use_stamp_note']
        bpy.context.scene.render.stamp_note_text = self.data['output_props']['metadata']['stamp_note_text']
        bpy.context.scene.render.use_stamp = self.data['output_props']['metadata']['use_stamp']
        if bpy.context.scene.render.use_stamp == True:
            bpy.context.scene.render.stamp_font_size = self.data['output_props']['metadata']['stamp_font_size']
            bpy.context.scene.render.stamp_foreground = self.stringToColor(self.data['output_props']['metadata']['stamp_foreground'])
            bpy.context.scene.render.stamp_background = self.stringToColor(self.data['output_props']['metadata']['stamp_background'])
            bpy.context.scene.render.use_stamp_labels = self.data['output_props']['metadata']['use_stamp_labels']

        # Output Properties - Output
        bpy.context.scene.render.filepath = self.data['output_props']['output']['filepath']
        bpy.context.scene.render.use_file_extension = self.data['output_props']['output']['use_file_extension']
        bpy.context.scene.render.use_render_cache = self.data['output_props']['output']['use_render_cache']
        bpy.context.scene.render.image_settings.file_format = self.data['output_props']['output']['file_format']
        bpy.context.scene.render.image_settings.color_mode = self.data['output_props']['output']['color_mode']
        bpy.context.scene.render.image_settings.quality = self.data['output_props']['output']['quality']
        bpy.context.scene.render.image_settings.color_depth = self.data['output_props']['output']['color_depth']
        bpy.context.scene.render.image_settings.compression = self.data['output_props']['output']['compression']
        bpy.context.scene.render.image_settings.jpeg2k_codec = self.data['output_props']['output']['image_settings']['codec']
        bpy.context.scene.render.image_settings.use_jpeg2k_cinema_preset = self.data['output_props']['output']['image_settings']['use_jpeg2k_cinema_preset']
        bpy.context.scene.render.image_settings.use_jpeg2k_cinema_48 = self.data['output_props']['output']['image_settings']['use_jpeg2k_cinema_48']
        bpy.context.scene.render.image_settings.use_jpeg2k_ycc = self.data['output_props']['output']['image_settings']['use_jpeg2k_ycc']
        bpy.context.scene.render.use_overwrite = self.data['output_props']['output']['image_sequence']['overwrite']
        bpy.context.scene.render.use_placeholder = self.data['output_props']['output']['image_sequence']['use_placeholder']

        bpy.context.scene.render.image_settings.views_format = self.data['output_props']['output']['views']['views_format']
        bpy.context.scene.render.image_settings.quality = self.data['output_props']['output']['views']['quality']
        # self.data['output_props']['output']['views']['stereo_mode'] = bpy.data.scenes["Scene"].(null)
        # self.data['output_props']['output']['views']['interlace_type'] = bpy.data.scenes["Scene"].(null)'
        # self.data['output_props']['output']['views']['swap_left_right'] = bpy.data.scenes["Scene"].(null)
        bpy.context.scene.render.image_settings.color_management = self.data['output_props']['output']['color_management']['type']
        bpy.context.scene.display_settings.display_device = self.data['output_props']['output']['color_management']['display_device']
        bpy.context.scene.view_settings.view_transform = self.data['output_props']['output']['color_management']['view_transform']
        bpy.context.scene.view_settings.look = self.data['output_props']['output']['color_management']['look']
        bpy.context.scene.view_settings.exposure = self.data['output_props']['output']['color_management']['exposure']
        bpy.context.scene.view_settings.gamma  = self.data['output_props']['output']['color_management']['gamma']
        bpy.context.scene.view_settings.use_curve_mapping = self.data['output_props']['output']['color_management']['use_curve_mapping']
        # curve info is not currently readable.

        # Post Processing
        bpy.context.scene.render.use_compositing = self.data['output_props']['post_processing']['use_compositing']
        bpy.context.scene.render.use_sequencer = self.data['output_props']['post_processing']['use_sequencer']
        bpy.context.scene.render.dither_intensity  = self.data['output_props']['post_processing']['dither_intensity']

        # Output Properties - Stereoscopy
        bpy.context.scene.render.use_multiview = self.data['output_props']['stereoscopy']['use_multiview']
        bpy.context.scene.render.views_format = self.data['output_props']['stereoscopy']['views_format']
        bpy.context.scene.render.views["left"].use = self.data['output_props']['stereoscopy']['use_left']
        bpy.context.scene.render.views["right"].use = self.data['output_props']['stereoscopy']['use_right']
        bpy.context.scene.render.views["left"].camera_suffix = self.data['output_props']['stereoscopy']['left_suffix']
        bpy.context.scene.render.views["right"].camera_suffix = self.data['output_props']['stereoscopy']['right_suffix']


    def loadCyclesViewLayerProps(self, props):
        print("Loading Cycles View Layer properties...")
        bpy.context.scene.view_layers["ViewLayer"].use = self.data['viewlayer_props']['use']
        bpy.context.scene.render.use_single_layer = self.data['viewlayer_props']['use_single_layer']

        # View Layer Properties - Passes
        bpy.context.scene.view_layers["ViewLayer"].use_pass_combined = self.data['viewlayer_props']['passes']['data']['use_pass_combined']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_z = self.data['viewlayer_props']['passes']['data']['use_pass_z']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_mist = self.data['viewlayer_props']['passes']['data']['use_pass_mist']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_position = self.data['viewlayer_props']['passes']['data']['use_pass_position']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_normal = self.data['viewlayer_props']['passes']['data']['use_pass_normal']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_vector = self.data['viewlayer_props']['passes']['data']['use_pass_vector']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_uv = self.data['viewlayer_props']['passes']['data']['use_pass_uv']
        # bpy.data.scenes["Scene"].(null) = self.data['viewlayer_props']['passes']['data']['use_denoising_data']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_object_index = self.data['viewlayer_props']['passes']['data']['use_pass_object_index']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_material_index = self.data['viewlayer_props']['passes']['data']['use_pass_material_index']
        # bpy.data.scenes["Scene"].(null) = self.data['viewlayer_props']['passes']['data']['use_debug_sample_count']
        bpy.context.scene.view_layers["ViewLayer"].pass_alpha_threshold = self.data['viewlayer_props']['passes']['data']['pass_alpha_threshold']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_diffuse_direct  = self.data['viewlayer_props']['passes']['light']['use_pass_diffuse_direct']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_diffuse_indirect = self.data['viewlayer_props']['passes']['light']['use_pass_diffuse_indirect']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_diffuse_color = self.data['viewlayer_props']['passes']['light']['use_pass_diffuse_color']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_glossy_direct = self.data['viewlayer_props']['passes']['light']['use_pass_glossy_direct']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_glossy_indirect = self.data['viewlayer_props']['passes']['light']['use_pass_glossy_indirect']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_glossy_color = self.data['viewlayer_props']['passes']['light']['use_pass_glossy_color']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_transmission_direct = self.data['viewlayer_props']['passes']['light']['use_pass_transmission_direct']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_transmission_indirect = self.data['viewlayer_props']['passes']['light']['use_pass_transmission_indirect']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_transmission_color = self.data['viewlayer_props']['passes']['light']['use_pass_transmission_color']
        # bpy.data.scenes["Scene"].(null) = self.data['viewlayer_props']['passes']['light']['use_pass_volume_direct']
        # bpy.data.scenes["Scene"].(null) = self.data['viewlayer_props']['passes']['light']['use_pass_volume_indirect']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_emit = self.data['viewlayer_props']['passes']['light']['use_pass_emit']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_environment = self.data['viewlayer_props']['passes']['light']['use_pass_environment']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_shadow = self.data['viewlayer_props']['passes']['light']['use_pass_shadow']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_ambient_occlusion = self.data['viewlayer_props']['passes']['light']['use_pass_ambient_occlusion']
        # bpy.data.scenes["Scene"].(null) = self.data['viewlayer_props']['passes']['light']['use_shadow_catcher']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_object = self.data['viewlayer_props']['passes']['cryptomatte']['use_pass_cryptomatte_object']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_material = self.data['viewlayer_props']['passes']['cryptomatte']['use_pass_cryptomatte_material']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_asset = self.data['viewlayer_props']['passes']['cryptomatte']['use_pass_cryptomatte_asset']
        bpy.context.scene.view_layers["ViewLayer"].pass_cryptomatte_depth = self.data['viewlayer_props']['passes']['cryptomatte']['pass_cryptomatte_depth']
        # self.data['viewlayer_props']['passes']['shader_aov'] = {}
        # self.data['viewlayer_props']['passes']['light_groups'] = {}

        # View Layer Properties - Filter
        bpy.context.scene.view_layers["ViewLayer"].use_sky = self.data['viewlayer_props']['filter']['use_sky']
        bpy.context.scene.view_layers["ViewLayer"].use_solid = self.data['viewlayer_props']['filter']['use_solid']
        bpy.context.scene.view_layers["ViewLayer"].use_strand = self.data['viewlayer_props']['filter']['use_strand']
        bpy.context.scene.view_layers["ViewLayer"].use_volumes = self.data['viewlayer_props']['filter']['use_volumes']
        bpy.context.scene.view_layers["ViewLayer"].use_motion_blur = self.data['viewlayer_props']['filter']['use_motion_blur']
        # bpy.data.scenes["Scene"].(null)  = self.data['viewlayer_props']['filter']['use_denoising']

        # View Layer Properties - Override
        # TODO - Handle material
        # bpy.context.scene.view_layers["ViewLayer"].material_override = self.data['viewlayer_props']['override']['material_override']
        bpy.context.scene.view_layers["ViewLayer"].samples = self.data['viewlayer_props']['override']['samples']

        # View Layer Properties - Custom Properties - TODO - FUTURE
        # self.data['viewlayer_props']['custom_props'] = {}

    def loadCyclesSceneProps(self, props):
        print("Loading Cycles Scene properties...")
        # Scene Properties - Scene
        # I need to figure out how to serialize the camera. Value printed is:
        # <bpy_struct, Object("Camera") at 0x000002EE7C60B908>
        # self.data['scene_props']['scene']['camera'] = bpy.context.scene.camera
        # print('scene_props.scene.camera = ')
        # print(bpy.context.scene.camera)
        # print('*****************************')
        # print('*****************************')
        # print('*****************************')
        # I suspect the following 2 lines will also fail 
        # self.data['scene_props']['scene']['background_set'] = bpy.context.scene.background_set
        # self.data['scene_props']['scene']['active_clip'] = bpy.context.scene.active_clip # Is this right?
        # Scene Properties - Units
        bpy.context.scene.unit_settings.system = self.data['scene_props']['units']['system']
        bpy.context.scene.unit_settings.scale_length = self.data['scene_props']['units']['scale_length']
        bpy.context.scene.unit_settings.use_separate = self.data['scene_props']['units']['use_separate']
        bpy.context.scene.unit_settings.system_rotation = self.data['scene_props']['units']['system_rotation']
        bpy.context.scene.unit_settings.length_unit = self.data['scene_props']['units']['length_unit']
        bpy.context.scene.unit_settings.mass_unit = self.data['scene_props']['units']['mass_unit']
        bpy.context.scene.unit_settings.time_unit = self.data['scene_props']['units']['time_unit']
        bpy.context.scene.unit_settings.temperature_unit = self.data['scene_props']['units']['temperature_unit']
        # Scene Properties - Gravity
        bpy.context.scene.use_gravity = self.data['scene_props']['gravity']['use_gravity']
        bpy.context.scene.gravity[0] = self.data['scene_props']['gravity']['gravity_x']
        bpy.context.scene.gravity[1] = self.data['scene_props']['gravity']['gravity_y']
        bpy.context.scene.gravity[2] = self.data['scene_props']['gravity']['gravity_z']
        # Scene Properties - Keying Sets
        # self.data['scene_props']['keying_sets'] = {} # TODO
        # Scene Properties - Audio
        bpy.context.scene.audio_volume = self.data['scene_props']['audio']['volume']
        bpy.context.scene.audio_distance_model = self.data['scene_props']['audio']['audio_distance_model']
        bpy.context.scene.audio_doppler_speed = self.data['scene_props']['audio']['audio_doppler_speed']
        bpy.context.scene.audio_doppler_factor = self.data['scene_props']['audio']['audio_doppler_factor']
        # Scene Properties - Rigid Body  World
        # self.data['scene_props']['rigid_body_world'] = {} # TODO FUTURE
        # Scene Properties - Custom Properties
        # self.data['scene_props']['custom_properties'] = {} # TODO FUTURE

    def loadCyclesWorldProps(self, props):
        print("Loading Cycles World properties...")
        # TBD TODO
        # self.data['world_props']['surface']['surface'] = bpy.data.worlds["World"].node_tree.nodes["Translucent BSDF"].inputs[0].default_value
        # self.data['world_props']['surface']['color'] = bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value
        # self.data['world_props']['surface']['strength'] = bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value
        # World Properties - Volume

        # TBD - Its not clear to me how to get/set this data reliably.
        # self.data['world_props']['mist_pass'] = {}
        # self.data['world_props']['mist_pass']['start'] = bpy.context.scene.world.mist_settings.start
        # self.data['world_props']['mist_pass']['depth'] = bpy.context.scene.world.mist_settings.depth
        # self.data['world_props']['mist_pass']['falloff'] = bpy.context.scene.world.mist_settings.falloff
        bpy.context.scene.world.cycles_visibility.camera = self.data['world_props']['ray_visibility']['camera']
        bpy.context.scene.world.cycles_visibility.diffuse = self.data['world_props']['ray_visibility']['diffuse']
        bpy.context.scene.world.cycles_visibility.glossy = self.data['world_props']['ray_visibility']['glossy']
        bpy.context.scene.world.cycles_visibility.transmission = self.data['world_props']['ray_visibility']['transmission']
        bpy.context.scene.world.cycles_visibility.scatter = self.data['world_props']['ray_visibility']['scatter']
        bpy.context.scene.world.cycles.sampling_method = self.data['world_props']['settings']['surface']['sampling_method']
        bpy.context.scene.world.cycles.sample_map_resolution = self.data['world_props']['settings']['surface']['sample_map_resolution']
        bpy.context.scene.world.cycles.max_bounces = self.data['world_props']['settings']['surface']['max_bounces']
        bpy.context.scene.world.cycles.is_caustics_light = self.data['world_props']['settings']['surface']['is_caustics_light']
        bpy.context.scene.world.cycles.volume_sampling = self.data['world_props']['settings']['volume']['volume_sampling']
        bpy.context.scene.world.cycles.volume_interpolation = self.data['world_props']['settings']['volume']['volume_interpolation']
        bpy.context.scene.world.cycles.homogeneous_volume = self.data['world_props']['settings']['volume']['homogeneous_volume']
        bpy.context.scene.world.cycles.volume_step_size = self.data['world_props']['settings']['volume']['volume_step_size']
        # self.data['world_props']['settings']['light_group'] = {} # TBD FUTURE
        print("Color string =  " + self.data['world_props']['settings']['viewport_display']['color'])
        print("Color value =  " + str(self.stringToColor(self.data['world_props']['settings']['viewport_display']['color'])))
        bpy.context.scene.world.color = self.stringToColor(self.data['world_props']['settings']['viewport_display']['color'])
        # self.data['world_props']['custom_properties'] = {} # TBD FUTURE

    def loadCyclesCollectionProps(self, props):
        print("Loading Cycles Collection properties...")
        bpy.data.collections["Collection"].hide_select = self.data['collection_props']['restrictions']['hide_select']
        bpy.data.collections["Collection"].hide_render = self.data['collection_props']['restrictions']['hide_render']
        # self.data['collection_props']['restrictions']['holdout'] = bpy.data.scenes["Scene"].(null)
        # self.data['collection_props']['restrictions']['indirect_only'] = bpy.data.scenes["Scene"].(null)
        bpy.data.collections["Collection"].instance_offset[0] = self.data['collection_props']['instancing']['instance_offset_x']
        bpy.data.collections["Collection"].instance_offset[1] = self.data['collection_props']['instancing']['instance_offset_y']
        bpy.data.collections["Collection"].instance_offset[2] = self.data['collection_props']['instancing']['instance_offset_z']
        bpy.data.collections["Collection"].lineart_usage = self.data['collection_props']['line_art']['lineart_usage']
        bpy.data.collections["Collection"].lineart_use_intersection_mask = self.data['collection_props']['line_art']['lineart_use_intersection_mask']
        # if the use_lineart_intersection_masks is checked, then these are valid
        bpy.data.collections["Collection"].lineart_intersection_mask[0] = self.data['collection_props']['line_art']['lineart_intersection_mask_0']
        bpy.data.collections["Collection"].lineart_intersection_mask[1] = self.data['collection_props']['line_art']['lineart_intersection_mask_1']
        bpy.data.collections["Collection"].lineart_intersection_mask[2] = self.data['collection_props']['line_art']['lineart_intersection_mask_2']
        bpy.data.collections["Collection"].lineart_intersection_mask[3] = self.data['collection_props']['line_art']['lineart_intersection_mask_3']
        bpy.data.collections["Collection"].lineart_intersection_mask[4] = self.data['collection_props']['line_art']['lineart_intersection_mask_4']
        bpy.data.collections["Collection"].lineart_intersection_mask[5] = self.data['collection_props']['line_art']['lineart_intersection_mask_5']
        bpy.data.collections["Collection"].lineart_intersection_mask[6] = self.data['collection_props']['line_art']['lineart_intersection_mask_6']
        bpy.data.collections["Collection"].lineart_intersection_mask[7] = self.data['collection_props']['line_art']['lineart_intersection_mask_7']
        bpy.data.collections["Collection"].use_lineart_intersection_priority = self.data['collection_props']['line_art']['use_lineart_intersection_priority']
        bpy.data.collections["Collection"].lineart_intersection_priority = self.data['collection_props']['line_art']['lineart_intersection_priority']

    def loadCyclesTextureProps(self, props):
        print("Loading Cycles Texture properties...")
        # TODO FUTURE

    def loadEevee(self, context):
        scene = context.scene
        my_props = scene.my_props

        # =================
        # Render Properties
        # =================
        # Always load the core Render Properties
        context.scene.render.engine = self.data['render_props']['engine']

        # print("my_props:")
        # print(list(my_props.keys()))
        if(my_props.load_pref_render == True):
            self.loadEeveeRenderProps(my_props)

        # ====================
        # Workspace Properties
        # ====================
        # if load_pref_render["load_pref_workspace"]:
        if(my_props.load_pref_workspace == True):
            self.loadEeveeWorkspaceProps(my_props)

        # ===============
        # Output Settings
        # ===============
        if(my_props.load_pref_output == True):
            self.loadEeveeOutputProps(my_props)

        # ===================
        # View Layer Settings
        # ===================
        if(my_props.load_pref_view_layer == True):
            self.loadEeveeViewLayerProps(my_props)

        # ===================
        # Scene Properties
        # ===================
        if(my_props.load_pref_scene == True):
            self.loadEeveeSceneProps(my_props)

        #=================
        # World Properties
        #=================
        if(my_props.load_pref_world == True):
            self.loadEeveeWorldProps(my_props)

        #======================
        # Collection Properties
        #======================
        if(my_props.load_pref_collection == True):
            self.loadEeveeCollectionProps(my_props)

    def loadEeveeWorkspaceProps(self, props):
        bpy.context.scene.tool_settings.use_transform_data_origin = self.data['workspace']['options']['transform']['use_transform_data_origin']
        bpy.context.scene.tool_settings.use_transform_pivot_point_align = self.data['workspace']['options']['transform']['use_transform_pivot_point_align']
        bpy.context.scene.tool_settings.use_transform_skip_children = self.data['workspace']['options']['transform']['use_transform_skip_children']
        bpy.data.workspaces["Scripting"].use_pin_scene = self.data['workspace']['workspace']['use_pin_scene']
        bpy.data.workspaces["Scripting"].object_mode = self.data['workspace']['workspace']['object_mode']
        bpy.data.workspaces["Scripting"].use_filter_by_owner = self.data['workspace']['workspace']['filter_addons']['use_filter_by_owner']

    def loadEeveeRenderProps(self, props):
        bpy.context.scene.eevee.taa_render_samples = self.data['render_props']['sampling']['render_samples']
        bpy.context.scene.eevee.taa_samples = self.data['render_props']['sampling']['viewport_samples']
        bpy.context.scene.eevee.use_taa_reprojection = self.data['render_props']['sampling']['viewport_denoising']
        bpy.context.scene.eevee.use_gtao = self.data['render_props']['sampling']['ambient_occlusion']['use_gtao']
        bpy.context.scene.eevee.gtao_distance = self.data['render_props']['sampling']['ambient_occlusion']['gtao_distance']
        bpy.context.scene.eevee.gtao_factor = self.data['render_props']['sampling']['ambient_occlusion']['gtao_factor']
        bpy.context.scene.eevee.gtao_quality = self.data['render_props']['sampling']['ambient_occlusion']['gtao_quality']
        bpy.context.scene.eevee.use_gtao_bent_normals = self.data['render_props']['sampling']['ambient_occlusion']['use_gtao_bent_normals']
        bpy.context.scene.eevee.use_gtao_bounce = self.data['render_props']['sampling']['ambient_occlusion']['use_gtao_bounce']

        bpy.context.scene.eevee.use_bloom = self.data['render_props']['sampling']['bloom']['use_bloom']
        bpy.context.scene.eevee.bloom_threshold = self.data['render_props']['sampling']['bloom']['bloom_threshold']
        bpy.context.scene.eevee.bloom_knee = self.data['render_props']['sampling']['bloom']['bloom_knee']
        bpy.context.scene.eevee.bloom_radius = self.data['render_props']['sampling']['bloom']['bloom_radius']
        bpy.context.scene.eevee.bloom_color = self.stringToColor(self.data['render_props']['sampling']['bloom']['bloom_color'])
        bpy.context.scene.eevee.bloom_intensity= self.data['render_props']['sampling']['bloom']['bloom_intensity']
        bpy.context.scene.eevee.bloom_clamp = self.data['render_props']['sampling']['bloom']['bloom_clamp']
        # Depth of Field
        bpy.context.scene.eevee.bokeh_max_size = self.data['render_props']['sampling']['depth_of_field']['bokeh_max_size']
        bpy.context.scene.eevee.bokeh_threshold = self.data['render_props']['sampling']['depth_of_field']['bokeh_threshold']
        bpy.context.scene.eevee.bokeh_neighbor_max = self.data['render_props']['sampling']['depth_of_field']['bokeh_neighbor_max']
        bpy.context.scene.eevee.bokeh_denoise_fac = self.data['render_props']['sampling']['depth_of_field']['bokeh_denoise_fac']
        bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = self.data['render_props']['sampling']['depth_of_field']['use_bokeh_high_quality_slight_defocus']
        bpy.context.scene.eevee.use_bokeh_jittered = self.data['render_props']['sampling']['depth_of_field']['use_bokeh_jittered']
        bpy.context.scene.eevee.bokeh_overblur = self.data['render_props']['sampling']['depth_of_field']['bokeh_overblur']
        # Subsurface Scattering
        bpy.context.scene.eevee.sss_samples = self.data['render_props']['sampling']['subsurface_scattering']['sss_samples']
        bpy.context.scene.eevee.sss_jitter_threshold = self.data['render_props']['sampling']['subsurface_scattering']['sss_jitter_threshold']
        # Screen Space Reflections
        bpy.context.scene.eevee.use_ssr = self.data['render_props']['sampling']['screen_space_reflections']['use_ssr']
        bpy.context.scene.eevee.use_ssr_refraction = self.data['render_props']['sampling']['screen_space_reflections']['use_ssr_refraction']
        bpy.context.scene.eevee.use_ssr_halfres = self.data['render_props']['sampling']['screen_space_reflections']['use_ssr_halfres']
        bpy.context.scene.eevee.ssr_quality = self.data['render_props']['sampling']['screen_space_reflections']['ssr_quality']
        bpy.context.scene.eevee.ssr_max_roughness = self.data['render_props']['sampling']['screen_space_reflections']['ssr_max_roughness']
        bpy.context.scene.eevee.ssr_thickness = self.data['render_props']['sampling']['screen_space_reflections']['ssr_thickness']
        bpy.context.scene.eevee.ssr_border_fade = self.data['render_props']['sampling']['screen_space_reflections']['ssr_border_fade']
        bpy.context.scene.eevee.ssr_firefly_fac = self.data['render_props']['sampling']['screen_space_reflections']['ssr_firefly_fac']
        # Motion Blur
        bpy.context.scene.eevee.motion_blur_position = self.data['render_props']['motion_blur']['motion_blur_position']
        bpy.context.scene.eevee.motion_blur_shutter = self.data['render_props']['motion_blur']['motion_blur_shutter']
        bpy.context.scene.eevee.motion_blur_depth_scale = self.data['render_props']['motion_blur']['motion_blur_depth_scale']
        bpy.context.scene.eevee.motion_blur_max = self.data['render_props']['motion_blur']['motion_blur_max']
        bpy.context.scene.eevee.motion_blur_steps = self.data['render_props']['motion_blur']['motion_blur_steps']
        # Volumetrics
        bpy.context.scene.eevee.volumetric_start = self.data['render_props']['volumetrics']['volumetric_start']
        bpy.context.scene.eevee.volumetric_end = self.data['render_props']['volumetrics']['volumetric_end']
        bpy.context.scene.eevee.volumetric_tile_size = self.data['render_props']['volumetrics']['volumetric_tile_size']
        bpy.context.scene.eevee.volumetric_samples = self.data['render_props']['volumetrics']['volumetric_samples']
        bpy.context.scene.eevee.volumetric_sample_distribution = self.data['render_props']['volumetrics']['volumetric_sample_distribution']
        bpy.context.scene.eevee.use_volumetric_lights = self.data['render_props']['volumetrics']['use_volumetric_lights']
        bpy.context.scene.eevee.use_volumetric_lights = self.data['render_props']['volumetrics']['use_volumetric_lights']
        bpy.context.scene.eevee.volumetric_light_clamp = self.data['render_props']['volumetrics']['volumetric_light_clamp']
        bpy.context.scene.eevee.use_volumetric_shadows = self.data['render_props']['volumetrics']['use_volumetric_shadows']
        bpy.context.scene.eevee.volumetric_shadow_samples = self.data['render_props']['volumetrics']['volumetric_shadow_samples']
        # Performnce
        bpy.context.scene.render.use_high_quality_normals = self.data['render_props']['performance']['use_high_quality_normals']
        # Curves
        bpy.context.scene.render.hair_type = self.data['render_props']['curves']['hair_type']
        bpy.context.scene.render.hair_subdiv = self.data['render_props']['curves']['hair_subdiv']
        # Shadows
        bpy.context.scene.eevee.shadow_cube_size = self.data['render_props']['shadows']['shadow_cube_size']
        bpy.context.scene.eevee.shadow_cascade_size = self.data['render_props']['shadows']['shadow_cascade_size']
        bpy.context.scene.eevee.use_shadow_high_bitdepth = self.data['render_props']['shadows']['use_shadow_high_bitdepth']
        bpy.context.scene.eevee.use_soft_shadows = self.data['render_props']['shadows']['use_soft_shadows']
        bpy.context.scene.eevee.light_threshold = self.data['render_props']['shadows']['light_threshold']
        # Indirect Lighting
        bpy.context.scene.eevee.gi_auto_bake = self.data['render_props']['indirect_lighting']['gi_auto_bake']
        bpy.context.scene.eevee.gi_diffuse_bounces = self.data['render_props']['indirect_lighting']['gi_diffuse_bounces']
        bpy.context.scene.eevee.gi_cubemap_resolution = self.data['render_props']['indirect_lighting']['gi_cubemap_resolution']
        bpy.context.scene.eevee.gi_visibility_resolution = self.data['render_props']['indirect_lighting']['gi_visibility_resolution']
        bpy.context.scene.eevee.gi_irradiance_smoothing = self.data['render_props']['indirect_lighting']['gi_irradiance_smoothing']
        bpy.context.scene.eevee.gi_glossy_clamp = self.data['render_props']['indirect_lighting']['gi_glossy_clamp']
        bpy.context.scene.eevee.gi_filter_quality = self.data['render_props']['indirect_lighting']['gi_filter_quality']
        bpy.context.scene.eevee.gi_cubemap_display_size = self.data['render_props']['indirect_lighting']['gi_cubemap_display_size']
        bpy.context.scene.eevee.gi_irradiance_display_size = self.data['render_props']['indirect_lighting']['gi_irradiance_display_size']
        # Film
        bpy.context.scene.render.filter_size = self.data['render_props']['film']['filter_size']
        bpy.context.scene.render.film_transparent = self.data['render_props']['film']['film_transparent']
        bpy.context.scene.eevee.overscan_size = self.data['render_props']['film']['overscan_size']
        bpy.context.scene.eevee.use_overscan = self.data['render_props']['film']['use_overscan']
        # Simplify
        bpy.context.scene.render.use_simplify = self.data['render_props']['simplify']['use_simplify']
        bpy.context.scene.render.simplify_subdivision = self.data['render_props']['simplify']['simplify_subdivision']
        bpy.context.scene.render.simplify_child_particles = self.data['render_props']['simplify']['simplify_child_particles']
        bpy.context.scene.render.simplify_volumes = self.data['render_props']['simplify']['simplify_volumes']
        bpy.context.scene.render.simplify_subdivision_render = self.data['render_props']['simplify']['simplify_subdivision_render']
        bpy.context.scene.render.simplify_child_particles_render = self.data['render_props']['simplify']['simplify_child_particles_render']
        bpy.context.scene.render.simplify_gpencil = self.data['render_props']['simplify']['simplify_gpencil']
        bpy.context.scene.render.simplify_gpencil_onplay = self.data['render_props']['simplify']['simplify_gpencil_onplay']
        bpy.context.scene.render.simplify_gpencil_view_fill = self.data['render_props']['simplify']['simplify_gpencil_view_fill']
        bpy.context.scene.render.simplify_gpencil_modifier = self.data['render_props']['simplify']['simplify_gpencil_modifier']
        bpy.context.scene.render.simplify_gpencil_shader_fx = self.data['render_props']['simplify']['simplify_gpencil_shader_fx']
        bpy.context.scene.render.simplify_gpencil_tint = self.data['render_props']['simplify']['simplify_gpencil_tint']
        bpy.context.scene.render.simplify_gpencil_antialiasing = self.data['render_props']['simplify']['simplify_gpencil_antialiasing']
        # Grease Pencil
        bpy.context.scene.grease_pencil_settings.antialias_threshold = self.data['render_props']['grease_pencil']['antialias_threshold']
        # Freestyle
        bpy.context.scene.render.use_freestyle = self.data['render_props']['freestyle']['use_freestyle']
        bpy.context.scene.render.line_thickness_mode = self.data['render_props']['freestyle']['line_thickness_mode']
        bpy.context.scene.render.line_thickness = self.data['render_props']['freestyle']['line_thickness']
        # Color Management
        bpy.context.scene.display_settings.display_device = self.data['render_props']['color_management']['display_device']
        bpy.context.scene.view_settings.view_transform = self.data['render_props']['color_management']['view_transform']
        bpy.context.scene.view_settings.look = self.data['render_props']['color_management']['look']
        bpy.context.scene.view_settings.exposure = self.data['render_props']['color_management']['exposure']
        bpy.context.scene.view_settings.gamma = self.data['render_props']['color_management']['gamma']
        bpy.context.scene.sequencer_colorspace_settings.name = self.data['render_props']['color_management']['name']
        bpy.context.scene.view_settings.use_curve_mapping = self.data['render_props']['color_management']['use_curve_mapping']

    def loadEeveeOutputProps(self, props):
        # Format
        bpy.context.scene.render.resolution_x = self.data['output_props']['format']['resolution_x']
        bpy.context.scene.render.resolution_y = self.data['output_props']['format']['resolution_y']
        bpy.context.scene.render.resolution_percentage = self.data['output_props']['format']['resolution_percentage']
        bpy.context.scene.render.pixel_aspect_x = self.data['output_props']['format']['pixel_aspect_x']
        bpy.context.scene.render.pixel_aspect_y = self.data['output_props']['format']['pixel_aspect_y']
        bpy.context.scene.render.use_border = self.data['output_props']['format']['use_border']
        bpy.context.scene.render.use_crop_to_border = self.data['output_props']['format']['use_crop_to_border']
        # Frame Range
        bpy.context.scene.frame_start = self.data['output_props']['frame_range']['frame_start']
        bpy.context.scene.frame_end = self.data['output_props']['frame_range']['frame_end']
        bpy.context.scene.frame_step = self.data['output_props']['frame_range']['frame_step']
        bpy.context.scene.render.frame_map_old = self.data['output_props']['frame_range']['frame_map_old']
        bpy.context.scene.render.frame_map_new = self.data['output_props']['frame_range']['frame_map_new']
        # Stereoscopy
        bpy.context.scene.render.use_multiview = self.data['output_props']['stereoscopy']['use_multiview']
        bpy.context.scene.render.views_format = self.data['output_props']['stereoscopy']['views_format']
        bpy.context.scene.render.views["left"].use = self.data['output_props']['stereoscopy']['left_use']
        bpy.context.scene.render.views["right"].use = self.data['output_props']['stereoscopy']['right_use']
        bpy.context.scene.render.views["left"].camera_suffix = self.data['output_props']['stereoscopy']['left_camera_suffix']
        bpy.context.scene.render.views["right"].camera_suffix = self.data['output_props']['stereoscopy']['right_camera_suffix']
        # Output

        bpy.context.scene.render.filepath = self.data['output_props']['output']['filepath']
        bpy.context.scene.render.use_file_extension = self.data['output_props']['output']['use_file_extension']
        bpy.context.scene.render.use_render_cache = self.data['output_props']['output']['use_render_cache']
        bpy.context.scene.render.image_settings.file_format = self.data['output_props']['output']['file_format']
        bpy.context.scene.render.image_settings.color_mode = self.data['output_props']['output']['color_mode']
        bpy.context.scene.render.use_placeholder = self.data['output_props']['output']['use_placeholder']
        bpy.context.scene.render.image_settings.views_format = self.data['output_props']['output']['views_format']
        # TODO
        # self.data['output_props']['output']['stereo_mode'] = bpy.data.scenes["Scene"].(null) = 'INTERLACE'
        bpy.context.scene.render.image_settings.color_management = self.data['output_props']['output']['color_management']
        # if(bpy.context.scene.render.image_settings.color_management == 'OVERRIDE'):
        #     # TODO This doesn't work yet.
        #     bpy.context.scene.colorspace_settings.name = self.data['output_props']['output']['name']

        # Metadata
        bpy.context.scene.render.metadata_input = self.data['output_props']['metadata']['metadata_input']
        bpy.context.scene.render.use_stamp_date = self.data['output_props']['metadata']['use_stamp_date']
        bpy.context.scene.render.use_stamp_time = self.data['output_props']['metadata']['use_stamp_time']
        bpy.context.scene.render.use_stamp_render_time = self.data['output_props']['metadata']['use_stamp_render_time']
        bpy.context.scene.render.use_stamp_frame = self.data['output_props']['metadata']['use_stamp_frame']
        bpy.context.scene.render.use_stamp_frame_range = self.data['output_props']['metadata']['use_stamp_frame_range']
        bpy.context.scene.render.use_stamp_memory = self.data['output_props']['metadata']['use_stamp_memory']
        bpy.context.scene.render.use_stamp_hostname = self.data['output_props']['metadata']['use_stamp_hostname']
        bpy.context.scene.render.use_stamp_camera = self.data['output_props']['metadata']['use_stamp_camera']
        bpy.context.scene.render.use_stamp_lens = self.data['output_props']['metadata']['use_stamp_lens']
        bpy.context.scene.render.use_stamp_scene = self.data['output_props']['metadata']['use_stamp_scene']
        bpy.context.scene.render.use_stamp_marker = self.data['output_props']['metadata']['use_stamp_marker']
        bpy.context.scene.render.use_stamp_filename = self.data['output_props']['metadata']['use_stamp_filename']
        bpy.context.scene.render.use_stamp_sequencer_strip = self.data['output_props']['metadata']['use_stamp_sequencer_strip']
        bpy.context.scene.render.use_stamp_note = self.data['output_props']['metadata']['use_stamp_note']
        bpy.context.scene.render.stamp_note_text = self.data['output_props']['metadata']['stamp_note_text']
        bpy.context.scene.render.use_stamp = self.data['output_props']['metadata']['use_stamp']
        if bpy.context.scene.render.use_stamp == True:
            bpy.context.scene.render.stamp_font_size = self.data['output_props']['metadata']['stamp_font_size']
            bpy.context.scene.render.stamp_foreground = self.stringToColorAlpha(self.data['output_props']['metadata']['stamp_foreground'])
            bpy.context.scene.render.stamp_background = self.stringToColorAlpha(self.data['output_props']['metadata']['stamp_background'])
            bpy.context.scene.render.use_stamp_labels = self.data['output_props']['metadata']['use_stamp_labels']
        # Post Processing
        bpy.context.scene.render.use_compositing = self.data['output_props']['post_processing']['use_compositing']
        bpy.context.scene.render.use_sequencer = self.data['output_props']['post_processing']['use_sequencer']
        bpy.context.scene.render.dither_intensity = self.data['output_props']['post_processing']['dither_intensity']

    def loadEeveeViewLayerProps(self, props):
        bpy.context.scene.view_layers["ViewLayer"].use = self.data['viewlayer_props']['view_layer']['use']
        bpy.context.scene.render.use_single_layer = self.data['viewlayer_props']['view_layer']['use_single_layer']

        # ======
        # Passes
        # ======
        bpy.context.scene.view_layers["ViewLayer"].use_pass_combined = self.data['viewlayer_props']['passes']['data']['use_pass_combined']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_z = self.data['viewlayer_props']['passes']['data']['use_pass_z']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_mist = self.data['viewlayer_props']['passes']['data']['use_pass_mist']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_normal = self.data['viewlayer_props']['passes']['data']['use_pass_normal']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_diffuse_direct = self.data['viewlayer_props']['passes']['light']['use_pass_diffuse_direct']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_diffuse_color = self.data['viewlayer_props']['passes']['light']['use_pass_diffuse_color']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_glossy_direct = self.data['viewlayer_props']['passes']['light']['use_pass_glossy_direct']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_glossy_color = self.data['viewlayer_props']['passes']['light']['use_pass_glossy_color']
        bpy.context.scene.view_layers["ViewLayer"].eevee.use_pass_volume_direct = self.data['viewlayer_props']['passes']['light']['volume']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_emit = self.data['viewlayer_props']['passes']['light']['use_pass_emit']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_environment = self.data['viewlayer_props']['passes']['light']['use_pass_environment']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_shadow = self.data['viewlayer_props']['passes']['light']['use_pass_shadow']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_ambient_occlusion = self.data['viewlayer_props']['passes']['light']['use_pass_ambient_occlusion']
        bpy.context.scene.view_layers["ViewLayer"].eevee.use_pass_bloom = self.data['viewlayer_props']['passes']['effects']['use_pass_bloom']
        # self.data['passes']['light']['use_shadow_catcher'] = bpy.data.scenes["Scene"].(null)
        bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_object = self.data['viewlayer_props']['passes']['cryptomatte']['use_pass_cryptomatte_object']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_material = self.data['viewlayer_props']['passes']['cryptomatte']['use_pass_cryptomatte_material']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_asset = self.data['viewlayer_props']['passes']['cryptomatte']['use_pass_cryptomatte_asset']
        bpy.context.scene.view_layers["ViewLayer"].pass_cryptomatte_depth = self.data['viewlayer_props']['passes']['cryptomatte']['pass_cryptomatte_depth']
        bpy.context.scene.view_layers["ViewLayer"].use_pass_cryptomatte_accurate = self.data['viewlayer_props']['passes']['cryptomatte']['use_pass_cryptomatte_accurate']
        bpy.context.scene.view_layers["ViewLayer"].use_freestyle = self.data['viewlayer_props']['passes']['freestyle']['use_freestyle']
        # TODO - The rest of the Freestyle section I don't understand

    def loadEeveeSceneProps(self, props):
        # I need to figure out how to serialize the camera. Value printed is:
        # <bpy_struct, Object("Camera") at 0x000002EE7C60B908>
        # settings['scene_props']['scene']['camera'] = bpy.context.scene.camera
        # print('scene_props.scene.camera = ')
        # print(bpy.context.scene.camera)
        # print('*****************************')
        # print('*****************************')
        # print('*****************************')
        # I suspect the following 2 lines will also fail 
        # settings['scene_props']['scene']['background_set'] = bpy.context.scene.background_set
        # settings['scene_props']['scene']['active_clip'] = bpy.context.scene.active_clip # Is this right?
        # Scene Properties - Units
        bpy.context.scene.unit_settings.system = self.data['scene_props']['units']['system']
        bpy.context.scene.unit_settings.scale_length = self.data['scene_props']['units']['scale_length']
        bpy.context.scene.unit_settings.use_separate = self.data['scene_props']['units']['use_separate']
        bpy.context.scene.unit_settings.system_rotation = self.data['scene_props']['units']['system_rotation']
        bpy.context.scene.unit_settings.length_unit = self.data['scene_props']['units']['length_unit']
        bpy.context.scene.unit_settings.mass_unit = self.data['scene_props']['units']['mass_unit']
        bpy.context.scene.unit_settings.time_unit  = self.data['scene_props']['units']['time_unit']
        bpy.context.scene.unit_settings.temperature_unit= self.data['scene_props']['units']['temperature_unit']
        # Scene Properties - Gravity
        bpy.context.scene.use_gravity = self.data['scene_props']['gravity']['use_gravity']
        bpy.context.scene.gravity[0] = self.data['scene_props']['gravity']['gravity_x']
        bpy.context.scene.gravity[1] = self.data['scene_props']['gravity']['gravity_y']
        bpy.context.scene.gravity[2] = self.data['scene_props']['gravity']['gravity_z']
        # Scene Properties - Keying SSets
        # settings['scene_props']['keying_sets'] = {} # TBD
        # Scene Properties - Audio
        bpy.context.scene.audio_volume = self.data['scene_props']['audio']['volume']
        bpy.context.scene.audio_distance_model = self.data['scene_props']['audio']['audio_distance_model']
        bpy.context.scene.audio_doppler_speed = self.data['scene_props']['audio']['audio_doppler_speed']
        bpy.context.scene.audio_doppler_factor = self.data['scene_props']['audio']['audio_doppler_factor']
        # Scene Properties - Rigid Body  World
        # settings['scene_props']['rigid_body_world'] = {} # TBD FUTURE
        # Scene Properties - Custom Properties
        # settings['scene_props']['custom_properties'] = {} # TBD FUTURE

    
    def loadEeveeWorldProps(self, props):
        # World Properties - Surface
        # TBD
        # settings['world_props']['surface']['surface'] = bpy.data.worlds["World"].node_tree.nodes["Translucent BSDF"].inputs[0].default_value
        # settings['world_props']['surface']['color'] = bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value
        # settings['world_props']['surface']['strength'] = bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value
        # World Properties - Volume
        # TBD - Its not clear to me how to get/set this data reliably.

        bpy.context.scene.world.mist_settings.start = self.data['world_props']['mist_pass']['start']
        bpy.context.scene.world.mist_settings.depth = self.data['world_props']['mist_pass']['depth']
        bpy.context.scene.world.mist_settings.falloff = self.data['world_props']['mist_pass']['falloff']
        bpy.context.scene.world.color = self.stringToColor(self.data['world_props']['viewport_display']['color'])
        # settings['world_props']['custom_properties'] = {} # TBD FUTURE

    def loadEeveeCollectionProps(self, props):
        # Collection Properties
        bpy.data.collections["Collection"].hide_select = self.data['collection_props']['restrictions']['hide_select']
        bpy.data.collections["Collection"].hide_render = self.data['collection_props']['restrictions']['hide_render']
        # settings['collection_props']['restrictions']['holdout'] = bpy.data.scenes["Scene"].(null)
        # settings['collection_props']['restrictions']['indirect_only'] = bpy.data.scenes["Scene"].(null)
        bpy.data.collections["Collection"].instance_offset[0] = self.data['collection_props']['instancing']['instance_offset_x']
        bpy.data.collections["Collection"].instance_offset[1] = self.data['collection_props']['instancing']['instance_offset_y']
        bpy.data.collections["Collection"].instance_offset[2] = self.data['collection_props']['instancing']['instance_offset_z']
        bpy.data.collections["Collection"].lineart_usage = self.data['collection_props']['line_art']['lineart_usage']
        bpy.data.collections["Collection"].lineart_use_intersection_mask = self.data['collection_props']['line_art']['lineart_use_intersection_mask']
        # if the use_lineart_intersection_masks is checked, then these are valid
        bpy.data.collections["Collection"].lineart_intersection_mask[0] = self.data['collection_props']['line_art']['lineart_intersection_mask_0']
        bpy.data.collections["Collection"].lineart_intersection_mask[1] = self.data['collection_props']['line_art']['lineart_intersection_mask_1']
        bpy.data.collections["Collection"].lineart_intersection_mask[2] = self.data['collection_props']['line_art']['lineart_intersection_mask_2']
        bpy.data.collections["Collection"].lineart_intersection_mask[3] = self.data['collection_props']['line_art']['lineart_intersection_mask_3']
        bpy.data.collections["Collection"].lineart_intersection_mask[4] = self.data['collection_props']['line_art']['lineart_intersection_mask_4']
        bpy.data.collections["Collection"].lineart_intersection_mask[5] = self.data['collection_props']['line_art']['lineart_intersection_mask_5']
        bpy.data.collections["Collection"].lineart_intersection_mask[6]  = self.data['collection_props']['line_art']['lineart_intersection_mask_6']
        bpy.data.collections["Collection"].lineart_intersection_mask[7] = self.data['collection_props']['line_art']['lineart_intersection_mask_7']
        bpy.data.collections["Collection"].use_lineart_intersection_priority = self.data['collection_props']['line_art']['use_lineart_intersection_priority']
        bpy.data.collections["Collection"].lineart_intersection_priority = self.data['collection_props']['line_art']['lineart_intersection_priority']

        # settings['collection_props']['custom_properties'] = {}  # TODO

    # Convert a color string from the JSON file "(1.0, 1.0, 1.0)" into a Blender color value array
    def stringToColor(self, colorString):
        # print("colorString = " + colorString)
        temp = colorString.strip("()")
        # print("temp  = " + temp)
        strArray = temp.split(',')
        # print("strArray =")
        # print(strArray)

        color = (0,0,0)
        color = (float(strArray[0]), float(strArray[1]), float(strArray[2]))
        # print("final color")
        # print(color)
        return color

    # Convert a colorAlpha string from the JSON file "(1.0, 1.0, 1.0, 1.0)" into a Blender bpy_float[4] array
    def stringToColorAlpha(self, colorAlphaString):
        # print("colorAlphaString = " + colorAlphaString)
        temp = colorAlphaString.strip("()")
        # print("temp  = " + temp)
        strArray = temp.split(',')
        # print("strArray =")
        # print(strArray)

        colorAlpha = array('f', [0.0,  0.0, 0.0, 0.0])
        colorAlpha[0] = float(strArray[0])
        colorAlpha[1] = float(strArray[1])
        colorAlpha[2] = float(strArray[2])
        colorAlpha[3] = float(strArray[3])
        # print("final color w/ alpha")
        # print(colorAlpha)
        return colorAlpha
