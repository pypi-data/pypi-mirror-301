import typing
import collections.abc
import typing_extensions
import bl_operators.wm
import bpy.types

def alembic_export(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = True,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    start: int | None = -2147483648,
    end: int | None = -2147483648,
    xsamples: int | None = 1,
    gsamples: int | None = 1,
    sh_open: float | None = 0.0,
    sh_close: float | None = 1.0,
    selected: bool | None = False,
    renderable_only: bool | None = True,
    visible_objects_only: bool | None = False,
    flatten: bool | None = False,
    uvs: bool | None = True,
    packuv: bool | None = True,
    normals: bool | None = True,
    vcolors: bool | None = False,
    face_sets: bool | None = False,
    subdiv_schema: bool | None = False,
    apply_subdiv: bool | None = False,
    curves_as_mesh: bool | None = False,
    global_scale: float | None = 1.0,
    triangulate: bool | None = False,
    quad_method: typing.Literal[
        "BEAUTY", "FIXED", "FIXED_ALTERNATE", "SHORTEST_DIAGONAL"
    ]
    | None = "SHORTEST_DIAGONAL",
    ngon_method: typing.Literal[
        "BEAUTY", "FIXED", "FIXED_ALTERNATE", "SHORTEST_DIAGONAL"
    ]
    | None = "BEAUTY",
    export_hair: bool | None = True,
    export_particles: bool | None = True,
    as_background_job: bool | None = False,
    init_scene_frame_range: bool | None = False,
):
    """Export current scene in an Alembic archive

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param start: Start Frame, Start frame of the export, use the default value to take the start frame of the current scene
        :type start: int | None
        :param end: End Frame, End frame of the export, use the default value to take the end frame of the current scene
        :type end: int | None
        :param xsamples: Transform Samples, Number of times per frame transformations are sampled
        :type xsamples: int | None
        :param gsamples: Geometry Samples, Number of times per frame object data are sampled
        :type gsamples: int | None
        :param sh_open: Shutter Open, Time at which the shutter is open
        :type sh_open: float | None
        :param sh_close: Shutter Close, Time at which the shutter is closed
        :type sh_close: float | None
        :param selected: Selected Objects Only, Export only selected objects
        :type selected: bool | None
        :param renderable_only: Renderable Objects Only, Export only objects marked renderable in the outliner
        :type renderable_only: bool | None
        :param visible_objects_only: Visible Objects Only, Export only objects that are visible
        :type visible_objects_only: bool | None
        :param flatten: Flatten Hierarchy, Do not preserve objects' parent/children relationship
        :type flatten: bool | None
        :param uvs: UVs, Export UVs
        :type uvs: bool | None
        :param packuv: Pack UV Islands, Export UVs with packed island
        :type packuv: bool | None
        :param normals: Normals, Export normals
        :type normals: bool | None
        :param vcolors: Vertex Colors, Export vertex colors
        :type vcolors: bool | None
        :param face_sets: Face Sets, Export per face shading group assignments
        :type face_sets: bool | None
        :param subdiv_schema: Use Subdivision Schema, Export meshes using Alembic's subdivision schema
        :type subdiv_schema: bool | None
        :param apply_subdiv: Apply Subdivision Surface, Export subdivision surfaces as meshes
        :type apply_subdiv: bool | None
        :param curves_as_mesh: Curves as Mesh, Export curves and NURBS surfaces as meshes
        :type curves_as_mesh: bool | None
        :param global_scale: Scale, Value by which to enlarge or shrink the objects with respect to the world's origin
        :type global_scale: float | None
        :param triangulate: Triangulate, Export Polygons (Quads & NGons) as Triangles
        :type triangulate: bool | None
        :param quad_method: Quad Method, Method for splitting the quads into triangles

    BEAUTY
    Beauty , Split the quads in nice triangles, slower method.

    FIXED
    Fixed, Split the quads on the first and third vertices.

    FIXED_ALTERNATE
    Fixed Alternate, Split the quads on the 2nd and 4th vertices.

    SHORTEST_DIAGONAL
    Shortest Diagonal, Split the quads based on the distance between the vertices.
        :type quad_method: typing.Literal['BEAUTY','FIXED','FIXED_ALTERNATE','SHORTEST_DIAGONAL'] | None
        :param ngon_method: Polygon Method, Method for splitting the polygons into triangles

    BEAUTY
    Beauty , Split the quads in nice triangles, slower method.

    FIXED
    Fixed, Split the quads on the first and third vertices.

    FIXED_ALTERNATE
    Fixed Alternate, Split the quads on the 2nd and 4th vertices.

    SHORTEST_DIAGONAL
    Shortest Diagonal, Split the quads based on the distance between the vertices.
        :type ngon_method: typing.Literal['BEAUTY','FIXED','FIXED_ALTERNATE','SHORTEST_DIAGONAL'] | None
        :param export_hair: Export Hair, Exports hair particle systems as animated curves
        :type export_hair: bool | None
        :param export_particles: Export Particles, Exports non-hair particle systems
        :type export_particles: bool | None
        :param as_background_job: Run as Background Job, Enable this to run the import in the background, disable to block Blender while importing. This option is deprecated; EXECUTE this operator to run in the foreground, and INVOKE it to run as a background job
        :type as_background_job: bool | None
        :type init_scene_frame_range: bool | None
    """

def alembic_import(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = True,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    scale: float | None = 1.0,
    set_frame_range: bool | None = True,
    validate_meshes: bool | None = False,
    is_sequence: bool | None = False,
    as_background_job: bool | None = False,
):
    """Load an Alembic archive

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param scale: Scale, Value by which to enlarge or shrink the objects with respect to the world's origin
        :type scale: float | None
        :param set_frame_range: Set Frame Range, If checked, update scene's start and end frame to match those of the Alembic archive
        :type set_frame_range: bool | None
        :param validate_meshes: Validate Meshes, Check imported mesh objects for invalid data (slow)
        :type validate_meshes: bool | None
        :param is_sequence: Is Sequence, Set to true if the cache is split into separate files
        :type is_sequence: bool | None
        :param as_background_job: Run as Background Job, Enable this to run the export in the background, disable to block Blender while exporting. This option is deprecated; EXECUTE this operator to run in the foreground, and INVOKE it to run as a background job
        :type as_background_job: bool | None
    """

def append(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    directory: str = "",
    filename: str = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = True,
    filemode: int | None = 1,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    link: bool | None = False,
    autoselect: bool | None = True,
    active_collection: bool | None = True,
    instance_collections: bool | None = False,
    set_fake: bool | None = False,
    use_recursive: bool | None = True,
):
    """Append from a Library .blend file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param directory: Directory, Directory of the file
        :type directory: str
        :param filename: File Name, Name of the file
        :type filename: str
        :param files: Files
        :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param link: Link, Link the objects or data-blocks rather than appending
        :type link: bool | None
        :param autoselect: Select, Select new objects
        :type autoselect: bool | None
        :param active_collection: Active Collection, Put new objects on the active collection
        :type active_collection: bool | None
        :param instance_collections: Instance Collections, Create instances for collections, rather than adding them directly to the scene
        :type instance_collections: bool | None
        :param set_fake: Fake User, Set Fake User for appended items (except Objects and Groups)
        :type set_fake: bool | None
        :param use_recursive: Localize All, Localize all appended data, including those indirectly linked from other libraries
        :type use_recursive: bool | None
    """

def batch_rename(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_type: typing.Literal[
        "OBJECT",
        "MATERIAL",
        "MESH",
        "CURVE",
        "META",
        "ARMATURE",
        "LATTICE",
        "GPENCIL",
        "CAMERA",
        "SPEAKER",
        "LIGHT_PROBE",
        "BONE",
        "NODE",
        "SEQUENCE_STRIP",
    ]
    | None = "OBJECT",
    data_source: typing.Literal["SELECT", "ALL"] | None = "SELECT",
    actions: bpy.types.bpy_prop_collection[bl_operators.wm.BatchRenameAction]
    | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_type: Type, Type of data to rename
    :type data_type: typing.Literal['OBJECT','MATERIAL','MESH','CURVE','META','ARMATURE','LATTICE','GPENCIL','CAMERA','SPEAKER','LIGHT_PROBE','BONE','NODE','SEQUENCE_STRIP'] | None
    :param data_source: Source
    :type data_source: typing.Literal['SELECT','ALL'] | None
    :param actions: actions
    :type actions: bpy.types.bpy_prop_collection[bl_operators.wm.BatchRenameAction] | None
    """

def blend_strings_utf8_validate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Check and fix all strings in current .blend file to be valid UTF-8 Unicode (needed for some old, 2.4x area files)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def call_menu(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
):
    """Call (draw) a pre-defined menu

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the menu
    :type name: str
    """

def call_menu_pie(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
):
    """Call (draw) a pre-defined pie menu

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the pie menu
    :type name: str
    """

def call_panel(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    keep_open: bool | None = True,
):
    """Call (draw) a pre-defined panel

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the menu
    :type name: str
    :param keep_open: Keep Open
    :type keep_open: bool | None
    """

def collada_export(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = True,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    prop_bc_export_ui_section: typing.Literal[
        "main", "geometry", "armature", "animation", "collada"
    ]
    | None = "main",
    apply_modifiers: bool | None = False,
    export_mesh_type: int | None = 0,
    export_mesh_type_selection: typing.Literal["view", "render"] | None = "view",
    export_global_forward_selection: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"]
    | None = "Y",
    export_global_up_selection: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"]
    | None = "Z",
    apply_global_orientation: bool | None = False,
    selected: bool | None = False,
    include_children: bool | None = False,
    include_armatures: bool | None = False,
    include_shapekeys: bool | None = False,
    deform_bones_only: bool | None = False,
    include_animations: bool | None = True,
    include_all_actions: bool | None = True,
    export_animation_type_selection: typing.Literal["sample", "keys"] | None = "sample",
    sampling_rate: int | None = 1,
    keep_smooth_curves: bool | None = False,
    keep_keyframes: bool | None = False,
    keep_flat_curves: bool | None = False,
    active_uv_only: bool | None = False,
    use_texture_copies: bool | None = True,
    triangulate: bool | None = True,
    use_object_instantiation: bool | None = True,
    use_blender_profile: bool | None = True,
    sort_by_name: bool | None = False,
    export_object_transformation_type: int | None = 0,
    export_object_transformation_type_selection: typing.Literal["matrix", "decomposed"]
    | None = "matrix",
    export_animation_transformation_type: int | None = 0,
    export_animation_transformation_type_selection: typing.Literal[
        "matrix", "decomposed"
    ]
    | None = "matrix",
    open_sim: bool | None = False,
    limit_precision: bool | None = False,
    keep_bind_info: bool | None = False,
):
    """Save a Collada file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param prop_bc_export_ui_section: Export Section, Only for User Interface organization

    main
    Main, Data Export Section.

    geometry
    Geom, Geometry Export Section.

    armature
    Arm, Armature Export Section.

    animation
    Anim, Animation Export Section.

    collada
    Extra, Collada Export Section.
        :type prop_bc_export_ui_section: typing.Literal['main','geometry','armature','animation','collada'] | None
        :param apply_modifiers: Apply Modifiers, Apply modifiers to exported mesh (non destructive))
        :type apply_modifiers: bool | None
        :param export_mesh_type: Resolution, Modifier resolution for export
        :type export_mesh_type: int | None
        :param export_mesh_type_selection: Resolution, Modifier resolution for export

    view
    Viewport, Apply modifier's viewport settings.

    render
    Render, Apply modifier's render settings.
        :type export_mesh_type_selection: typing.Literal['view','render'] | None
        :param export_global_forward_selection: Global Forward Axis, Global Forward axis for export

    X
    X, Global Forward is positive X Axis.

    Y
    Y, Global Forward is positive Y Axis.

    Z
    Z, Global Forward is positive Z Axis.

    -X
    -X, Global Forward is negative X Axis.

    -Y
    -Y, Global Forward is negative Y Axis.

    -Z
    -Z, Global Forward is negative Z Axis.
        :type export_global_forward_selection: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
        :param export_global_up_selection: Global Up Axis, Global Up axis for export

    X
    X, Global UP is positive X Axis.

    Y
    Y, Global UP is positive Y Axis.

    Z
    Z, Global UP is positive Z Axis.

    -X
    -X, Global UP is negative X Axis.

    -Y
    -Y, Global UP is negative Y Axis.

    -Z
    -Z, Global UP is negative Z Axis.
        :type export_global_up_selection: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
        :param apply_global_orientation: Apply Global Orientation, Rotate all root objects to match the global orientation settings otherwise set the global orientation per Collada asset
        :type apply_global_orientation: bool | None
        :param selected: Selection Only, Export only selected elements
        :type selected: bool | None
        :param include_children: Include Children, Export all children of selected objects (even if not selected)
        :type include_children: bool | None
        :param include_armatures: Include Armatures, Export related armatures (even if not selected)
        :type include_armatures: bool | None
        :param include_shapekeys: Include Shape Keys, Export all Shape Keys from Mesh Objects
        :type include_shapekeys: bool | None
        :param deform_bones_only: Deform Bones Only, Only export deforming bones with armatures
        :type deform_bones_only: bool | None
        :param include_animations: Include Animations, Export animations if available (exporting animations will enforce the decomposition of node transforms into  <translation> <rotation> and <scale> components)
        :type include_animations: bool | None
        :param include_all_actions: Include all Actions, Export also unassigned actions (this allows you to export entire animation libraries for your character(s))
        :type include_all_actions: bool | None
        :param export_animation_type_selection: Key Type, Type for exported animations (use sample keys or Curve keys)

    sample
    Samples, Export Sampled points guided by sampling rate.

    keys
    Curves, Export Curves (note: guided by curve keys).
        :type export_animation_type_selection: typing.Literal['sample','keys'] | None
        :param sampling_rate: Sampling Rate, The distance between 2 keyframes (1 to key every frame)
        :type sampling_rate: int | None
        :param keep_smooth_curves: Keep Smooth curves, Export also the curve handles (if available) (this does only work when the inverse parent matrix is the unity matrix, otherwise you may end up with odd results)
        :type keep_smooth_curves: bool | None
        :param keep_keyframes: Keep Keyframes, Use existing keyframes as additional sample points (this helps when you want to keep manual tweaks)
        :type keep_keyframes: bool | None
        :param keep_flat_curves: All Keyed Curves, Export also curves which have only one key or are totally flat
        :type keep_flat_curves: bool | None
        :param active_uv_only: Only Selected UV Map, Export only the selected UV Map
        :type active_uv_only: bool | None
        :param use_texture_copies: Copy, Copy textures to same folder where the .dae file is exported
        :type use_texture_copies: bool | None
        :param triangulate: Triangulate, Export Polygons (Quads & NGons) as Triangles
        :type triangulate: bool | None
        :param use_object_instantiation: Use Object Instances, Instantiate multiple Objects from same Data
        :type use_object_instantiation: bool | None
        :param use_blender_profile: Use Blender Profile, Export additional Blender specific information (for material, shaders, bones, etc.)
        :type use_blender_profile: bool | None
        :param sort_by_name: Sort by Object name, Sort exported data by Object name
        :type sort_by_name: bool | None
        :param export_object_transformation_type: Transform, Object Transformation type for translation, scale and rotation
        :type export_object_transformation_type: int | None
        :param export_object_transformation_type_selection: Transform, Object Transformation type for translation, scale and rotation

    matrix
    Matrix, Use <matrix> representation for exported transformations.

    decomposed
    Decomposed, Use <rotate>, <translate> and <scale> representation for exported transformations.
        :type export_object_transformation_type_selection: typing.Literal['matrix','decomposed'] | None
        :param export_animation_transformation_type: Transform, Transformation type for translation, scale and rotation. Note: The Animation transformation type in the Anim Tab is always equal to the Object transformation type in the Geom tab
        :type export_animation_transformation_type: int | None
        :param export_animation_transformation_type_selection: Transform, Transformation type for translation, scale and rotation. Note: The Animation transformation type in the Anim Tab is always equal to the Object transformation type in the Geom tab

    matrix
    Matrix, Use <matrix> representation for exported transformations.

    decomposed
    Decomposed, Use <rotate>, <translate> and <scale> representation for exported transformations.
        :type export_animation_transformation_type_selection: typing.Literal['matrix','decomposed'] | None
        :param open_sim: Export to SL/OpenSim, Compatibility mode for SL, OpenSim and other compatible online worlds
        :type open_sim: bool | None
        :param limit_precision: Limit Precision, Reduce the precision of the exported data to 6 digits
        :type limit_precision: bool | None
        :param keep_bind_info: Keep Bind Info, Store Bindpose information in custom bone properties for later use during Collada export
        :type keep_bind_info: bool | None
    """

def collada_import(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = True,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    import_units: bool | None = False,
    fix_orientation: bool | None = False,
    find_chains: bool | None = False,
    auto_connect: bool | None = False,
    min_chain_length: int | None = 0,
    keep_bind_info: bool | None = False,
):
    """Load a Collada file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param import_units: Import Units, If disabled match import to Blender's current Unit settings, otherwise use the settings from the Imported scene
        :type import_units: bool | None
        :param fix_orientation: Fix Leaf Bones, Fix Orientation of Leaf Bones (Collada does only support Joints)
        :type fix_orientation: bool | None
        :param find_chains: Find Bone Chains, Find best matching Bone Chains and ensure bones in chain are connected
        :type find_chains: bool | None
        :param auto_connect: Auto Connect, Set use_connect for parent bones which have exactly one child bone
        :type auto_connect: bool | None
        :param min_chain_length: Minimum Chain Length, When searching Bone Chains disregard chains of length below this value
        :type min_chain_length: int | None
        :param keep_bind_info: Keep Bind Info, Store Bindpose information in custom bone properties for later use during Collada export
        :type keep_bind_info: bool | None
    """

def context_collection_boolean_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path_iter: str = "",
    data_path_item: str = "",
    type: typing.Literal["TOGGLE", "ENABLE", "DISABLE"] | None = "TOGGLE",
):
    """Set boolean values for a collection of items

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path_iter: data_path_iter, The data path relative to the context, must point to an iterable
    :type data_path_iter: str
    :param data_path_item: data_path_item, The data path from each iterable to the value (int or float)
    :type data_path_item: str
    :param type: Type
    :type type: typing.Literal['TOGGLE','ENABLE','DISABLE'] | None
    """

def context_cycle_array(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    reverse: bool | None = False,
):
    """Set a context array value (useful for cycling the active mesh edit mode)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param reverse: Reverse, Cycle backwards
    :type reverse: bool | None
    """

def context_cycle_enum(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    reverse: bool | None = False,
    wrap: bool | None = False,
):
    """Toggle a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param reverse: Reverse, Cycle backwards
    :type reverse: bool | None
    :param wrap: Wrap, Wrap back to the first/last values
    :type wrap: bool | None
    """

def context_cycle_int(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    reverse: bool | None = False,
    wrap: bool | None = False,
):
    """Set a context value (useful for cycling active material, vertex keys, groups, etc.)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param reverse: Reverse, Cycle backwards
    :type reverse: bool | None
    :param wrap: Wrap, Wrap back to the first/last values
    :type wrap: bool | None
    """

def context_menu_enum(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    """

def context_modal_mouse(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path_iter: str = "",
    data_path_item: str = "",
    header_text: str = "",
    input_scale: float | None = 0.01,
    invert: bool | None = False,
    initial_x: int | None = 0,
):
    """Adjust arbitrary values with mouse input

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path_iter: data_path_iter, The data path relative to the context, must point to an iterable
    :type data_path_iter: str
    :param data_path_item: data_path_item, The data path from each iterable to the value (int or float)
    :type data_path_item: str
    :param header_text: Header Text, Text to display in header during scale
    :type header_text: str
    :param input_scale: input_scale, Scale the mouse movement by this value before applying the delta
    :type input_scale: float | None
    :param invert: invert, Invert the mouse input
    :type invert: bool | None
    :param initial_x: initial_x
    :type initial_x: int | None
    """

def context_pie_enum(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    """

def context_scale_float(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: float | None = 1.0,
):
    """Scale a float context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assign value
    :type value: float | None
    """

def context_scale_int(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: float | None = 1.0,
    always_step: bool | None = True,
):
    """Scale an int context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assign value
    :type value: float | None
    :param always_step: Always Step, Always adjust the value by a minimum of 1 when 'value' is not 1.0
    :type always_step: bool | None
    """

def context_set_boolean(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: bool | None = True,
):
    """Set a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assignment value
    :type value: bool | None
    """

def context_set_enum(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: str = "",
):
    """Set a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assignment value (as a string)
    :type value: str
    """

def context_set_float(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: float | None = 0.0,
    relative: bool | None = False,
):
    """Set a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assignment value
    :type value: float | None
    :param relative: Relative, Apply relative to the current value (delta)
    :type relative: bool | None
    """

def context_set_id(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: str = "",
):
    """Set a context value to an ID data-block

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assign value
    :type value: str
    """

def context_set_int(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: int | None = 0,
    relative: bool | None = False,
):
    """Set a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assign value
    :type value: int | None
    :param relative: Relative, Apply relative to the current value (delta)
    :type relative: bool | None
    """

def context_set_string(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: str = "",
):
    """Set a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assign value
    :type value: str
    """

def context_set_value(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value: str = "",
):
    """Set a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value: Value, Assignment value (as a string)
    :type value: str
    """

def context_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    module: str = "",
):
    """Toggle a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param module: Module, Optionally override the context with a module
    :type module: str
    """

def context_toggle_enum(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    value_1: str = "",
    value_2: str = "",
):
    """Toggle a context value

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Context Attributes, RNA context string
    :type data_path: str
    :param value_1: Value, Toggle enum
    :type value_1: str
    :param value_2: Value, Toggle enum
    :type value_2: str
    """

def debug_menu(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    debug_value: int | None = 0,
):
    """Open a popup to set the debug level

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param debug_value: Debug Value
    :type debug_value: int | None
    """

def doc_view(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    doc_id: str = "",
):
    """Open online reference docs in a web browser

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param doc_id: Doc ID
    :type doc_id: str
    """

def doc_view_manual(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    doc_id: str = "",
):
    """Load online manual

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param doc_id: Doc ID
    :type doc_id: str
    """

def doc_view_manual_ui_context(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """View a context based online manual in a web browser

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def drop_blend_file(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    """

def interface_theme_preset_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
):
    """Add or remove a theme preset

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the preset, used to make the path name
    :type name: str
    :param remove_name: remove_name
    :type remove_name: bool | None
    :param remove_active: remove_active
    :type remove_active: bool | None
    """

def keyconfig_preset_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
):
    """Add or remove a Key-config Preset

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the preset, used to make the path name
    :type name: str
    :param remove_name: remove_name
    :type remove_name: bool | None
    :param remove_active: remove_active
    :type remove_active: bool | None
    """

def lib_reload(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    library: str = "",
    filepath: str = "",
    directory: str = "",
    filename: str = "",
    hide_props_region: bool | None = True,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
):
    """Reload the given library

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param library: Library, Library to reload
        :type library: str
        :param filepath: File Path, Path to file
        :type filepath: str
        :param directory: Directory, Directory of the file
        :type directory: str
        :param filename: File Name, Name of the file
        :type filename: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
    """

def lib_relocate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    library: str = "",
    filepath: str = "",
    directory: str = "",
    filename: str = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    hide_props_region: bool | None = True,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
):
    """Relocate the given library to one or several others

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param library: Library, Library to relocate
        :type library: str
        :param filepath: File Path, Path to file
        :type filepath: str
        :param directory: Directory, Directory of the file
        :type directory: str
        :param filename: File Name, Name of the file
        :type filename: str
        :param files: Files
        :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
    """

def link(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    directory: str = "",
    filename: str = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = True,
    filemode: int | None = 1,
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    link: bool | None = True,
    autoselect: bool | None = True,
    active_collection: bool | None = True,
    instance_collections: bool | None = True,
):
    """Link from a Library .blend file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param directory: Directory, Directory of the file
        :type directory: str
        :param filename: File Name, Name of the file
        :type filename: str
        :param files: Files
        :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param link: Link, Link the objects or data-blocks rather than appending
        :type link: bool | None
        :param autoselect: Select, Select new objects
        :type autoselect: bool | None
        :param active_collection: Active Collection, Put new objects on the active collection
        :type active_collection: bool | None
        :param instance_collections: Instance Collections, Create instances for collections, rather than adding them directly to the scene
        :type instance_collections: bool | None
    """

def memory_statistics(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Print memory statistics to the console

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def open_mainfile(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    load_ui: bool | None = True,
    use_scripts: bool | None = True,
    display_file_selector: bool | None = True,
    state: int | None = 0,
):
    """Open a Blender file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param load_ui: Load UI, Load user interface setup in the .blend file
        :type load_ui: bool | None
        :param use_scripts: Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences
        :type use_scripts: bool | None
        :param display_file_selector: Display File Selector
        :type display_file_selector: bool | None
        :param state: State
        :type state: int | None
    """

def operator_cheat_sheet(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """List all the Operators in a text-block, useful for scripting

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def operator_defaults(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set the active operator to its default values

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def operator_pie_enum(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    prop_string: str = "",
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Operator, Operator name (in python as string)
    :type data_path: str
    :param prop_string: Property, Property name (as a string)
    :type prop_string: str
    """

def operator_preset_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
    operator: str = "",
):
    """Add or remove an Operator Preset

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Name of the preset, used to make the path name
    :type name: str
    :param remove_name: remove_name
    :type remove_name: bool | None
    :param remove_active: remove_active
    :type remove_active: bool | None
    :param operator: Operator
    :type operator: str
    """

def owner_disable(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    owner_id: str = "",
):
    """Enable workspace owner ID

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param owner_id: UI Tag
    :type owner_id: str
    """

def owner_enable(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    owner_id: str = "",
):
    """Enable workspace owner ID

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param owner_id: UI Tag
    :type owner_id: str
    """

def path_open(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
):
    """Open a path in a file browser

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    """

def previews_batch_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    directory: str = "",
    filter_blender: bool | None = True,
    filter_folder: bool | None = True,
    use_scenes: bool | None = True,
    use_collections: bool | None = True,
    use_objects: bool | None = True,
    use_intern_data: bool | None = True,
    use_trusted: bool | None = False,
    use_backups: bool | None = True,
):
    """Clear selected .blend file's previews

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param files: files
    :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
    :param directory: directory
    :type directory: str
    :param filter_blender: filter_blender
    :type filter_blender: bool | None
    :param filter_folder: filter_folder
    :type filter_folder: bool | None
    :param use_scenes: Scenes, Clear scenes' previews
    :type use_scenes: bool | None
    :param use_collections: Collections, Clear collections' previews
    :type use_collections: bool | None
    :param use_objects: Objects, Clear objects' previews
    :type use_objects: bool | None
    :param use_intern_data: Mat/Tex/..., Clear 'internal' previews (materials, textures, images, etc.)
    :type use_intern_data: bool | None
    :param use_trusted: Trusted Blend Files, Enable python evaluation for selected files
    :type use_trusted: bool | None
    :param use_backups: Save Backups, Keep a backup (.blend1) version of the files when saving with cleared previews
    :type use_backups: bool | None
    """

def previews_batch_generate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    directory: str = "",
    filter_blender: bool | None = True,
    filter_folder: bool | None = True,
    use_scenes: bool | None = True,
    use_collections: bool | None = True,
    use_objects: bool | None = True,
    use_intern_data: bool | None = True,
    use_trusted: bool | None = False,
    use_backups: bool | None = True,
):
    """Generate selected .blend file's previews

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param files: files
    :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
    :param directory: directory
    :type directory: str
    :param filter_blender: filter_blender
    :type filter_blender: bool | None
    :param filter_folder: filter_folder
    :type filter_folder: bool | None
    :param use_scenes: Scenes, Generate scenes' previews
    :type use_scenes: bool | None
    :param use_collections: Collections, Generate collections' previews
    :type use_collections: bool | None
    :param use_objects: Objects, Generate objects' previews
    :type use_objects: bool | None
    :param use_intern_data: Mat/Tex/..., Generate 'internal' previews (materials, textures, images, etc.)
    :type use_intern_data: bool | None
    :param use_trusted: Trusted Blend Files, Enable python evaluation for selected files
    :type use_trusted: bool | None
    :param use_backups: Save Backups, Keep a backup (.blend1) version of the files when saving with generated previews
    :type use_backups: bool | None
    """

def previews_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    id_type: set[
        typing.Literal[
            "ALL",
            "GEOMETRY",
            "SHADING",
            "SCENE",
            "COLLECTION",
            "OBJECT",
            "MATERIAL",
            "LIGHT",
            "WORLD",
            "TEXTURE",
            "IMAGE",
        ]
    ]
    | None = {},
):
    """Clear data-block previews (only for some types like objects, materials, textures, etc.)

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param id_type: Data-Block Type, Which data-block previews to clear

    ALL
    All Types.

    GEOMETRY
    All Geometry Types, Clear previews for scenes, collections and objects.

    SHADING
    All Shading Types, Clear previews for materials, lights, worlds, textures and images.

    SCENE
    Scenes.

    COLLECTION
    Collections.

    OBJECT
    Objects.

    MATERIAL
    Materials.

    LIGHT
    Lights.

    WORLD
    Worlds.

    TEXTURE
    Textures.

    IMAGE
    Images.
        :type id_type: set[typing.Literal['ALL','GEOMETRY','SHADING','SCENE','COLLECTION','OBJECT','MATERIAL','LIGHT','WORLD','TEXTURE','IMAGE']] | None
    """

def previews_ensure(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Ensure data-block previews are available and up-to-date (to be saved in .blend file, only for some types like materials, textures, etc.)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def properties_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
):
    """Add your own property to the data-block

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Property Edit, Property data_path edit
    :type data_path: str
    """

def properties_context_change(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    context: str = "",
):
    """Jump to a different tab inside the properties editor

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param context: Context
    :type context: str
    """

def properties_edit(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    property: str = "",
    value: str = "",
    default: str = "",
    min: float | None = -10000,
    max: float | None = 10000.0,
    use_soft_limits: bool | None = False,
    is_overridable_library: bool | None = False,
    soft_min: float | None = -10000,
    soft_max: float | None = 10000.0,
    description: str = "",
    subtype: str | None = "",
):
    """Edit the attributes of the property

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Property Edit, Property data_path edit
    :type data_path: str
    :param property: Property Name, Property name edit
    :type property: str
    :param value: Property Value, Property value edit
    :type value: str
    :param default: Default Value, Default value of the property. Important for NLA mixing
    :type default: str
    :param min: Min, Minimum value of the property
    :type min: float | None
    :param max: Max, Maximum value of the property
    :type max: float | None
    :param use_soft_limits: Use Soft Limits, Limits the Property Value slider to a range, values outside the range must be inputted numerically
    :type use_soft_limits: bool | None
    :param is_overridable_library: Is Library Overridable, Allow the property to be overridden when the Data-Block is linked
    :type is_overridable_library: bool | None
    :param soft_min: Min, Minimum value of the property
    :type soft_min: float | None
    :param soft_max: Max, Maximum value of the property
    :type soft_max: float | None
    :param description: Tooltip
    :type description: str
    :param subtype: Subtype
    :type subtype: str | None
    """

def properties_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path: str = "",
    property: str = "",
):
    """Internal use (edit a property data_path)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path: Property Edit, Property data_path edit
    :type data_path: str
    :param property: Property Name, Property name edit
    :type property: str
    """

def quit_blender(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Quit Blender

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def radial_control(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    data_path_primary: str = "",
    data_path_secondary: str = "",
    use_secondary: str = "",
    rotation_path: str = "",
    color_path: str = "",
    fill_color_path: str = "",
    fill_color_override_path: str = "",
    fill_color_override_test_path: str = "",
    zoom_path: str = "",
    image_id: str = "",
    secondary_tex: bool | None = False,
):
    """Set some size property (like e.g. brush size) with mouse wheel

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param data_path_primary: Primary Data Path, Primary path of property to be set by the radial control
    :type data_path_primary: str
    :param data_path_secondary: Secondary Data Path, Secondary path of property to be set by the radial control
    :type data_path_secondary: str
    :param use_secondary: Use Secondary, Path of property to select between the primary and secondary data paths
    :type use_secondary: str
    :param rotation_path: Rotation Path, Path of property used to rotate the texture display
    :type rotation_path: str
    :param color_path: Color Path, Path of property used to set the color of the control
    :type color_path: str
    :param fill_color_path: Fill Color Path, Path of property used to set the fill color of the control
    :type fill_color_path: str
    :param fill_color_override_path: Fill Color Override Path
    :type fill_color_override_path: str
    :param fill_color_override_test_path: Fill Color Override Test
    :type fill_color_override_test_path: str
    :param zoom_path: Zoom Path, Path of property used to set the zoom level for the control
    :type zoom_path: str
    :param image_id: Image ID, Path of ID that is used to generate an image for the control
    :type image_id: str
    :param secondary_tex: Secondary Texture, Tweak brush secondary/mask texture
    :type secondary_tex: bool | None
    """

def read_factory_settings(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    app_template: str = "Template",
    use_empty: bool | None = False,
):
    """Load factory default startup file and preferences. To make changes permanent, use "Save Startup File" and "Save Preferences"

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :type app_template: str
    :param use_empty: Empty
    :type use_empty: bool | None
    """

def read_factory_userpref(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Load factory default preferences. To make changes to preferences permanent, use "Save Preferences"

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def read_history(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reloads history and bookmarks

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def read_homefile(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    load_ui: bool | None = True,
    use_splash: bool | None = False,
    app_template: str = "Template",
    use_empty: bool | None = False,
):
    """Open the default file (doesn't save the current file)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: File Path, Path to an alternative start-up file
    :type filepath: str
    :param load_ui: Load UI, Load user interface setup from the .blend file
    :type load_ui: bool | None
    :param use_splash: Splash
    :type use_splash: bool | None
    :type app_template: str
    :param use_empty: Empty
    :type use_empty: bool | None
    """

def read_userpref(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Load last saved preferences

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def recover_auto_save(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = False,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "LIST_VERTICAL",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_TIME",
):
    """Open an automatically saved file to recover it

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
    """

def recover_last_session(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Open the last closed file ("quit.blend")

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def redraw_timer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "DRAW",
        "DRAW_SWAP",
        "DRAW_WIN",
        "DRAW_WIN_SWAP",
        "ANIM_STEP",
        "ANIM_PLAY",
        "UNDO",
    ]
    | None = "DRAW",
    iterations: int | None = 10,
    time_limit: float | None = 0.0,
):
    """Simple redraw timer to test the speed of updating the interface

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    DRAW
    Draw Region, Draw Region.

    DRAW_SWAP
    Draw Region + Swap, Draw Region and Swap.

    DRAW_WIN
    Draw Window, Draw Window.

    DRAW_WIN_SWAP
    Draw Window + Swap, Draw Window and Swap.

    ANIM_STEP
    Anim Step, Animation Steps.

    ANIM_PLAY
    Anim Play, Animation Playback.

    UNDO
    Undo/Redo, Undo/Redo.
        :type type: typing.Literal['DRAW','DRAW_SWAP','DRAW_WIN','DRAW_WIN_SWAP','ANIM_STEP','ANIM_PLAY','UNDO'] | None
        :param iterations: Iterations, Number of times to redraw
        :type iterations: int | None
        :param time_limit: Time Limit, Seconds to run the test for (override iterations)
        :type time_limit: float | None
    """

def revert_mainfile(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_scripts: bool | None = True,
):
    """Reload the saved file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_scripts: Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences
    :type use_scripts: bool | None
    """

def save_as_mainfile(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    compress: bool | None = False,
    relative_remap: bool | None = True,
    copy: bool | None = False,
):
    """Save the current file in the desired location

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param compress: Compress, Write compressed .blend file
        :type compress: bool | None
        :param relative_remap: Remap Relative, Remap relative paths when saving to a different directory
        :type relative_remap: bool | None
        :param copy: Save Copy, Save a copy of the actual working state but does not make saved file active
        :type copy: bool | None
    """

def save_homefile(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Make the current file the default .blend file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def save_mainfile(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
    filter_blender: bool | None = True,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    compress: bool | None = False,
    relative_remap: bool | None = False,
    exit: bool | None = False,
):
    """Save the current Blender file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param compress: Compress, Write compressed .blend file
        :type compress: bool | None
        :param relative_remap: Remap Relative, Remap relative paths when saving to a different directory
        :type relative_remap: bool | None
        :param exit: Exit, Exit Blender after saving
        :type exit: bool | None
    """

def save_userpref(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Make the current preferences default

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def search_menu(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Pop-up a search over all menus in the current context

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def search_operator(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Pop-up a search over all available operators in current context

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_stereo_3d(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    display_mode: typing.Literal[
        "ANAGLYPH", "INTERLACE", "TIMESEQUENTIAL", "SIDEBYSIDE", "TOPBOTTOM"
    ]
    | None = "ANAGLYPH",
    anaglyph_type: typing.Literal["RED_CYAN", "GREEN_MAGENTA", "YELLOW_BLUE"]
    | None = "RED_CYAN",
    interlace_type: typing.Literal[
        "ROW_INTERLEAVED", "COLUMN_INTERLEAVED", "CHECKERBOARD_INTERLEAVED"
    ]
    | None = "ROW_INTERLEAVED",
    use_interlace_swap: bool | None = False,
    use_sidebyside_crosseyed: bool | None = False,
):
    """Toggle 3D stereo support for current window (or change the display mode)

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param display_mode: Display Mode

    ANAGLYPH
    Anaglyph, Render views for left and right eyes as two differently filtered colors in a single image (anaglyph glasses are required).

    INTERLACE
    Interlace, Render views for left and right eyes interlaced in a single image (3D-ready monitor is required).

    TIMESEQUENTIAL
    Time Sequential, Render alternate eyes (also known as page flip, quad buffer support in the graphic card is required).

    SIDEBYSIDE
    Side-by-Side, Render views for left and right eyes side-by-side.

    TOPBOTTOM
    Top-Bottom, Render views for left and right eyes one above another.
        :type display_mode: typing.Literal['ANAGLYPH','INTERLACE','TIMESEQUENTIAL','SIDEBYSIDE','TOPBOTTOM'] | None
        :param anaglyph_type: Anaglyph Type
        :type anaglyph_type: typing.Literal['RED_CYAN','GREEN_MAGENTA','YELLOW_BLUE'] | None
        :param interlace_type: Interlace Type
        :type interlace_type: typing.Literal['ROW_INTERLEAVED','COLUMN_INTERLEAVED','CHECKERBOARD_INTERLEAVED'] | None
        :param use_interlace_swap: Swap Left/Right, Swap left and right stereo channels
        :type use_interlace_swap: bool | None
        :param use_sidebyside_crosseyed: Cross-Eyed, Right eye should see left image and vice-versa
        :type use_sidebyside_crosseyed: bool | None
    """

def splash(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Open the splash screen with release info

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def splash_about(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Open a window with information about Blender

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def sysinfo(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
):
    """Generate system information, saved into a text file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    """

def tool_set_by_id(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
    cycle: bool | None = False,
    as_fallback: bool | None = False,
    space_type: typing.Literal[
        "EMPTY",
        "VIEW_3D",
        "IMAGE_EDITOR",
        "NODE_EDITOR",
        "SEQUENCE_EDITOR",
        "CLIP_EDITOR",
        "DOPESHEET_EDITOR",
        "GRAPH_EDITOR",
        "NLA_EDITOR",
        "TEXT_EDITOR",
        "CONSOLE",
        "INFO",
        "TOPBAR",
        "STATUSBAR",
        "OUTLINER",
        "PROPERTIES",
        "FILE_BROWSER",
        "PREFERENCES",
    ]
    | None = "EMPTY",
):
    """Set the tool by name (for keymaps)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Identifier, Identifier of the tool
    :type name: str
    :param cycle: Cycle, Cycle through tools in this group
    :type cycle: bool | None
    :param as_fallback: Set Fallback, Set the fallback tool instead of the primary tool
    :type as_fallback: bool | None
    :param space_type: Type
    :type space_type: typing.Literal['EMPTY','VIEW_3D','IMAGE_EDITOR','NODE_EDITOR','SEQUENCE_EDITOR','CLIP_EDITOR','DOPESHEET_EDITOR','GRAPH_EDITOR','NLA_EDITOR','TEXT_EDITOR','CONSOLE','INFO','TOPBAR','STATUSBAR','OUTLINER','PROPERTIES','FILE_BROWSER','PREFERENCES'] | None
    """

def tool_set_by_index(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    index: int | None = 0,
    cycle: bool | None = False,
    expand: bool | None = True,
    as_fallback: bool | None = False,
    space_type: typing.Literal[
        "EMPTY",
        "VIEW_3D",
        "IMAGE_EDITOR",
        "NODE_EDITOR",
        "SEQUENCE_EDITOR",
        "CLIP_EDITOR",
        "DOPESHEET_EDITOR",
        "GRAPH_EDITOR",
        "NLA_EDITOR",
        "TEXT_EDITOR",
        "CONSOLE",
        "INFO",
        "TOPBAR",
        "STATUSBAR",
        "OUTLINER",
        "PROPERTIES",
        "FILE_BROWSER",
        "PREFERENCES",
    ]
    | None = "EMPTY",
):
    """Set the tool by index (for keymaps)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: Index in toolbar
    :type index: int | None
    :param cycle: Cycle, Cycle through tools in this group
    :type cycle: bool | None
    :param expand: expand, Include tool sub-groups
    :type expand: bool | None
    :param as_fallback: Set Fallback, Set the fallback tool instead of the primary
    :type as_fallback: bool | None
    :param space_type: Type
    :type space_type: typing.Literal['EMPTY','VIEW_3D','IMAGE_EDITOR','NODE_EDITOR','SEQUENCE_EDITOR','CLIP_EDITOR','DOPESHEET_EDITOR','GRAPH_EDITOR','NLA_EDITOR','TEXT_EDITOR','CONSOLE','INFO','TOPBAR','STATUSBAR','OUTLINER','PROPERTIES','FILE_BROWSER','PREFERENCES'] | None
    """

def toolbar(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def toolbar_fallback_pie(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def toolbar_prompt(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Leader key like functionality for accessing tools

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def url_open(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    url: str = "",
):
    """Open a website in the web-browser

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param url: URL, URL to open
    :type url: str
    """

def url_open_preset(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "",
    id: str = "",
):
    """Open a preset website in the web-browser

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Site
    :type type: str | None
    :param id: Identifier, Optional identifier
    :type id: str
    """

def usd_export(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = True,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    selected_objects_only: bool | None = False,
    export_animation: bool | None = False,
    export_hair: bool | None = False,
    export_uvmaps: bool | None = True,
    export_normals: bool | None = True,
    export_materials: bool | None = True,
    use_instancing: bool | None = False,
    evaluation_mode: typing.Literal["RENDER", "VIEWPORT"] | None = "RENDER",
):
    """Export current scene in a USD archive

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | None
        :param filter_image: Filter image files
        :type filter_image: bool | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | None
        :param filter_python: Filter python files
        :type filter_python: bool | None
        :param filter_font: Filter font files
        :type filter_font: bool | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | None
        :param filter_text: Filter text files
        :type filter_text: bool | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: int | None
        :param display_type: Display Type

    DEFAULT
    Default, Automatically determine display type for files.

    LIST_VERTICAL
    Short List, Display files as short list.

    LIST_HORIZONTAL
    Long List, Display files as a detailed list.

    THUMBNAIL
    Thumbnails, Display files as thumbnails.
        :type display_type: typing.Literal['DEFAULT','LIST_VERTICAL','LIST_HORIZONTAL','THUMBNAIL'] | None
        :param sort_method: File sorting mode

    FILE_SORT_ALPHA
    Name, Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension, Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date, Sort files by modification time.

    FILE_SORT_SIZE
    Size, Sort files by size.
        :type sort_method: typing.Literal['FILE_SORT_ALPHA','FILE_SORT_EXTENSION','FILE_SORT_TIME','FILE_SORT_SIZE'] | None
        :param selected_objects_only: Selection Only, Only selected objects are exported. Unselected parents of selected objects are exported as empty transform
        :type selected_objects_only: bool | None
        :param export_animation: Animation, When checked, the render frame range is exported. When false, only the current frame is exported
        :type export_animation: bool | None
        :param export_hair: Hair, When checked, hair is exported as USD curves
        :type export_hair: bool | None
        :param export_uvmaps: UV Maps, When checked, all UV maps of exported meshes are included in the export
        :type export_uvmaps: bool | None
        :param export_normals: Normals, When checked, normals of exported meshes are included in the export
        :type export_normals: bool | None
        :param export_materials: Materials, When checked, the viewport settings of materials are exported as USD preview materials, and material assignments are exported as geometry subsets
        :type export_materials: bool | None
        :param use_instancing: Instancing, When checked, instanced objects are exported as references in USD. When unchecked, instanced objects are exported as real objects
        :type use_instancing: bool | None
        :param evaluation_mode: Use Settings for, Determines visibility of objects, modifier settings, and other areas where there are different settings for viewport and rendering

    RENDER
    Render, Use Render settings for object visibility, modifier settings, etc.

    VIEWPORT
    Viewport, Use Viewport settings for object visibility, modifier settings, etc.
        :type evaluation_mode: typing.Literal['RENDER','VIEWPORT'] | None
    """

def window_close(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Close the current window

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def window_fullscreen_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle the current window fullscreen

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def window_new(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Create a new window

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def window_new_main(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Create a new main window with its own workspace and scene selection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def xr_session_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Open a view for use with virtual reality headsets, or close it if already opened

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """
