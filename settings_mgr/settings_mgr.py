import bpy
import json
import os


class SaveButtonOperator(bpy.types.Operator):
    """Save the file"""
    bl_idname = "setmgr.save"
    bl_label = "Settings Manager"
    # Our settings data
    data = {}

        
    def execute(self, context):
        global data

        fn = bpy.path.abspath("//" + context.scene.my_tool.filename + '.json')
        print('fn = ' + fn)
        ospath = os.path.basename(fn)
        print('os.path.basename = ' + ospath)
        bpypath = bpy.path.basename(fn)
        print('bpy.path.basename = ' + bpypath)
        fn = bpy.path.ensure_ext(fn, '.json', case_sensitive=False)
        print('adj filename = ' + fn)

        self.readSettings(context, self.data)
        print('About to call saveFile: ' + fn)
        self.saveFile(context, fn, self.data)
        return {'FINISHED'}
    
    def saveFile(self, context, filename, data):
        print('Saving file: ' + filename)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=True, ensure_ascii=True, indent=4)
        print('   Done!')
        msg = 'Saved as: ' + filename
        context.scene.my_tool.message = msg
        print(msg)
        # bpy.ops.message.messagebox('INVOKE_DEFAULT', message = msg)
        bpy.ops.message.messagebox('INVOKE_DEFAULT', message = msg)
        return {'FINISHED'}

    def readSettings(self, context, settings):
        print('Reading the settings...')

        # Are we using cycles or EEVEE?
        settings['render_props'] = {}
        settings['render_props']['engine'] = context.scene.render.engine
        if settings['render_props']['engine'] == 'CYCLES':
            settings['render_props']['feature_set'] = bpy.context.scene.cycles.feature_set
            settings['render_props']['device'] = bpy.context.scene.cycles.device
            # Sampling
            settings['render_props']['sampling'] = {}
            settings['render_props']['sampling']['viewport'] = {}
            settings['render_props']['sampling']['viewport']['use_preview_adaptive_sampling'] = bpy.context.scene.cycles.use_preview_adaptive_sampling
            settings['render_props']['sampling']['viewport']['preview_adaptive_threshold'] = bpy.context.scene.cycles.preview_adaptive_threshold
            settings['render_props']['sampling']['viewport']['preview_samples'] = bpy.context.scene.cycles.preview_samples
            settings['render_props']['sampling']['viewport']['preview_adaptive_min_samples'] = bpy.context.scene.cycles.preview_adaptive_min_samples
            settings['render_props']['sampling']['viewport']['use_preview_denoising'] = bpy.context.scene.cycles.use_preview_denoising
            settings['render_props']['sampling']['viewport']['preview_denoiser'] = bpy.context.scene.cycles.preview_denoiser
            settings['render_props']['sampling']['viewport']['preview_denoising_input_passes'] = bpy.context.scene.cycles.preview_denoising_input_passes
            settings['render_props']['sampling']['viewport']['preview_denoising_start_sample'] = bpy.context.scene.cycles.preview_denoising_start_sample
            settings['render_props']['sampling']['render'] = {}
            settings['render_props']['sampling']['render']['use_adaptive_sampling'] = bpy.context.scene.cycles.use_adaptive_sampling
            settings['render_props']['sampling']['render']['adaptive_threshold'] = bpy.context.scene.cycles.adaptive_threshold
            settings['render_props']['sampling']['render']['samples'] = bpy.context.scene.cycles.samples
            settings['render_props']['sampling']['render']['adaptive_min_samples'] = bpy.context.scene.cycles.adaptive_min_samples
            settings['render_props']['sampling']['render']['time_limit'] = bpy.context.scene.cycles.time_limit
            settings['render_props']['sampling']['render']['use_denoising'] = bpy.context.scene.cycles.use_denoising
            settings['render_props']['sampling']['render']['denoiser'] = bpy.context.scene.cycles.denoiser
            settings['render_props']['sampling']['render']['denoising_prefilter'] = bpy.context.scene.cycles.denoising_prefilter
            settings['render_props']['sampling']['advanced'] = {}
            settings['render_props']['sampling']['advanced']['seed'] = bpy.context.scene.cycles.seed
            settings['render_props']['sampling']['advanced']['sampling_pattern'] = bpy.context.scene.cycles.sampling_pattern
            settings['render_props']['sampling']['advanced']['sample_offset'] = bpy.context.scene.cycles.sample_offset
            settings['render_props']['sampling']['advanced']['auto_scrambling_distance'] = bpy.context.scene.cycles.auto_scrambling_distance
            settings['render_props']['sampling']['advanced']['preview_scrambling_distance'] = bpy.context.scene.cycles.preview_scrambling_distance
            settings['render_props']['sampling']['advanced']['scrambling_distance'] = bpy.context.scene.cycles.scrambling_distance
            settings['render_props']['sampling']['advanced']['min_light_bounces'] = bpy.context.scene.cycles.min_light_bounces
            settings['render_props']['sampling']['advanced']['min_transparent_bounces'] = bpy.context.scene.cycles.min_transparent_bounces
            settings['render_props']['sampling']['advanced']['light_sampling_threshold'] = bpy.context.scene.cycles.light_sampling_threshold
            # Light Paths
            settings['render_props']['light_paths'] = {}
            settings['render_props']['light_paths']['max_bounces'] = {}
            settings['render_props']['light_paths']['max_bounces']['total'] = bpy.context.scene.cycles.max_bounces
            settings['render_props']['light_paths']['max_bounces']['diffuse_bounces'] = bpy.context.scene.cycles.diffuse_bounces
            settings['render_props']['light_paths']['max_bounces']['glossy_bounces'] = bpy.context.scene.cycles.glossy_bounces
            settings['render_props']['light_paths']['max_bounces']['transmission_bounces'] = bpy.context.scene.cycles.transmission_bounces
            settings['render_props']['light_paths']['max_bounces']['volume_bounces'] = bpy.context.scene.cycles.volume_bounces
            settings['render_props']['light_paths']['max_bounces']['transparent_max_bounces'] = bpy.context.scene.cycles.transparent_max_bounces
            settings['render_props']['light_paths']['clamping'] = {}
            settings['render_props']['light_paths']['clamping']['sample_clamp_direct'] = bpy.context.scene.cycles.sample_clamp_direct
            settings['render_props']['light_paths']['clamping']['sample_clamp_indirect'] = bpy.context.scene.cycles.sample_clamp_indirect
            settings['render_props']['light_paths']['caustics'] = {}
            settings['render_props']['light_paths']['caustics']['blur_glossy'] = bpy.context.scene.cycles.blur_glossy
            settings['render_props']['light_paths']['caustics']['caustics_reflective'] = bpy.context.scene.cycles.caustics_reflective
            settings['render_props']['light_paths']['caustics']['caustics_refractive'] = bpy.context.scene.cycles.caustics_refractive
            settings['render_props']['light_paths']['fast_gi'] = {}
            settings['render_props']['light_paths']['fast_gi']['use_fast_gi'] = bpy.context.scene.cycles.use_fast_gi
            settings['render_props']['light_paths']['fast_gi']['fast_gi_method'] = bpy.context.scene.cycles.fast_gi_method
            settings['render_props']['light_paths']['fast_gi']['ao_factor'] = bpy.context.scene.world.light_settings.ao_factor
            settings['render_props']['light_paths']['fast_gi']['distance'] = bpy.context.scene.world.light_settings.distance
            # Volumes
            settings['render_props']['volumes'] = {}
            settings['render_props']['volumes']['volume_step_rate'] = bpy.context.scene.cycles.volume_step_rate
            settings['render_props']['volumes']['volume_preview_step_rate'] = bpy.context.scene.cycles.volume_preview_step_rate
            settings['render_props']['volumes']['volume_max_steps'] = bpy.context.scene.cycles.volume_max_steps
            #Curves
            settings['render_props']['curves'] = {}
            settings['render_props']['curves']['shape'] = bpy.context.scene.cycles_curves.shape
            settings['render_props']['curves']['subdivisions'] = bpy.context.scene.cycles_curves.subdivisions
            settings['render_props']['curves']['viewport_display'] = {}
            settings['render_props']['curves']['viewport_display']['hair_type'] = bpy.context.scene.render.hair_type
            settings['render_props']['curves']['viewport_display']['hair_subdiv'] = bpy.context.scene.render.hair_subdiv
            # Simplify
            settings['render_props']['simplify'] = {}
            settings['render_props']['simplify']['use_simplify'] = bpy.context.scene.render.use_simplify
            settings['render_props']['simplify']['viewport'] = {}
            settings['render_props']['simplify']['viewport']['simplify_child_particles'] = bpy.context.scene.render.simplify_child_particles
            settings['render_props']['simplify']['viewport']['texture_limit'] = bpy.context.scene.cycles.texture_limit
            settings['render_props']['simplify']['viewport']['simplify_volumes'] = bpy.context.scene.render.simplify_volumes
            settings['render_props']['simplify']['render'] = {}
            settings['render_props']['simplify']['render']['simplify_subdivision_render'] = bpy.context.scene.render.simplify_subdivision_render
            settings['render_props']['simplify']['render']['simplify_child_particles_render'] = bpy.context.scene.render.simplify_child_particles_render
            settings['render_props']['simplify']['render']['texture_limit_render'] = bpy.context.scene.cycles.texture_limit_render
            settings['render_props']['simplify']['culling'] = {}
            settings['render_props']['simplify']['culling']['use_camera_cull'] = bpy.context.scene.cycles.use_camera_cull
            settings['render_props']['simplify']['culling']['camera_cull_margin'] = bpy.context.scene.cycles.camera_cull_margin
            settings['render_props']['simplify']['culling']['use_distance_cull'] = bpy.context.scene.cycles.use_distance_cull
            settings['render_props']['simplify']['culling']['distance_cull_margin'] = bpy.context.scene.cycles.distance_cull_margin
            settings['render_props']['simplify']['grease_pencil'] = {}
            settings['render_props']['simplify']['grease_pencil']['simplify_gpencil'] = bpy.context.scene.render.simplify_gpencil
            settings['render_props']['simplify']['grease_pencil']['simplify_gpencil_onplay'] = bpy.context.scene.render.simplify_gpencil_onplay
            settings['render_props']['simplify']['grease_pencil']['simplify_gpencil_view_fill'] = bpy.context.scene.render.simplify_gpencil_view_fill
            settings['render_props']['simplify']['grease_pencil']['simplify_gpencil_modifier'] = bpy.context.scene.render.simplify_gpencil_modifier
            settings['render_props']['simplify']['grease_pencil']['simplify_gpencil_shader_fx'] = bpy.context.scene.render.simplify_gpencil_shader_fx
            settings['render_props']['simplify']['grease_pencil']['simplify_gpencil_tint'] = bpy.context.scene.render.simplify_gpencil_tint
            settings['render_props']['simplify']['grease_pencil']['simplify_gpencil_antialiasing'] = bpy.context.scene.render.simplify_gpencil_antialiasing
            # Motion Blur
            settings['render_props']['motion_blur'] = {}
            settings['render_props']['motion_blur']['use_motion_blur'] = bpy.context.scene.render.use_motion_blur = True
            settings['render_props']['motion_blur']['motion_blur_position'] = bpy.context.scene.cycles.motion_blur_position = 'CENTER'
            settings['render_props']['motion_blur']['motion_blur_shutter'] = bpy.context.scene.render.motion_blur_shutter = 0.6
            settings['render_props']['motion_blur']['rolling_shutter_type'] = bpy.context.scene.cycles.rolling_shutter_type = 'TOP'
            settings['render_props']['motion_blur']['rolling_shutter_duration'] = bpy.context.scene.cycles.rolling_shutter_duration = 0.2
            settings['render_props']['motion_blur']['shutter_curve'] = {} # not available ATM

            # Film
            settings['render_props']['film'] = {}
            settings['render_props']['film']['film_exposure'] = bpy.context.scene.cycles.film_exposure
            settings['render_props']['film']['pixel_filter'] = {}
            settings['render_props']['film']['pixel_filter']['pixel_filter_type'] = bpy.context.scene.cycles.pixel_filter_type
            # does not apply to the Box type
            settings['render_props']['film']['pixel_filter']['filter_width'] = bpy.context.scene.cycles.filter_width
            settings['render_props']['film']['transparent'] = {}
            settings['render_props']['film']['transparent']['film_transparent'] = bpy.context.scene.render.film_transparent
            settings['render_props']['film']['transparent']['film_transparent_glass'] = bpy.context.scene.cycles.film_transparent_glass
            settings['render_props']['film']['transparent']['film_transparent_roughness'] = bpy.context.scene.cycles.film_transparent_roughness

            # Performance
            settings['render_props']['performance'] = {}
            settings['render_props']['performance']['threads'] = {}
            settings['render_props']['performance']['threads']['threads_mode'] = bpy.context.scene.render.threads_mode
            settings['render_props']['performance']['threads']['threads'] = bpy.context.scene.render.threads
            settings['render_props']['performance']['memory'] = {}
            settings['render_props']['performance']['memory']['use_auto_tile'] = bpy.context.scene.cycles.use_auto_tile
            settings['render_props']['performance']['memory']['tile_size'] = bpy.context.scene.cycles.tile_size
            settings['render_props']['performance']['final_render'] = {}
            settings['render_props']['performance']['final_render']['use_persistent_data'] = bpy.context.scene.render.use_persistent_data
            settings['render_props']['performance']['viewport'] = {}
            settings['render_props']['performance']['viewport']['preview_pixel_size'] = bpy.context.scene.render.preview_pixel_size

            # Bake
            settings['render_props']['bake'] = {}
            settings['render_props']['bake']['use_bake_multires'] = bpy.context.scene.render.use_bake_multires
            settings['render_props']['bake']['bake_type'] = bpy.context.scene.render.bake_type
            settings['render_props']['bake']['output'] = {}
            settings['render_props']['bake']['output']['use_bake_clear'] = bpy.context.scene.render.use_bake_clear
            settings['render_props']['bake']['output']['use_bake_lores_mesh'] = bpy.context.scene.render.use_bake_lores_mesh
            settings['render_props']['bake']['margin'] = {}
            settings['render_props']['bake']['margin']['bake_margin_type'] = bpy.context.scene.render.bake_margin_type
            settings['render_props']['bake']['margin']['bake_margin'] = bpy.context.scene.render.bake_margin

            # Grease Pencil
            settings['render_props']['grease_pencil'] = {}
            settings['render_props']['grease_pencil']['antialias_threshold'] = bpy.context.scene.grease_pencil_settings.antialias_threshold
            # Freestyle
            settings['render_props']['freestyle'] = {}
            settings['render_props']['freestyle']['use_freestyle'] = bpy.context.scene.render.use_freestyle
            settings['render_props']['freestyle']['line_thickness_mode'] = bpy.context.scene.render.line_thickness_mode
            settings['render_props']['freestyle']['line_thickness'] = bpy.context.scene.render.line_thickness
            # Color Management
            settings['render_props']['color_management'] = {}
            settings['render_props']['color_management']['display_device'] = bpy.context.scene.display_settings.display_device
            settings['render_props']['color_management']['view_transform'] = bpy.context.scene.view_settings.view_transform
            settings['render_props']['color_management']['look'] = bpy.context.scene.view_settings.look
            settings['render_props']['color_management']['exposure'] = bpy.context.scene.view_settings.exposure
            settings['render_props']['color_management']['gamma'] = bpy.context.scene.view_settings.gamma
            settings['render_props']['color_management']['name'] = bpy.context.scene.sequencer_colorspace_settings.name
            settings['render_props']['color_management']['curves'] = {}
            settings['render_props']['color_management']['curves']['use_curve_mapping'] = bpy.context.scene.view_settings.use_curve_mapping
            # curve data no working yet. Same code for black and white levels
            # settings['render_props']['color_management']['curves']['black_level'] = {}
            # settings['render_props']['color_management']['curves']['white_level'] = {}
            # settings['render_props']['color_management']['curves']['black_level']['red'] = bpy.data.scenes["Scene"].(null)[0]
            # settings['render_props']['color_management']['curves']['black_level']['green'] = bpy.data.scenes["Scene"].(null)[1]
            # settings['render_props']['color_management']['curves']['black_level']['blue'] = bpy.data.scenes["Scene"].(null)[2]

            # Workspace
            settings['workspace'] = {}
            settings['workspace']['options'] = {}
            settings['workspace']['options']['transform'] = {}
            settings['workspace']['options']['transform']['context'] = bpy.context.space_data.context
            settings['workspace']['options']['transform']['use_transform_data_origin'] = bpy.context.scene.tool_settings.use_transform_data_origin
            settings['workspace']['options']['transform']['use_transform_pivot_point_align'] = bpy.context.scene.tool_settings.use_transform_pivot_point_align
            settings['workspace']['workspace'] = {}
            settings['workspace']['workspace']['use_pin_scene'] = bpy.data.workspaces["Scripting"].use_pin_scene
            settings['workspace']['workspace']['object_mode'] = bpy.data.workspaces["Scripting"].object_mode
            settings['workspace']['workspace']['filter_addons'] = {}
            settings['workspace']['workspace']['filter_addons']['use_filter_by_owner'] = bpy.data.workspaces["Scripting"].use_filter_by_owner

            # Output Properties
            settings['output_props'] = {}
            settings['output_props']['format'] = {}
            settings['output_props']['format']['resolution_x'] = bpy.context.scene.render.resolution_x
            settings['output_props']['format']['resolution_y'] = bpy.context.scene.render.resolution_y
            settings['output_props']['format']['resolution_percentage'] = bpy.context.scene.render.resolution_percentage
            settings['output_props']['format']['pixel_aspect_x'] = bpy.context.scene.render.pixel_aspect_x
            settings['output_props']['format']['pixel_aspect_y'] = bpy.context.scene.render.pixel_aspect_y
            # frame rate does not seem to be readable
            settings['output_props']['format']['render_region'] = bpy.context.scene.render.use_border
            settings['output_props']['format']['crop_to_render_region'] = bpy.context.scene.render.use_crop_to_border

            # Frame Range
            settings['output_props']['frame_range'] = {}
            settings['output_props']['frame_range']['frame_start'] = bpy.context.scene.frame_start
            settings['output_props']['frame_range']['frame_end'] = bpy.context.scene.frame_end
            settings['output_props']['frame_range']['frame_step'] = bpy.context.scene.frame_step
            settings['output_props']['frame_range']['frame_map_old'] = bpy.context.scene.render.frame_map_old
            settings['output_props']['frame_range']['frame_map_new'] = bpy.context.scene.render.frame_map_new

            # Stereoscopy
            settings['output_props']['stereoscopy'] = {}
            settings['output_props']['stereoscopy']['use_multiview'] = bpy.context.scene.render.use_multiview
            settings['output_props']['stereoscopy']['views_format'] = bpy.context.scene.render.views_format
            settings['output_props']['stereoscopy']['use_multiview'] = bpy.context.scene.render.views["left"].use
            settings['output_props']['stereoscopy']['use_multiview'] = bpy.context.scene.render.views["right"].use
            settings['output_props']['stereoscopy']['use_multiview'] = bpy.context.scene.render.views["left"].camera_suffix

            # output
            settings['output_props']['output'] = {}
            settings['output_props']['output']['filepath'] = bpy.context.scene.render.filepath
            settings['output_props']['output']['use_file_extension'] = bpy.context.scene.render.use_file_extension
            settings['output_props']['output']['use_render_cache'] = bpy.context.scene.render.use_render_cache
            settings['output_props']['output']['file_format'] = bpy.context.scene.render.image_settings.file_format
            settings['output_props']['output']['color_mode'] = bpy.context.scene.render.image_settings.color_mode
            settings['output_props']['output']['quality'] = bpy.context.scene.render.image_settings.quality
            settings['output_props']['output']['color_depth'] = bpy.context.scene.render.image_settings.color_depth
            settings['output_props']['output']['compression'] = bpy.context.scene.render.image_settings.compression
            settings['output_props']['output']['image_settings'] = {}
            settings['output_props']['output']['image_settings']['codec'] = bpy.context.scene.render.image_settings.jpeg2k_codec
            settings['output_props']['output']['image_settings']['use_jpeg2k_cinema_preset'] = bpy.context.scene.render.image_settings.use_jpeg2k_cinema_preset
            settings['output_props']['output']['image_settings']['use_jpeg2k_cinema_48'] = bpy.context.scene.render.image_settings.use_jpeg2k_cinema_48
            settings['output_props']['output']['image_settings']['use_jpeg2k_ycc'] = bpy.context.scene.render.image_settings.use_jpeg2k_ycc
            settings['output_props']['output']['image_sequence'] = {}
            settings['output_props']['output']['image_sequence']['overwrite'] = bpy.context.scene.render.use_overwrite
            settings['output_props']['output']['image_sequence']['use_placeholder'] = bpy.context.scene.render.use_placeholder

            settings['output_props']['output']['views'] = {}
            settings['output_props']['output']['views']['views_format'] = bpy.context.scene.render.image_settings.views_format
            settings['output_props']['output']['views']['quality'] = bpy.context.scene.render.image_settings.quality
            # settings['output_props']['output']['views']['stereo_mode'] = bpy.data.scenes["Scene"].(null)
            # settings['output_props']['output']['views']['interlace_type'] = bpy.data.scenes["Scene"].(null)'
            # settings['output_props']['output']['views']['swap_left_right'] = bpy.data.scenes["Scene"].(null)
            settings['output_props']['output']['color_management'] = {}
            settings['output_props']['output']['color_management']['type'] = bpy.context.scene.render.image_settings.color_management
            settings['output_props']['output']['color_management']['display_device'] = bpy.context.scene.display_settings.display_device
            settings['output_props']['output']['color_management']['view_transform'] = bpy.context.scene.view_settings.view_transform
            settings['output_props']['output']['color_management']['look'] = bpy.context.scene.view_settings.look
            settings['output_props']['output']['color_management']['exposure'] = bpy.context.scene.view_settings.exposure
            settings['output_props']['output']['color_management']['gamma'] = bpy.context.scene.view_settings.gamma
            settings['output_props']['output']['color_management']['use_curve_mapping'] = bpy.context.scene.view_settings.use_curve_mapping
            # curve info is not currently readable.
            # Metadata
            settings['output_props']['metadata'] = {}
            settings['output_props']['metadata']['metadata_input'] = bpy.context.scene.render.metadata_input
            settings['output_props']['metadata']['use_stamp_date'] = bpy.context.scene.render.use_stamp_date
            settings['output_props']['metadata']['use_stamp_time'] = bpy.context.scene.render.use_stamp_time
            settings['output_props']['metadata']['use_stamp_render_time'] = bpy.context.scene.render.use_stamp_render_time
            settings['output_props']['metadata']['use_stamp_frame'] = bpy.context.scene.render.use_stamp_frame
            settings['output_props']['metadata']['use_stamp_frame_range'] = bpy.context.scene.render.use_stamp_frame_range
            settings['output_props']['metadata']['use_stamp_memory'] = bpy.context.scene.render.use_stamp_memory
            settings['output_props']['metadata']['use_stamp_hostname'] = bpy.context.scene.render.use_stamp_hostname
            settings['output_props']['metadata']['use_stamp_camera'] = bpy.context.scene.render.use_stamp_camera
            settings['output_props']['metadata']['use_stamp_lens'] = bpy.context.scene.render.use_stamp_lens
            settings['output_props']['metadata']['use_stamp_scene'] = bpy.context.scene.render.use_stamp_scene
            settings['output_props']['metadata']['use_stamp_marker'] = bpy.context.scene.render.use_stamp_marker
            settings['output_props']['metadata']['use_stamp_filename'] = bpy.context.scene.render.use_stamp_filename
            settings['output_props']['metadata']['use_stamp_sequencer_strip'] = bpy.context.scene.render.use_stamp_sequencer_strip
            settings['output_props']['metadata']['use_stamp_note'] = bpy.context.scene.render.use_stamp_note
            settings['output_props']['metadata']['stamp_note_text'] = bpy.context.scene.render.stamp_note_text
            settings['output_props']['metadata']['use_stamp'] = bpy.context.scene.render.use_stamp
            settings['output_props']['metadata']['stamp_font_size'] = bpy.context.scene.render.stamp_font_size
            settings['output_props']['metadata']['stamp_foreground'] = bpy.context.scene.render.stamp_foreground
            settings['output_props']['metadata']['stamp_background'] = bpy.context.scene.render.stamp_background
            settings['output_props']['metadata']['use_stamp_labels'] = bpy.context.scene.render.use_stamp_labels

            # View Layer Properties
            settings['viewlayer_props'] = {}
            settings['viewlayer_props']['use'] = bpy.context.scene.view_layers["ViewLayer"].use
            settings['viewlayer_props']['use_single_layer'] = bpy.context.scene.render.use_single_layer

            # Custom Properties - TBD - FUTURE
            settings['viewlayer_props'] = {}
            settings['viewlayer_props']['custom_props'] = {}

            # Scene Properties
            settings['scene_props'] = {}
            settings['scene_props']['scene'] = {}
            settings['scene_props']['scene']['camera'] = bpy.context.scene.camera
            settings['scene_props']['scene']['background_set'] = bpy.context.scene.background_set
            settings['scene_props']['scene']['active_clip'] = bpy.context.scene.active_clip # Is this right?
            settings['scene_props']['units'] = {}
            settings['scene_props']['units']['system'] = bpy.context.scene.unit_settings.system
            settings['scene_props']['units']['scale_length'] = bpy.context.scene.unit_settings.scale_length
            settings['scene_props']['units']['use_separate'] = bpy.context.scene.unit_settings.use_separate
            settings['scene_props']['units']['system_rotation'] = bpy.context.scene.unit_settings.system_rotation
            settings['scene_props']['units']['length_unit'] = bpy.context.scene.unit_settings.length_unit
            settings['scene_props']['units']['mass_unit'] = bpy.context.scene.unit_settings.mass_unit
            settings['scene_props']['units']['time_unit'] = bpy.context.scene.unit_settings.time_unit
            settings['scene_props']['units']['temperature_unit'] = bpy.context.scene.unit_settings.temperature_unit
            settings['scene_props']['gravity'] = {}
            settings['scene_props']['gravity']['use_gravity'] = bpy.context.scene.use_gravity
            settings['scene_props']['gravity']['gravity_x'] = bpy.context.scene.gravity[0]
            settings['scene_props']['gravity']['gravity_y'] = bpy.context.scene.gravity[1]
            settings['scene_props']['gravity']['gravity_z'] = bpy.context.scene.gravity[2]
            settings['scene_props']['keying_sets'] = {} # TBD
            settings['scene_props']['audio'] = {}
            settings['scene_props']['audio']['volume'] = bpy.context.scene.audio_volume
            settings['scene_props']['audio']['audio_distance_model'] = bpy.context.scene.audio_distance_model
            settings['scene_props']['audio']['audio_doppler_speed'] = bpy.context.scene.audio_doppler_speed
            settings['scene_props']['audio']['audio_doppler_factor'] = bpy.context.scene.audio_doppler_factor
            settings['scene_props']['rigid_body_world'] = {} # TBD FUTURE
            settings['scene_props']['custom_properties'] = {} # TBD FUTURE
            # World Properties
            settings['world_props'] = {}
            settings['world_props']['viewport_display'] = {}
            settings['world_props']['viewport_display']['color'] = bpy.context.scene.world.color
            settings['world_props']['custom_properties'] = {} # TBD FUTURE

            # Collection Properties
            settings['collection_props'] = {}
            settings['collection_props']['restrictions'] = {}
            settings['collection_props']['restrictions']['hide_select'] = bpy.data.collections["Collection"].hide_select = True
            settings['collection_props']['restrictions']['hide_render'] = bpy.data.collections["Collection"].hide_render = True
            # settings['collection_props']['restrictions']['holdout'] = bpy.data.scenes["Scene"].(null)
            # settings['collection_props']['restrictions']['indirect_only'] = bpy.data.scenes["Scene"].(null)
            settings['collection_props']['instancing'] = {}
            settings['collection_props']['instancing']['instance_offset_x'] = bpy.data.collections["Collection"].instance_offset[0]
            settings['collection_props']['instancing']['instance_offset_y'] = bpy.data.collections["Collection"].instance_offset[1]
            settings['collection_props']['instancing']['instance_offset_z'] = bpy.data.collections["Collection"].instance_offset[2]
            settings['collection_props']['line_art'] = {}
            settings['collection_props']['line_art']['lineart_usage'] = bpy.data.collections["Collection"].lineart_usage
            settings['collection_props']['line_art']['lineart_use_intersection_mask'] = bpy.data.collections["Collection"].lineart_use_intersection_mask
            # if the use_lineart_intersection_masks is checked, then these are valid
            settings['collection_props']['line_art']['lineart_intersection_mask_0'] = bpy.data.collections["Collection"].lineart_intersection_mask[0]
            settings['collection_props']['line_art']['lineart_intersection_mask_1'] = bpy.data.collections["Collection"].lineart_intersection_mask[1]
            settings['collection_props']['line_art']['lineart_intersection_mask_2'] = bpy.data.collections["Collection"].lineart_intersection_mask[2]
            settings['collection_props']['line_art']['lineart_intersection_mask_3'] = bpy.data.collections["Collection"].lineart_intersection_mask[3]
            settings['collection_props']['line_art']['lineart_intersection_mask_4'] = bpy.data.collections["Collection"].lineart_intersection_mask[4]
            settings['collection_props']['line_art']['lineart_intersection_mask_5'] = bpy.data.collections["Collection"].lineart_intersection_mask[5]
            settings['collection_props']['line_art']['lineart_intersection_mask_6'] = bpy.data.collections["Collection"].lineart_intersection_mask[6]
            settings['collection_props']['line_art']['lineart_intersection_mask_7'] = bpy.data.collections["Collection"].lineart_intersection_mask[7]
            settings['collection_props']['line_art']['use_lineart_intersection_priority'] = bpy.data.collections["Collection"].use_lineart_intersection_priority
            settings['collection_props']['line_art']['lineart_intersection_priority'] = bpy.data.collections["Collection"].lineart_intersection_priority

            # Object Properties - Future
            settings['object_props'] = {}
            settings['object_props']['modifiers'] = {}
            # Particle Properties - Future
            settings['object_props']['particle_props'] = {}
            # Physics Properties - Future
            settings['object_props']['physics_props'] = {}
            # Object Constraint Properties - Future
            settings['object_props']['object_constraint_props'] = {}
            # Object Data Properties - Future
            settings['object_props']['object_data_props'] = {}
            # Meterial Properties - Future
            settings['object_props']['material_props'] = {}
            # Texture Properties - Future
            settings['texture_props'] = {}
        else:
            # EEVEE settings
            # Sampling
            settings['render_props']['sampling'] = {}
            settings['render_props']['sampling']['render_samples'] = bpy.context.scene.eevee.taa_render_samples
            settings['render_props']['sampling']['viewport_samples'] = bpy.context.scene.eevee.taa_samples
            settings['render_props']['sampling']['viewport_denoising'] = bpy.context.scene.eevee.use_taa_reprojection
            settings['render_props']['sampling']['ambient_occlusion'] = {}
            settings['render_props']['sampling']['ambient_occlusion']['use_gtao'] = bpy.context.scene.eevee.use_gtao
            settings['render_props']['sampling']['ambient_occlusion']['gtao_distance'] = bpy.context.scene.eevee.gtao_distance
            settings['render_props']['sampling']['ambient_occlusion']['gtao_factor'] = bpy.context.scene.eevee.gtao_factor
            settings['render_props']['sampling']['ambient_occlusion']['gtao_quality'] = bpy.context.scene.eevee.gtao_quality
            settings['render_props']['sampling']['ambient_occlusion']['use_gtao_bent_normals'] = bpy.context.scene.eevee.use_gtao_bent_normals
            settings['render_props']['sampling']['ambient_occlusion']['use_gtao_bounce'] = bpy.context.scene.eevee.use_gtao_bounce

            settings['render_props']['sampling']['bloom']['use_bloom'] = bpy.context.scene.eevee.use_bloom
            settings['render_props']['sampling']['bloom']['bloom_threshold'] = bpy.context.scene.eevee.bloom_threshold
            settings['render_props']['sampling']['bloom']['bloom_knee'] = bpy.context.scene.eevee.bloom_knee
            settings['render_props']['sampling']['bloom']['bloom_radius'] = bpy.context.scene.eevee.bloom_radius
            settings['render_props']['sampling']['bloom']['bloom_color'] = bpy.context.scene.eevee.bloom_color
            settings['render_props']['sampling']['bloom']['bloom_intensity'] = bpy.context.scene.eevee.bloom_intensity
            settings['render_props']['sampling']['bloom']['bloom_clamp'] = bpy.context.scene.eevee.bloom_clamp




        # print(settings)
        print('   Done!')

    
# Get the operator for the button
class CompareButtonOperator(bpy.types.Operator):
    """Compare to the file"""
    bl_idname = "setmgr.compare"
    bl_label = "Settings Manager"

    def execute(self, context):
        filename = context.scene.my_tool.compare_filename
        self.compareFile(context, filename)
        return {'FINISHED'}
    
    def compareFile(self, context, filename):
        print('Comparing to file: ' + filename)
        # DO COMPARISON HERE
        
        print('Comparison Results')


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
        
        # Compare
        row = layout.row()
        row.label(text="Compare File:")
        
        layout.prop(mytool, "compare_filename")
        row = layout.row()
        row.operator(CompareButtonOperator.bl_idname, text="Compare To", icon='LINENUMBERS_ON')
    
# I discovered this class at https://b3d.interplanety.org/en/creating-pop-up-panels-with-user-ui-in-blender-add-on/
class MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""
 
    def execute(self, context):
        # self.report({'INFO'}, self.message)
        self.report({'INFO'}, context.scene.my_tool.message)
        # print(self.message)
        print(context.scene.my_tool.message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        # self.layout.label(self.message)
        mymsg = context.scene.my_tool.message
        self.layout.label(mymsg)
        # context.scene.my_tool.message
        self.layout.label("")
