import bpy
import os

# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

# Cleanup the filename to match Blender standards (ie use // as the filename
# prefix if it is stored in the same directory ad the main Blender file.)
def cleanupFileName(origFileName):
    # Clean up the file names
        curDir = bpy.path.abspath("//")

        # Does any directory info exist in the current save file name?
        osdir = os.path.dirname(origFileName)
        # print('os.path.dirname RAW = ' + osdir)
        if(osdir == ''):
            # No directory information is given. Assume the local directory for the file
            # print("osdir == ''")
            fn = "//" + origFileName

        if(origFileName.startswith('//')):
            # They are already using the shorthand for the local file directory.
            # Make no changes!
            fn = bpy.path.abspath(origFileName)
        elif(origFileName.startswith(curDir)):
            # They are using the fully qualified path name. Shorten it in the property
            fn = origFileName.replace(curDir, '//')
        else:
            # Looks like a different directory has been specified
            fn = bpy.path.abspath(origFileName)

        # print('fn = ' + fn)
        fn = bpy.path.ensure_ext(fn, '.json', case_sensitive=False)
        # print('adj filename = ' + fn)
        return fn


class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Some Data"

    # ImportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    isSaveFile: BoolProperty(
        name="Is Save File Name",
        description="This is true if this is for the file we want to save, False if its the file we want to load.",
        options={'HIDDEN'},
        default=False
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return self.read_some_data(context, self.filepath, self.use_setting)

    def read_some_data(self, context, filepath, use_some_setting):
        print("running read_some_data...")
        fn = cleanupFileName(filepath)
        # f = open(filepath, 'r', encoding='utf-8')
        print(fn)
        scene = context.scene
        mytool = scene.my_tool
        if(self.isSaveFile):
            print('Save file name = ' + fn)
            mytool.save_filename = fn
        else:
            print('Load file name = ' + fn)
            mytool.load_filename = fn

        # data = f.read()
        # f.close()

        # would normally load the data here
        # print(data)

        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportSomeData.bl_idname, text="Text Import Operator")


# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSomeData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.import_test.some_data('INVOKE_DEFAULT')
