import typing
import collections.abc
import typing_extensions
import bpy.ops.transform
import bpy.types

def add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    type: typing.Literal[
        "MESH",
        "CURVE",
        "SURFACE",
        "META",
        "FONT",
        "HAIR",
        "POINTCLOUD",
        "VOLUME",
        "ARMATURE",
        "LATTICE",
        "EMPTY",
        "GPENCIL",
        "CAMERA",
        "LIGHT",
        "SPEAKER",
        "LIGHT_PROBE",
    ]
    | None = "EMPTY",
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add an object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param type: Type
        :type type: typing.Literal['MESH','CURVE','SURFACE','META','FONT','HAIR','POINTCLOUD','VOLUME','ARMATURE','LATTICE','EMPTY','GPENCIL','CAMERA','LIGHT','SPEAKER','LIGHT_PROBE'] | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def add_named(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    linked: bool | None = False,
    name: str = "",
):
    """Add named object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param linked: Linked, Duplicate object but not object data, linking to the original data
    :type linked: bool | None
    :param name: Name, Object name to add
    :type name: str
    """

def align(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    bb_quality: bool | None = True,
    align_mode: typing.Literal["OPT_1", "OPT_2", "OPT_3"] | None = "OPT_2",
    relative_to: typing.Literal["OPT_1", "OPT_2", "OPT_3", "OPT_4"] | None = "OPT_4",
    align_axis: set[typing.Literal["X", "Y", "Z"]] | None = {},
):
    """Align Objects

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param bb_quality: High Quality, Enables high quality calculation of the bounding box for perfect results on complex shape meshes with rotation/scale (Slow)
        :type bb_quality: bool | None
        :param align_mode: Align Mode:, Side of object to use for alignment
        :type align_mode: typing.Literal['OPT_1','OPT_2','OPT_3'] | None
        :param relative_to: Relative To:, Reference location to align to

    OPT_1
    Scene Origin, Use the Scene Origin as the position for the selected objects to align to.

    OPT_2
    3D Cursor, Use the 3D cursor as the position for the selected objects to align to.

    OPT_3
    Selection, Use the selected objects as the position for the selected objects to align to.

    OPT_4
    Active, Use the active object as the position for the selected objects to align to.
        :type relative_to: typing.Literal['OPT_1','OPT_2','OPT_3','OPT_4'] | None
        :param align_axis: Align, Align to axis
        :type align_axis: set[typing.Literal['X','Y','Z']] | None
    """

def anim_transforms_to_deltas(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Convert object animation for normal transforms to delta transforms

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def armature_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add an armature object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def assign_property_defaults(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    process_data: bool | None = True,
    process_bones: bool | None = True,
):
    """Assign the current values of custom properties as their defaults, for use as part of the rest pose state in NLA track mixing

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param process_data: Process data properties
    :type process_data: bool | None
    :param process_bones: Process bone properties
    :type process_bones: bool | None
    """

def bake(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "COMBINED",
        "AO",
        "SHADOW",
        "NORMAL",
        "UV",
        "ROUGHNESS",
        "EMIT",
        "ENVIRONMENT",
        "DIFFUSE",
        "GLOSSY",
        "TRANSMISSION",
    ]
    | None = "COMBINED",
    pass_filter: set[
        typing.Literal[
            "NONE",
            "AO",
            "EMIT",
            "DIRECT",
            "INDIRECT",
            "COLOR",
            "DIFFUSE",
            "GLOSSY",
            "TRANSMISSION",
        ]
    ]
    | None = {},
    filepath: str = "",
    width: int | None = 512,
    height: int | None = 512,
    margin: int | None = 16,
    use_selected_to_active: bool | None = False,
    max_ray_distance: float | None = 0.0,
    cage_extrusion: float | None = 0.0,
    cage_object: str = "",
    normal_space: typing.Literal["OBJECT", "TANGENT"] | None = "TANGENT",
    normal_r: typing.Literal["POS_X", "POS_Y", "POS_Z", "NEG_X", "NEG_Y", "NEG_Z"]
    | None = "POS_X",
    normal_g: typing.Literal["POS_X", "POS_Y", "POS_Z", "NEG_X", "NEG_Y", "NEG_Z"]
    | None = "POS_Y",
    normal_b: typing.Literal["POS_X", "POS_Y", "POS_Z", "NEG_X", "NEG_Y", "NEG_Z"]
    | None = "POS_Z",
    save_mode: typing.Literal["INTERNAL", "EXTERNAL"] | None = "INTERNAL",
    use_clear: bool | None = False,
    use_cage: bool | None = False,
    use_split_materials: bool | None = False,
    use_automatic_name: bool | None = False,
    uv_layer: str = "",
):
    """Bake image textures of selected objects

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type, Type of pass to bake, some of them may not be supported by the current render engine
        :type type: typing.Literal['COMBINED','AO','SHADOW','NORMAL','UV','ROUGHNESS','EMIT','ENVIRONMENT','DIFFUSE','GLOSSY','TRANSMISSION'] | None
        :param pass_filter: Pass Filter, Filter to combined, diffuse, glossy, transmission and subsurface passes
        :type pass_filter: set[typing.Literal['NONE','AO','EMIT','DIRECT','INDIRECT','COLOR','DIFFUSE','GLOSSY','TRANSMISSION']] | None
        :param filepath: File Path, Image filepath to use when saving externally
        :type filepath: str
        :param width: Width, Horizontal dimension of the baking map (external only)
        :type width: int | None
        :param height: Height, Vertical dimension of the baking map (external only)
        :type height: int | None
        :param margin: Margin, Extends the baked result as a post process filter
        :type margin: int | None
        :param use_selected_to_active: Selected to Active, Bake shading on the surface of selected objects to the active object
        :type use_selected_to_active: bool | None
        :param max_ray_distance: Max Ray Distance, The maximum ray distance for matching points between the active and selected objects. If zero, there is no limit
        :type max_ray_distance: float | None
        :param cage_extrusion: Cage Extrusion, Inflate the active object by the specified distance for baking. This helps matching to points nearer to the outside of the selected object meshes
        :type cage_extrusion: float | None
        :param cage_object: Cage Object, Object to use as cage, instead of calculating the cage from the active object with cage extrusion
        :type cage_object: str
        :param normal_space: Normal Space, Choose normal space for baking

    OBJECT
    Object, Bake the normals in object space.

    TANGENT
    Tangent, Bake the normals in tangent space.
        :type normal_space: typing.Literal['OBJECT','TANGENT'] | None
        :param normal_r: R, Axis to bake in red channel
        :type normal_r: typing.Literal['POS_X','POS_Y','POS_Z','NEG_X','NEG_Y','NEG_Z'] | None
        :param normal_g: G, Axis to bake in green channel
        :type normal_g: typing.Literal['POS_X','POS_Y','POS_Z','NEG_X','NEG_Y','NEG_Z'] | None
        :param normal_b: B, Axis to bake in blue channel
        :type normal_b: typing.Literal['POS_X','POS_Y','POS_Z','NEG_X','NEG_Y','NEG_Z'] | None
        :param save_mode: Save Mode, Choose how to save the baking map

    INTERNAL
    Internal, Save the baking map in an internal image data-block.

    EXTERNAL
    External, Save the baking map in an external file.
        :type save_mode: typing.Literal['INTERNAL','EXTERNAL'] | None
        :param use_clear: Clear, Clear Images before baking (only for internal saving)
        :type use_clear: bool | None
        :param use_cage: Cage, Cast rays to active object from a cage
        :type use_cage: bool | None
        :param use_split_materials: Split Materials, Split baked maps per material, using material name in output file (external only)
        :type use_split_materials: bool | None
        :param use_automatic_name: Automatic Name, Automatically name the output file with the pass type
        :type use_automatic_name: bool | None
        :param uv_layer: UV Layer, UV layer to override active
        :type uv_layer: str
    """

def bake_image(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Bake image textures of selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def camera_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a camera object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def collection_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add an object to a new collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def collection_instance_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "Collection",
    collection: str | None = "",
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a collection instance

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param name: Name, Collection name to add
        :type name: str
        :param collection: Collection
        :type collection: str | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def collection_link(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection: str | None = "",
):
    """Add an object to an existing collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection
    :type collection: str | None
    """

def collection_objects_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select all objects in collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def collection_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the active object from this collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def collection_unlink(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Unlink the collection from all objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def constraint_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "",
):
    """Add a constraint to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

def constraint_add_with_targets(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "",
):
    """Add a constraint to the active object, with target (where applicable) set to the selected Objects/Bones

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: str | None
    """

def constraints_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear all the constraints for the active Object only

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def constraints_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy constraints to other selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    target: typing.Literal["CURVE", "MESH", "GPENCIL"] | None = "MESH",
    keep_original: bool | None = False,
    angle: float | None = 1.22173,
    thickness: int | None = 5,
    seams: bool | None = False,
    faces: bool | None = True,
    offset: float | None = 0.01,
):
    """Convert selected objects to another type

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param target: Target, Type of object to convert to
    :type target: typing.Literal['CURVE','MESH','GPENCIL'] | None
    :param keep_original: Keep Original, Keep original objects instead of replacing them
    :type keep_original: bool | None
    :param angle: Threshold Angle, Threshold to determine ends of the strokes
    :type angle: float | None
    :param thickness: Thickness
    :type thickness: int | None
    :param seams: Only Seam Edges, Convert only seam edges
    :type seams: bool | None
    :param faces: Export Faces, Export faces as filled strokes
    :type faces: bool | None
    :param offset: Stroke Offset, Offset strokes from fill
    :type offset: float | None
    """

def correctivesmooth_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind base pose in Corrective Smooth modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def data_transfer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_reverse_transfer: bool | None = False,
    use_freeze: bool | None = False,
    data_type: typing.Literal[
        "VGROUP_WEIGHTS",
        "BEVEL_WEIGHT_VERT",
        "SHARP_EDGE",
        "SEAM",
        "CREASE",
        "BEVEL_WEIGHT_EDGE",
        "FREESTYLE_EDGE",
        "CUSTOM_NORMAL",
        "VCOL",
        "UV",
        "SMOOTH",
        "FREESTYLE_FACE",
    ]
    | None = "",
    use_create: bool | None = True,
    vert_mapping: typing.Literal[
        "TOPOLOGY",
        "NEAREST",
        "EDGE_NEAREST",
        "EDGEINTERP_NEAREST",
        "POLY_NEAREST",
        "POLYINTERP_NEAREST",
        "POLYINTERP_VNORPROJ",
    ]
    | None = "NEAREST",
    edge_mapping: typing.Literal[
        "TOPOLOGY", "VERT_NEAREST", "NEAREST", "POLY_NEAREST", "EDGEINTERP_VNORPROJ"
    ]
    | None = "NEAREST",
    loop_mapping: typing.Literal[
        "TOPOLOGY",
        "NEAREST_NORMAL",
        "NEAREST_POLYNOR",
        "NEAREST_POLY",
        "POLYINTERP_NEAREST",
        "POLYINTERP_LNORPROJ",
    ]
    | None = "NEAREST_POLYNOR",
    poly_mapping: typing.Literal["TOPOLOGY", "NEAREST", "NORMAL", "POLYINTERP_PNORPROJ"]
    | None = "NEAREST",
    use_auto_transform: bool | None = False,
    use_object_transform: bool | None = True,
    use_max_distance: bool | None = False,
    max_distance: float | None = 1.0,
    ray_radius: float | None = 0.0,
    islands_precision: float | None = 0.1,
    layers_select_src: typing.Literal["ACTIVE", "ALL", "BONE_SELECT", "BONE_DEFORM"]
    | None = "ACTIVE",
    layers_select_dst: typing.Literal["ACTIVE", "NAME", "INDEX"] | None = "ACTIVE",
    mix_mode: typing.Literal[
        "REPLACE", "ABOVE_THRESHOLD", "BELOW_THRESHOLD", "MIX", "ADD", "SUB", "MUL"
    ]
    | None = "REPLACE",
    mix_factor: float | None = 1.0,
):
    """Transfer data layer(s) (weights, edge sharp, ...) from active to selected meshes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param use_reverse_transfer: Reverse Transfer, Transfer from selected objects to active one
        :type use_reverse_transfer: bool | None
        :param use_freeze: Freeze Operator, Prevent changes to settings to re-run the operator, handy to change several things at once with heavy geometry
        :type use_freeze: bool | None
        :param data_type: Data Type, Which data to transfer

    VGROUP_WEIGHTS
    Vertex Group(s), Transfer active or all vertex groups.

    BEVEL_WEIGHT_VERT
    Bevel Weight, Transfer bevel weights.

    SHARP_EDGE
    Sharp, Transfer sharp mark.

    SEAM
    UV Seam, Transfer UV seam mark.

    CREASE
    Subdivision Crease, Transfer crease values.

    BEVEL_WEIGHT_EDGE
    Bevel Weight, Transfer bevel weights.

    FREESTYLE_EDGE
    Freestyle Mark, Transfer Freestyle edge mark.

    CUSTOM_NORMAL
    Custom Normals, Transfer custom normals.

    VCOL
    VCol, Vertex (face corners) colors.

    UV
    UVs, Transfer UV layers.

    SMOOTH
    Smooth, Transfer flat/smooth mark.

    FREESTYLE_FACE
    Freestyle Mark, Transfer Freestyle face mark.
        :type data_type: typing.Literal['VGROUP_WEIGHTS','BEVEL_WEIGHT_VERT','SHARP_EDGE','SEAM','CREASE','BEVEL_WEIGHT_EDGE','FREESTYLE_EDGE','CUSTOM_NORMAL','VCOL','UV','SMOOTH','FREESTYLE_FACE'] | None
        :param use_create: Create Data, Add data layers on destination meshes if needed
        :type use_create: bool | None
        :param vert_mapping: Vertex Mapping, Method used to map source vertices to destination ones

    TOPOLOGY
    Topology, Copy from identical topology meshes.

    NEAREST
    Nearest Vertex, Copy from closest vertex.

    EDGE_NEAREST
    Nearest Edge Vertex, Copy from closest vertex of closest edge.

    EDGEINTERP_NEAREST
    Nearest Edge Interpolated, Copy from interpolated values of vertices from closest point on closest edge.

    POLY_NEAREST
    Nearest Face Vertex, Copy from closest vertex of closest face.

    POLYINTERP_NEAREST
    Nearest Face Interpolated, Copy from interpolated values of vertices from closest point on closest face.

    POLYINTERP_VNORPROJ
    Projected Face Interpolated, Copy from interpolated values of vertices from point on closest face hit by normal-projection.
        :type vert_mapping: typing.Literal['TOPOLOGY','NEAREST','EDGE_NEAREST','EDGEINTERP_NEAREST','POLY_NEAREST','POLYINTERP_NEAREST','POLYINTERP_VNORPROJ'] | None
        :param edge_mapping: Edge Mapping, Method used to map source edges to destination ones

    TOPOLOGY
    Topology, Copy from identical topology meshes.

    VERT_NEAREST
    Nearest Vertices, Copy from most similar edge (edge which vertices are the closest of destination edge's ones).

    NEAREST
    Nearest Edge, Copy from closest edge (using midpoints).

    POLY_NEAREST
    Nearest Face Edge, Copy from closest edge of closest face (using midpoints).

    EDGEINTERP_VNORPROJ
    Projected Edge Interpolated, Interpolate all source edges hit by the projection of destination one along its own normal (from vertices).
        :type edge_mapping: typing.Literal['TOPOLOGY','VERT_NEAREST','NEAREST','POLY_NEAREST','EDGEINTERP_VNORPROJ'] | None
        :param loop_mapping: Face Corner Mapping, Method used to map source faces' corners to destination ones

    TOPOLOGY
    Topology, Copy from identical topology meshes.

    NEAREST_NORMAL
    Nearest Corner And Best Matching Normal, Copy from nearest corner which has the best matching normal.

    NEAREST_POLYNOR
    Nearest Corner And Best Matching Face Normal, Copy from nearest corner which has the face with the best matching normal to destination corner's face one.

    NEAREST_POLY
    Nearest Corner Of Nearest Face, Copy from nearest corner of nearest polygon.

    POLYINTERP_NEAREST
    Nearest Face Interpolated, Copy from interpolated corners of the nearest source polygon.

    POLYINTERP_LNORPROJ
    Projected Face Interpolated, Copy from interpolated corners of the source polygon hit by corner normal projection.
        :type loop_mapping: typing.Literal['TOPOLOGY','NEAREST_NORMAL','NEAREST_POLYNOR','NEAREST_POLY','POLYINTERP_NEAREST','POLYINTERP_LNORPROJ'] | None
        :param poly_mapping: Face Mapping, Method used to map source faces to destination ones

    TOPOLOGY
    Topology, Copy from identical topology meshes.

    NEAREST
    Nearest Face, Copy from nearest polygon (using center points).

    NORMAL
    Best Normal-Matching, Copy from source polygon which normal is the closest to destination one.

    POLYINTERP_PNORPROJ
    Projected Face Interpolated, Interpolate all source polygons intersected by the projection of destination one along its own normal.
        :type poly_mapping: typing.Literal['TOPOLOGY','NEAREST','NORMAL','POLYINTERP_PNORPROJ'] | None
        :param use_auto_transform: Auto Transform, Automatically compute transformation to get the best possible match between source and destination meshes (WARNING: results will never be as good as manual matching of objects)
        :type use_auto_transform: bool | None
        :param use_object_transform: Object Transform, Evaluate source and destination meshes in global space
        :type use_object_transform: bool | None
        :param use_max_distance: Only Neighbor Geometry, Source elements must be closer than given distance from destination one
        :type use_max_distance: bool | None
        :param max_distance: Max Distance, Maximum allowed distance between source and destination element, for non-topology mappings
        :type max_distance: float | None
        :param ray_radius: Ray Radius, 'Width' of rays (especially useful when raycasting against vertices or edges)
        :type ray_radius: float | None
        :param islands_precision: Islands Precision, Factor controlling precision of islands handling (the higher, the better the results)
        :type islands_precision: float | None
        :param layers_select_src: Source Layers Selection, Which layers to transfer, in case of multi-layers types

    ACTIVE
    Active Layer, Only transfer active data layer.

    ALL
    All Layers, Transfer all data layers.

    BONE_SELECT
    Selected Pose Bones, Transfer all vertex groups used by selected pose bones.

    BONE_DEFORM
    Deform Pose Bones, Transfer all vertex groups used by deform bones.
        :type layers_select_src: typing.Literal['ACTIVE','ALL','BONE_SELECT','BONE_DEFORM'] | None
        :param layers_select_dst: Destination Layers Matching, How to match source and destination layers

    ACTIVE
    Active Layer, Affect active data layer of all targets.

    NAME
    By Name, Match target data layers to affect by name.

    INDEX
    By Order, Match target data layers to affect by order (indices).
        :type layers_select_dst: typing.Literal['ACTIVE','NAME','INDEX'] | None
        :param mix_mode: Mix Mode, How to affect destination elements with source values

    REPLACE
    Replace, Overwrite all elements' data.

    ABOVE_THRESHOLD
    Above Threshold, Only replace destination elements where data is above given threshold (exact behavior depends on data type).

    BELOW_THRESHOLD
    Below Threshold, Only replace destination elements where data is below given threshold (exact behavior depends on data type).

    MIX
    Mix, Mix source value into destination one, using given threshold as factor.

    ADD
    Add, Add source value to destination one, using given threshold as factor.

    SUB
    Subtract, Subtract source value to destination one, using given threshold as factor.

    MUL
    Multiply, Multiply source value to destination one, using given threshold as factor.
        :type mix_mode: typing.Literal['REPLACE','ABOVE_THRESHOLD','BELOW_THRESHOLD','MIX','ADD','SUB','MUL'] | None
        :param mix_factor: Mix Factor, Factor to use when applying data to destination (exact behavior depends on mix mode)
        :type mix_factor: float | None
    """

def datalayout_transfer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    data_type: typing.Literal[
        "VGROUP_WEIGHTS",
        "BEVEL_WEIGHT_VERT",
        "SHARP_EDGE",
        "SEAM",
        "CREASE",
        "BEVEL_WEIGHT_EDGE",
        "FREESTYLE_EDGE",
        "CUSTOM_NORMAL",
        "VCOL",
        "UV",
        "SMOOTH",
        "FREESTYLE_FACE",
    ]
    | None = "",
    use_delete: bool | None = False,
    layers_select_src: typing.Literal["ACTIVE", "ALL", "BONE_SELECT", "BONE_DEFORM"]
    | None = "ACTIVE",
    layers_select_dst: typing.Literal["ACTIVE", "NAME", "INDEX"] | None = "ACTIVE",
):
    """Transfer layout of data layer(s) from active to selected meshes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param modifier: Modifier, Name of the modifier to edit
        :type modifier: str
        :param data_type: Data Type, Which data to transfer

    VGROUP_WEIGHTS
    Vertex Group(s), Transfer active or all vertex groups.

    BEVEL_WEIGHT_VERT
    Bevel Weight, Transfer bevel weights.

    SHARP_EDGE
    Sharp, Transfer sharp mark.

    SEAM
    UV Seam, Transfer UV seam mark.

    CREASE
    Subdivision Crease, Transfer crease values.

    BEVEL_WEIGHT_EDGE
    Bevel Weight, Transfer bevel weights.

    FREESTYLE_EDGE
    Freestyle Mark, Transfer Freestyle edge mark.

    CUSTOM_NORMAL
    Custom Normals, Transfer custom normals.

    VCOL
    VCol, Vertex (face corners) colors.

    UV
    UVs, Transfer UV layers.

    SMOOTH
    Smooth, Transfer flat/smooth mark.

    FREESTYLE_FACE
    Freestyle Mark, Transfer Freestyle face mark.
        :type data_type: typing.Literal['VGROUP_WEIGHTS','BEVEL_WEIGHT_VERT','SHARP_EDGE','SEAM','CREASE','BEVEL_WEIGHT_EDGE','FREESTYLE_EDGE','CUSTOM_NORMAL','VCOL','UV','SMOOTH','FREESTYLE_FACE'] | None
        :param use_delete: Exact Match, Also delete some data layers from destination if necessary, so that it matches exactly source
        :type use_delete: bool | None
        :param layers_select_src: Source Layers Selection, Which layers to transfer, in case of multi-layers types

    ACTIVE
    Active Layer, Only transfer active data layer.

    ALL
    All Layers, Transfer all data layers.

    BONE_SELECT
    Selected Pose Bones, Transfer all vertex groups used by selected pose bones.

    BONE_DEFORM
    Deform Pose Bones, Transfer all vertex groups used by deform bones.
        :type layers_select_src: typing.Literal['ACTIVE','ALL','BONE_SELECT','BONE_DEFORM'] | None
        :param layers_select_dst: Destination Layers Matching, How to match source and destination layers

    ACTIVE
    Active Layer, Affect active data layer of all targets.

    NAME
    By Name, Match target data layers to affect by name.

    INDEX
    By Order, Match target data layers to affect by order (indices).
        :type layers_select_dst: typing.Literal['ACTIVE','NAME','INDEX'] | None
    """

def delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_global: bool | None = False,
    confirm: bool | None = True,
):
    """Delete selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_global: Delete Globally, Remove object from all scenes
    :type use_global: bool | None
    :param confirm: Confirm, Prompt for confirmation
    :type confirm: bool | None
    """

def drop_named_image(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    relative_path: bool | None = True,
    name: str = "",
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add an empty image type to scene with data

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: Filepath, Path to image file
        :type filepath: str
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | None
        :param name: Name, Image name to assign
        :type name: str
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def drop_named_material(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "Material",
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Material name to assign
    :type name: str
    """

def duplicate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    linked: bool | None = False,
    mode: typing.Literal[
        "INIT",
        "DUMMY",
        "TRANSLATION",
        "ROTATION",
        "RESIZE",
        "SKIN_RESIZE",
        "TOSPHERE",
        "SHEAR",
        "BEND",
        "SHRINKFATTEN",
        "TILT",
        "TRACKBALL",
        "PUSHPULL",
        "CREASE",
        "MIRROR",
        "BONE_SIZE",
        "BONE_ENVELOPE",
        "BONE_ENVELOPE_DIST",
        "CURVE_SHRINKFATTEN",
        "MASK_SHRINKFATTEN",
        "GPENCIL_SHRINKFATTEN",
        "BONE_ROLL",
        "TIME_TRANSLATE",
        "TIME_SLIDE",
        "TIME_SCALE",
        "TIME_EXTEND",
        "BAKE_TIME",
        "BWEIGHT",
        "ALIGN",
        "EDGESLIDE",
        "SEQSLIDE",
        "GPENCIL_OPACITY",
    ]
    | None = "TRANSLATION",
):
    """Duplicate selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param linked: Linked, Duplicate object but not object data, linking to the original data
    :type linked: bool | None
    :param mode: Mode
    :type mode: typing.Literal['INIT','DUMMY','TRANSLATION','ROTATION','RESIZE','SKIN_RESIZE','TOSPHERE','SHEAR','BEND','SHRINKFATTEN','TILT','TRACKBALL','PUSHPULL','CREASE','MIRROR','BONE_SIZE','BONE_ENVELOPE','BONE_ENVELOPE_DIST','CURVE_SHRINKFATTEN','MASK_SHRINKFATTEN','GPENCIL_SHRINKFATTEN','BONE_ROLL','TIME_TRANSLATE','TIME_SLIDE','TIME_SCALE','TIME_EXTEND','BAKE_TIME','BWEIGHT','ALIGN','EDGESLIDE','SEQSLIDE','GPENCIL_OPACITY'] | None
    """

def duplicate_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    OBJECT_OT_duplicate: duplicate | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
):
    """Duplicate selected objects and move them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param OBJECT_OT_duplicate: Duplicate Objects, Duplicate selected objects
    :type OBJECT_OT_duplicate: duplicate | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def duplicate_move_linked(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    OBJECT_OT_duplicate: duplicate | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
):
    """Duplicate selected objects and move them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param OBJECT_OT_duplicate: Duplicate Objects, Duplicate selected objects
    :type OBJECT_OT_duplicate: duplicate | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def duplicates_make_real(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_base_parent: bool | None = False,
    use_hierarchy: bool | None = False,
):
    """Make instanced objects attached to this object real

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_base_parent: Parent, Parent newly created objects to the original duplicator
    :type use_base_parent: bool | None
    :param use_hierarchy: Keep Hierarchy, Maintain parent child relationships
    :type use_hierarchy: bool | None
    """

def editmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle object's editmode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def effector_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "FORCE",
        "WIND",
        "VORTEX",
        "MAGNET",
        "HARMONIC",
        "CHARGE",
        "LENNARDJ",
        "TEXTURE",
        "GUIDE",
        "BOID",
        "TURBULENCE",
        "DRAG",
        "FLUID",
    ]
    | None = "FORCE",
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add an empty object with a physics effector to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type
        :type type: typing.Literal['FORCE','WIND','VORTEX','MAGNET','HARMONIC','CHARGE','LENNARDJ','TEXTURE','GUIDE','BOID','TURBULENCE','DRAG','FLUID'] | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def empty_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "PLAIN_AXES",
        "ARROWS",
        "SINGLE_ARROW",
        "CIRCLE",
        "CUBE",
        "SPHERE",
        "CONE",
        "IMAGE",
    ]
    | None = "PLAIN_AXES",
    radius: float | None = 1.0,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add an empty object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type
        :type type: typing.Literal['PLAIN_AXES','ARROWS','SINGLE_ARROW','CIRCLE','CUBE','SPHERE','CONE','IMAGE'] | None
        :param radius: Radius
        :type radius: float | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def explode_refresh(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Refresh data in the Explode modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def face_map_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new face map to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def face_map_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Assign faces to a face map

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def face_map_deselect(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Deselect faces belonging to a face map

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def face_map_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Move the active face map up/down in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to move, UP or DOWN
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def face_map_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove a face map from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def face_map_remove_from(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove faces from a face map

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def face_map_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select faces belonging to a face map

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def forcefield_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle object's force field

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def gpencil_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    type: typing.Literal["EMPTY", "STROKE", "MONKEY"] | None = "EMPTY",
):
    """Add a Grease Pencil object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
        :param type: Type

    EMPTY
    Blank, Create an empty grease pencil object.

    STROKE
    Stroke, Create a simple stroke with basic colors.

    MONKEY
    Monkey, Construct a Suzanne grease pencil object.
        :type type: typing.Literal['EMPTY','STROKE','MONKEY'] | None
    """

def gpencil_modifier_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "DATA_TRANSFER",
        "MESH_CACHE",
        "MESH_SEQUENCE_CACHE",
        "NORMAL_EDIT",
        "WEIGHTED_NORMAL",
        "UV_PROJECT",
        "UV_WARP",
        "VERTEX_WEIGHT_EDIT",
        "VERTEX_WEIGHT_MIX",
        "VERTEX_WEIGHT_PROXIMITY",
        "ARRAY",
        "BEVEL",
        "BOOLEAN",
        "BUILD",
        "DECIMATE",
        "EDGE_SPLIT",
        "MASK",
        "MIRROR",
        "MULTIRES",
        "REMESH",
        "SCREW",
        "SKIN",
        "SOLIDIFY",
        "SUBSURF",
        "TRIANGULATE",
        "WELD",
        "WIREFRAME",
        "ARMATURE",
        "CAST",
        "CURVE",
        "DISPLACE",
        "HOOK",
        "LAPLACIANDEFORM",
        "LATTICE",
        "MESH_DEFORM",
        "SHRINKWRAP",
        "SIMPLE_DEFORM",
        "SMOOTH",
        "CORRECTIVE_SMOOTH",
        "LAPLACIANSMOOTH",
        "SURFACE_DEFORM",
        "WARP",
        "WAVE",
        "CLOTH",
        "COLLISION",
        "DYNAMIC_PAINT",
        "EXPLODE",
        "FLUID",
        "OCEAN",
        "PARTICLE_INSTANCE",
        "PARTICLE_SYSTEM",
        "SOFT_BODY",
        "SURFACE",
        "SIMULATION",
    ]
    | None = "CURVE",
):
    """Add a procedural operation/effect to the active grease pencil object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    DATA_TRANSFER
    Data Transfer, Transfer several types of data (vertex groups, UV maps, vertex colors, custom normals) from one mesh to another.

    MESH_CACHE
    Mesh Cache, Deform the mesh using an external frame-by-frame vertex transform cache.

    MESH_SEQUENCE_CACHE
    Mesh Sequence Cache, Deform the mesh or curve using an external mesh cache in Alembic format.

    NORMAL_EDIT
    Normal Edit, Modify the direction of the surface normals.

    WEIGHTED_NORMAL
    Weighted Normal, Modify the direction of the surface normals using a weighting method.

    UV_PROJECT
    UV Project, Project the UV map coordinates from the negative Z axis of another object.

    UV_WARP
    UV Warp, Transform the UV map using the difference between two objects.

    VERTEX_WEIGHT_EDIT
    Vertex Weight Edit, Modify of the weights of a vertex group.

    VERTEX_WEIGHT_MIX
    Vertex Weight Mix, Mix the weights of two vertex groups.

    VERTEX_WEIGHT_PROXIMITY
    Vertex Weight Proximity, Set the vertex group weights based on the distance to another target object.

    ARRAY
    Array, Create copies of the shape with offsets.

    BEVEL
    Bevel, Generate sloped corners by adding geometry to the mesh's edges or vertices.

    BOOLEAN
    Boolean, Use another shape to cut, combine or perform a difference operation.

    BUILD
    Build, Cause the faces of the mesh object to appear or disappear one after the other over time.

    DECIMATE
    Decimate, Reduce the geometry density.

    EDGE_SPLIT
    Edge Split, Split away joined faces at the edges.

    MASK
    Mask, Dynamically hide vertices based on a vertex group or armature.

    MIRROR
    Mirror, Mirror along the local X, Y and/or Z axes, over the object origin.

    MULTIRES
    Multiresolution, Subdivide the mesh in a way that allows editing the higher subdivision levels.

    REMESH
    Remesh, Generate new mesh topology based on the current shape.

    SCREW
    Screw, Lathe around an axis, treating the input mesh as a profile.

    SKIN
    Skin, Create a solid shape from vertices and edges, using the vertex radius to define the thickness.

    SOLIDIFY
    Solidify,  Make the surface thick.

    SUBSURF
    Subdivision Surface, Split the faces into smaller parts, giving it a smoother appearance.

    TRIANGULATE
    Triangulate, Convert all polygons to triangles.

    WELD
    Weld, Find groups of vertices closer then dist and merges them together.

    WIREFRAME
    Wireframe, Convert faces into thickened edges.

    ARMATURE
    Armature, Deform the shape using an armature object.

    CAST
    Cast, Shift the shape towards a predefined primitive.

    CURVE
    Curve, Bend the mesh using a curve object.

    DISPLACE
    Displace, Offset vertices based on a texture.

    HOOK
    Hook, Deform specific points using another object.

    LAPLACIANDEFORM
    Laplacian Deform, Deform based a series of anchor points.

    LATTICE
    Lattice, Deform using the shape of a lattice object.

    MESH_DEFORM
    Mesh Deform, Deform using a different mesh, which acts as a deformation cage.

    SHRINKWRAP
    Shrinkwrap, Project the shape onto another object.

    SIMPLE_DEFORM
    Simple Deform, Deform the shape by twisting, bending, tapering or stretching.

    SMOOTH
    Smooth, Smooth the mesh by flattening the angles between adjacent faces.

    CORRECTIVE_SMOOTH
    Smooth Corrective, Smooth the mesh while still preserving the volume.

    LAPLACIANSMOOTH
    Smooth Laplacian, Reduce the noise on a mesh surface with minimal changes to its shape.

    SURFACE_DEFORM
    Surface Deform, Transfer motion from another mesh.

    WARP
    Warp, Warp parts of a mesh to a new location in a very flexible way thanks to 2 specified objects.

    WAVE
    Wave, Adds a ripple-like motion to an object’s geometry.

    CLOTH
    Cloth.

    COLLISION
    Collision.

    DYNAMIC_PAINT
    Dynamic Paint.

    EXPLODE
    Explode, Break apart the mesh faces and let them follow particles.

    FLUID
    Fluid.

    OCEAN
    Ocean, Generate a moving ocean surface.

    PARTICLE_INSTANCE
    Particle Instance.

    PARTICLE_SYSTEM
    Particle System, Spawn particles from the shape.

    SOFT_BODY
    Soft Body.

    SURFACE
    Surface.

    SIMULATION
    Simulation.
        :type type: typing.Literal['DATA_TRANSFER','MESH_CACHE','MESH_SEQUENCE_CACHE','NORMAL_EDIT','WEIGHTED_NORMAL','UV_PROJECT','UV_WARP','VERTEX_WEIGHT_EDIT','VERTEX_WEIGHT_MIX','VERTEX_WEIGHT_PROXIMITY','ARRAY','BEVEL','BOOLEAN','BUILD','DECIMATE','EDGE_SPLIT','MASK','MIRROR','MULTIRES','REMESH','SCREW','SKIN','SOLIDIFY','SUBSURF','TRIANGULATE','WELD','WIREFRAME','ARMATURE','CAST','CURVE','DISPLACE','HOOK','LAPLACIANDEFORM','LATTICE','MESH_DEFORM','SHRINKWRAP','SIMPLE_DEFORM','SMOOTH','CORRECTIVE_SMOOTH','LAPLACIANSMOOTH','SURFACE_DEFORM','WARP','WAVE','CLOTH','COLLISION','DYNAMIC_PAINT','EXPLODE','FLUID','OCEAN','PARTICLE_INSTANCE','PARTICLE_SYSTEM','SOFT_BODY','SURFACE','SIMULATION'] | None
    """

def gpencil_modifier_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    apply_as: typing.Literal["DATA", "SHAPE"] | None = "DATA",
    modifier: str = "",
    report: bool | None = False,
):
    """Apply modifier and remove from the stack

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param apply_as: Apply as, How to apply the modifier to the geometry

    DATA
    Object Data, Apply modifier to the object's data.

    SHAPE
    New Shape, Apply deform-only modifier to a new shape on this object.
        :type apply_as: typing.Literal['DATA','SHAPE'] | None
        :param modifier: Modifier, Name of the modifier to edit
        :type modifier: str
        :param report: Report, Create a notification after the operation
        :type report: bool | None
    """

def gpencil_modifier_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Duplicate modifier at the same position in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def gpencil_modifier_move_down(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Move modifier down in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def gpencil_modifier_move_to_index(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    index: int | None = 0,
):
    """Change the modifier's position in the list so it evaluates after the set number of others

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param index: Index, The index to move the modifier to
    :type index: int | None
    """

def gpencil_modifier_move_up(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Move modifier up in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def gpencil_modifier_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    report: bool | None = False,
):
    """Remove a modifier from the active grease pencil object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    """

def hair_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a hair object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def hide_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection_index: int | None = -1,
    toggle: bool | None = False,
):
    """Show only objects in collection (Shift to extend)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection_index: Collection Index, Index of the collection to change visibility
    :type collection_index: int | None
    :param toggle: Toggle, Toggle visibility
    :type toggle: bool | None
    """

def hide_render_clear_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reveal all render objects by setting the hide render flag

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def hide_view_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    select: bool | None = True,
):
    """Reveal temporarily hidden objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param select: Select
    :type select: bool | None
    """

def hide_view_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    unselected: bool | None = False,
):
    """Temporarily hide objects from the viewport

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param unselected: Unselected, Hide unselected rather than selected objects
    :type unselected: bool | None
    """

def hook_add_newob(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Hook selected vertices to a newly created object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def hook_add_selob(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_bone: bool | None = False,
):
    """Hook selected vertices to the first selected object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_bone: Active Bone, Assign the hook to the hook objects active bone
    :type use_bone: bool | None
    """

def hook_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Assign the selected vertices to a hook

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to assign to
    :type modifier: str | None
    """

def hook_recenter(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Set hook center to cursor position

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to assign to
    :type modifier: str | None
    """

def hook_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Remove a hook from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to remove
    :type modifier: str | None
    """

def hook_reset(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Recalculate and clear offset transformation

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to assign to
    :type modifier: str | None
    """

def hook_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str | None = "",
):
    """Select affected vertices on mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Modifier number to remove
    :type modifier: str | None
    """

def instance_offset_from_cursor(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set offset used for collection instances based on cursor position

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def isolate_type_render(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Hide unselected render objects of same type as active by setting the hide render flag

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def join(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Join selected objects into active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def join_shapes(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy the current resulting shape of another selected object to this one

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def join_uvs(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Transfer UV Maps from active to selected objects (needs matching geometry)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def laplaciandeform_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind mesh to system in laplacian deform modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def light_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["POINT", "SUN", "SPOT", "AREA"] | None = "POINT",
    radius: float | None = 1.0,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a light object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    POINT
    Point, Omnidirectional point light source.

    SUN
    Sun, Constant direction parallel ray light source.

    SPOT
    Spot, Directional cone light source.

    AREA
    Area, Directional area light source.
        :type type: typing.Literal['POINT','SUN','SPOT','AREA'] | None
        :param radius: Radius
        :type radius: float | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def lightprobe_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["CUBEMAP", "PLANAR", "GRID"] | None = "CUBEMAP",
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a light probe object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    CUBEMAP
    Reflection Cubemap, Reflection probe with spherical or cubic attenuation.

    PLANAR
    Reflection Plane, Planar reflection probe.

    GRID
    Irradiance Volume, Irradiance probe to capture diffuse indirect lighting.
        :type type: typing.Literal['CUBEMAP','PLANAR','GRID'] | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def link_to_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection_index: int | None = -1,
    is_new: bool | None = False,
    new_collection_name: str = "",
):
    """Link objects to a collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection_index: Collection Index, Index of the collection to move to
    :type collection_index: int | None
    :param is_new: New, Move objects to a new collection
    :type is_new: bool | None
    :param new_collection_name: Name, Name of the newly added collection
    :type new_collection_name: str
    """

def load_background_image(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    filter_image: bool | None = True,
    filter_folder: bool | None = True,
    view_align: bool | None = True,
):
    """Add a reference image into the background behind objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    :param filter_image: filter_image
    :type filter_image: bool | None
    :param filter_folder: filter_folder
    :type filter_folder: bool | None
    :param view_align: Align to view
    :type view_align: bool | None
    """

def load_reference_image(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    filter_image: bool | None = True,
    filter_folder: bool | None = True,
    view_align: bool | None = True,
):
    """Add a reference image into the scene between objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str
    :param filter_image: filter_image
    :type filter_image: bool | None
    :param filter_folder: filter_folder
    :type filter_folder: bool | None
    :param view_align: Align to view
    :type view_align: bool | None
    """

def location_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    clear_delta: bool | None = False,
):
    """Clear the object's location

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param clear_delta: Clear Delta, Clear delta location in addition to clearing the normal location transform
    :type clear_delta: bool | None
    """

def make_dupli_face(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Convert objects into instanced faces

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def make_links_data(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "OBDATA",
        "MATERIAL",
        "ANIMATION",
        "GROUPS",
        "DUPLICOLLECTION",
        "MODIFIERS",
        "FONTS",
    ]
    | None = "OBDATA",
):
    """Apply active object links to other selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['OBDATA','MATERIAL','ANIMATION','GROUPS','DUPLICOLLECTION','MODIFIERS','FONTS'] | None
    """

def make_links_scene(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    scene: str | None = "",
):
    """Link selection to another scene

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param scene: Scene
    :type scene: str | None
    """

def make_local(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "SELECT_OBJECT", "SELECT_OBDATA", "SELECT_OBDATA_MATERIAL", "ALL"
    ]
    | None = "SELECT_OBJECT",
):
    """Make library linked data-blocks local to this file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['SELECT_OBJECT','SELECT_OBDATA','SELECT_OBDATA_MATERIAL','ALL'] | None
    """

def make_override_library(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection: str | None = "DEFAULT",
):
    """Make a local override of this library linked data-block

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Override Collection, Name of directly linked collection containing the selected object, to make an override from
    :type collection: str | None
    """

def make_single_user(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["SELECTED_OBJECTS", "ALL"] | None = "SELECTED_OBJECTS",
    object: bool | None = False,
    obdata: bool | None = False,
    material: bool | None = False,
    animation: bool | None = False,
):
    """Make linked data local to each object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['SELECTED_OBJECTS','ALL'] | None
    :param object: Object, Make single user objects
    :type object: bool | None
    :param obdata: Object Data, Make single user object data
    :type obdata: bool | None
    :param material: Materials, Make materials local to each data-block
    :type material: bool | None
    :param animation: Object Animation, Make animation data local to each object
    :type animation: bool | None
    """

def material_slot_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_slot_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Assign active material slot to selection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_slot_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy material to selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_slot_deselect(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Deselect by active material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_slot_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Move the active material up/down in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to move the active material towards
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def material_slot_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the selected material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_slot_remove_unused(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove unused material slots

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_slot_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select by active material slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def meshdeform_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind mesh to cage in mesh deform modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def metaball_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["BALL", "CAPSULE", "PLANE", "ELLIPSOID", "CUBE"]
    | None = "BALL",
    radius: float | None = 2.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add an metaball object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Primitive
        :type type: typing.Literal['BALL','CAPSULE','PLANE','ELLIPSOID','CUBE'] | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def mode_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal[
        "OBJECT",
        "EDIT",
        "POSE",
        "SCULPT",
        "VERTEX_PAINT",
        "WEIGHT_PAINT",
        "TEXTURE_PAINT",
        "PARTICLE_EDIT",
        "EDIT_GPENCIL",
        "SCULPT_GPENCIL",
        "PAINT_GPENCIL",
        "VERTEX_GPENCIL",
        "WEIGHT_GPENCIL",
    ]
    | None = "OBJECT",
    toggle: bool | None = False,
):
    """Sets the object interaction mode

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode

    OBJECT
    Object Mode.

    EDIT
    Edit Mode.

    POSE
    Pose Mode.

    SCULPT
    Sculpt Mode.

    VERTEX_PAINT
    Vertex Paint.

    WEIGHT_PAINT
    Weight Paint.

    TEXTURE_PAINT
    Texture Paint.

    PARTICLE_EDIT
    Particle Edit.

    EDIT_GPENCIL
    Edit Mode, Edit Grease Pencil Strokes.

    SCULPT_GPENCIL
    Sculpt Mode, Sculpt Grease Pencil Strokes.

    PAINT_GPENCIL
    Draw, Paint Grease Pencil Strokes.

    VERTEX_GPENCIL
    Vertex Paint, Grease Pencil Vertex Paint Strokes.

    WEIGHT_GPENCIL
    Weight Paint, Grease Pencil Weight Paint Strokes.
        :type mode: typing.Literal['OBJECT','EDIT','POSE','SCULPT','VERTEX_PAINT','WEIGHT_PAINT','TEXTURE_PAINT','PARTICLE_EDIT','EDIT_GPENCIL','SCULPT_GPENCIL','PAINT_GPENCIL','VERTEX_GPENCIL','WEIGHT_GPENCIL'] | None
        :param toggle: Toggle
        :type toggle: bool | None
    """

def mode_set_with_submode(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal[
        "OBJECT",
        "EDIT",
        "POSE",
        "SCULPT",
        "VERTEX_PAINT",
        "WEIGHT_PAINT",
        "TEXTURE_PAINT",
        "PARTICLE_EDIT",
        "EDIT_GPENCIL",
        "SCULPT_GPENCIL",
        "PAINT_GPENCIL",
        "VERTEX_GPENCIL",
        "WEIGHT_GPENCIL",
    ]
    | None = "OBJECT",
    toggle: bool | None = False,
    mesh_select_mode: set[typing.Literal["VERT", "EDGE", "FACE"]] | None = {},
):
    """Sets the object interaction mode

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode

    OBJECT
    Object Mode.

    EDIT
    Edit Mode.

    POSE
    Pose Mode.

    SCULPT
    Sculpt Mode.

    VERTEX_PAINT
    Vertex Paint.

    WEIGHT_PAINT
    Weight Paint.

    TEXTURE_PAINT
    Texture Paint.

    PARTICLE_EDIT
    Particle Edit.

    EDIT_GPENCIL
    Edit Mode, Edit Grease Pencil Strokes.

    SCULPT_GPENCIL
    Sculpt Mode, Sculpt Grease Pencil Strokes.

    PAINT_GPENCIL
    Draw, Paint Grease Pencil Strokes.

    VERTEX_GPENCIL
    Vertex Paint, Grease Pencil Vertex Paint Strokes.

    WEIGHT_GPENCIL
    Weight Paint, Grease Pencil Weight Paint Strokes.
        :type mode: typing.Literal['OBJECT','EDIT','POSE','SCULPT','VERTEX_PAINT','WEIGHT_PAINT','TEXTURE_PAINT','PARTICLE_EDIT','EDIT_GPENCIL','SCULPT_GPENCIL','PAINT_GPENCIL','VERTEX_GPENCIL','WEIGHT_GPENCIL'] | None
        :param toggle: Toggle
        :type toggle: bool | None
        :param mesh_select_mode: Mesh Mode

    VERT
    Vertex, Vertex selection mode.

    EDGE
    Edge, Edge selection mode.

    FACE
    Face, Face selection mode.
        :type mesh_select_mode: set[typing.Literal['VERT','EDGE','FACE']] | None
    """

def modifier_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "DATA_TRANSFER",
        "MESH_CACHE",
        "MESH_SEQUENCE_CACHE",
        "NORMAL_EDIT",
        "WEIGHTED_NORMAL",
        "UV_PROJECT",
        "UV_WARP",
        "VERTEX_WEIGHT_EDIT",
        "VERTEX_WEIGHT_MIX",
        "VERTEX_WEIGHT_PROXIMITY",
        "ARRAY",
        "BEVEL",
        "BOOLEAN",
        "BUILD",
        "DECIMATE",
        "EDGE_SPLIT",
        "MASK",
        "MIRROR",
        "MULTIRES",
        "REMESH",
        "SCREW",
        "SKIN",
        "SOLIDIFY",
        "SUBSURF",
        "TRIANGULATE",
        "WELD",
        "WIREFRAME",
        "ARMATURE",
        "CAST",
        "CURVE",
        "DISPLACE",
        "HOOK",
        "LAPLACIANDEFORM",
        "LATTICE",
        "MESH_DEFORM",
        "SHRINKWRAP",
        "SIMPLE_DEFORM",
        "SMOOTH",
        "CORRECTIVE_SMOOTH",
        "LAPLACIANSMOOTH",
        "SURFACE_DEFORM",
        "WARP",
        "WAVE",
        "CLOTH",
        "COLLISION",
        "DYNAMIC_PAINT",
        "EXPLODE",
        "FLUID",
        "OCEAN",
        "PARTICLE_INSTANCE",
        "PARTICLE_SYSTEM",
        "SOFT_BODY",
        "SURFACE",
        "SIMULATION",
    ]
    | None = "SUBSURF",
):
    """Add a procedural operation/effect to the active object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    DATA_TRANSFER
    Data Transfer, Transfer several types of data (vertex groups, UV maps, vertex colors, custom normals) from one mesh to another.

    MESH_CACHE
    Mesh Cache, Deform the mesh using an external frame-by-frame vertex transform cache.

    MESH_SEQUENCE_CACHE
    Mesh Sequence Cache, Deform the mesh or curve using an external mesh cache in Alembic format.

    NORMAL_EDIT
    Normal Edit, Modify the direction of the surface normals.

    WEIGHTED_NORMAL
    Weighted Normal, Modify the direction of the surface normals using a weighting method.

    UV_PROJECT
    UV Project, Project the UV map coordinates from the negative Z axis of another object.

    UV_WARP
    UV Warp, Transform the UV map using the difference between two objects.

    VERTEX_WEIGHT_EDIT
    Vertex Weight Edit, Modify of the weights of a vertex group.

    VERTEX_WEIGHT_MIX
    Vertex Weight Mix, Mix the weights of two vertex groups.

    VERTEX_WEIGHT_PROXIMITY
    Vertex Weight Proximity, Set the vertex group weights based on the distance to another target object.

    ARRAY
    Array, Create copies of the shape with offsets.

    BEVEL
    Bevel, Generate sloped corners by adding geometry to the mesh's edges or vertices.

    BOOLEAN
    Boolean, Use another shape to cut, combine or perform a difference operation.

    BUILD
    Build, Cause the faces of the mesh object to appear or disappear one after the other over time.

    DECIMATE
    Decimate, Reduce the geometry density.

    EDGE_SPLIT
    Edge Split, Split away joined faces at the edges.

    MASK
    Mask, Dynamically hide vertices based on a vertex group or armature.

    MIRROR
    Mirror, Mirror along the local X, Y and/or Z axes, over the object origin.

    MULTIRES
    Multiresolution, Subdivide the mesh in a way that allows editing the higher subdivision levels.

    REMESH
    Remesh, Generate new mesh topology based on the current shape.

    SCREW
    Screw, Lathe around an axis, treating the input mesh as a profile.

    SKIN
    Skin, Create a solid shape from vertices and edges, using the vertex radius to define the thickness.

    SOLIDIFY
    Solidify,  Make the surface thick.

    SUBSURF
    Subdivision Surface, Split the faces into smaller parts, giving it a smoother appearance.

    TRIANGULATE
    Triangulate, Convert all polygons to triangles.

    WELD
    Weld, Find groups of vertices closer then dist and merges them together.

    WIREFRAME
    Wireframe, Convert faces into thickened edges.

    ARMATURE
    Armature, Deform the shape using an armature object.

    CAST
    Cast, Shift the shape towards a predefined primitive.

    CURVE
    Curve, Bend the mesh using a curve object.

    DISPLACE
    Displace, Offset vertices based on a texture.

    HOOK
    Hook, Deform specific points using another object.

    LAPLACIANDEFORM
    Laplacian Deform, Deform based a series of anchor points.

    LATTICE
    Lattice, Deform using the shape of a lattice object.

    MESH_DEFORM
    Mesh Deform, Deform using a different mesh, which acts as a deformation cage.

    SHRINKWRAP
    Shrinkwrap, Project the shape onto another object.

    SIMPLE_DEFORM
    Simple Deform, Deform the shape by twisting, bending, tapering or stretching.

    SMOOTH
    Smooth, Smooth the mesh by flattening the angles between adjacent faces.

    CORRECTIVE_SMOOTH
    Smooth Corrective, Smooth the mesh while still preserving the volume.

    LAPLACIANSMOOTH
    Smooth Laplacian, Reduce the noise on a mesh surface with minimal changes to its shape.

    SURFACE_DEFORM
    Surface Deform, Transfer motion from another mesh.

    WARP
    Warp, Warp parts of a mesh to a new location in a very flexible way thanks to 2 specified objects.

    WAVE
    Wave, Adds a ripple-like motion to an object’s geometry.

    CLOTH
    Cloth.

    COLLISION
    Collision.

    DYNAMIC_PAINT
    Dynamic Paint.

    EXPLODE
    Explode, Break apart the mesh faces and let them follow particles.

    FLUID
    Fluid.

    OCEAN
    Ocean, Generate a moving ocean surface.

    PARTICLE_INSTANCE
    Particle Instance.

    PARTICLE_SYSTEM
    Particle System, Spawn particles from the shape.

    SOFT_BODY
    Soft Body.

    SURFACE
    Surface.

    SIMULATION
    Simulation.
        :type type: typing.Literal['DATA_TRANSFER','MESH_CACHE','MESH_SEQUENCE_CACHE','NORMAL_EDIT','WEIGHTED_NORMAL','UV_PROJECT','UV_WARP','VERTEX_WEIGHT_EDIT','VERTEX_WEIGHT_MIX','VERTEX_WEIGHT_PROXIMITY','ARRAY','BEVEL','BOOLEAN','BUILD','DECIMATE','EDGE_SPLIT','MASK','MIRROR','MULTIRES','REMESH','SCREW','SKIN','SOLIDIFY','SUBSURF','TRIANGULATE','WELD','WIREFRAME','ARMATURE','CAST','CURVE','DISPLACE','HOOK','LAPLACIANDEFORM','LATTICE','MESH_DEFORM','SHRINKWRAP','SIMPLE_DEFORM','SMOOTH','CORRECTIVE_SMOOTH','LAPLACIANSMOOTH','SURFACE_DEFORM','WARP','WAVE','CLOTH','COLLISION','DYNAMIC_PAINT','EXPLODE','FLUID','OCEAN','PARTICLE_INSTANCE','PARTICLE_SYSTEM','SOFT_BODY','SURFACE','SIMULATION'] | None
    """

def modifier_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    report: bool | None = False,
):
    """Apply modifier and remove from the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    """

def modifier_apply_as_shapekey(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    keep_modifier: bool | None = False,
    modifier: str = "",
    report: bool | None = False,
):
    """Apply modifier as a new shapekey and remove from the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param keep_modifier: Keep Modifier, Do not remove the modifier from stack
    :type keep_modifier: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    """

def modifier_convert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Convert particles to a mesh object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def modifier_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Duplicate modifier at the same position in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def modifier_move_down(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Move modifier down in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def modifier_move_to_index(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    index: int | None = 0,
):
    """Change the modifier's index in the stack so it evaluates after the set number of others

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param index: Index, The index to move the modifier to
    :type index: int | None
    """

def modifier_move_up(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Move modifier up in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def modifier_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    report: bool | None = False,
):
    """Remove a modifier from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    """

def move_to_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection_index: int | None = -1,
    is_new: bool | None = False,
    new_collection_name: str = "",
):
    """Move objects to a collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection_index: Collection Index, Index of the collection to move to
    :type collection_index: int | None
    :param is_new: New, Move objects to a new collection
    :type is_new: bool | None
    :param new_collection_name: Name, Name of the newly added collection
    :type new_collection_name: str
    """

def multires_base_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Modify the base mesh to conform to the displaced mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def multires_external_pack(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Pack displacements from an external file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def multires_external_save(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
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
    filter_btx: bool | None = True,
    filter_collada: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    modifier: str = "",
):
    """Save displacements to an external file

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
        :param modifier: Modifier, Name of the modifier to edit
        :type modifier: str
    """

def multires_higher_levels_delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Deletes the higher resolution mesh, potential loss of detail

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def multires_rebuild_subdiv(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Rebuilds all possible subdivisions levels to generate a lower resolution base mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def multires_reshape(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Copy vertex coordinates from other object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def multires_subdivide(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    mode: typing.Literal["CATMULL_CLARK", "SIMPLE", "LINEAR"] | None = "CATMULL_CLARK",
):
    """Add a new level of subdivision

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param modifier: Modifier, Name of the modifier to edit
        :type modifier: str
        :param mode: Subdivision Mode, How the mesh is going to be subdivided to create a new level

    CATMULL_CLARK
    Catmull-Clark, Create a new level using Catmull-Clark subdivisions.

    SIMPLE
    Simple, Create a new level using simple subdivisions.

    LINEAR
    Linear, Create a new level using linear interpolation of the sculpted displacement.
        :type mode: typing.Literal['CATMULL_CLARK','SIMPLE','LINEAR'] | None
    """

def multires_unsubdivide(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Rebuild a lower subdivision level of the current base mesh

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def ocean_bake(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
    free: bool | None = False,
):
    """Bake an image sequence of ocean data

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    :param free: Free, Free the bake, rather than generating it
    :type free: bool | None
    """

def origin_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear the object's origin

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def origin_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "GEOMETRY_ORIGIN",
        "ORIGIN_GEOMETRY",
        "ORIGIN_CURSOR",
        "ORIGIN_CENTER_OF_MASS",
        "ORIGIN_CENTER_OF_VOLUME",
    ]
    | None = "GEOMETRY_ORIGIN",
    center: typing.Literal["MEDIAN", "BOUNDS"] | None = "MEDIAN",
):
    """Set the object's origin, by either moving the data, or set to center of data, or use 3D cursor

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    GEOMETRY_ORIGIN
    Geometry to Origin, Move object geometry to object origin.

    ORIGIN_GEOMETRY
    Origin to Geometry, Calculate the center of geometry based on the current pivot point (median, otherwise bounding-box).

    ORIGIN_CURSOR
    Origin to 3D Cursor, Move object origin to position of the 3D cursor.

    ORIGIN_CENTER_OF_MASS
    Origin to Center of Mass (Surface), Calculate the center of mass from the surface area.

    ORIGIN_CENTER_OF_VOLUME
    Origin to Center of Mass (Volume), Calculate the center of mass from the volume (must be manifold geometry with consistent normals).
        :type type: typing.Literal['GEOMETRY_ORIGIN','ORIGIN_GEOMETRY','ORIGIN_CURSOR','ORIGIN_CENTER_OF_MASS','ORIGIN_CENTER_OF_VOLUME'] | None
        :param center: Center
        :type center: typing.Literal['MEDIAN','BOUNDS'] | None
    """

def parent_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["CLEAR", "CLEAR_KEEP_TRANSFORM", "CLEAR_INVERSE"]
    | None = "CLEAR",
):
    """Clear the object's parenting

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    CLEAR
    Clear Parent, Completely clear the parenting relationship, including involved modifiers if any.

    CLEAR_KEEP_TRANSFORM
    Clear and Keep Transformation, As 'Clear Parent', but keep the current visual transformations of the object.

    CLEAR_INVERSE
    Clear Parent Inverse, Reset the transform corrections applied to the parenting relationship, does not remove parenting itself.
        :type type: typing.Literal['CLEAR','CLEAR_KEEP_TRANSFORM','CLEAR_INVERSE'] | None
    """

def parent_no_inverse_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set the object's parenting without setting the inverse parent correction

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def parent_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "OBJECT",
        "ARMATURE",
        "ARMATURE_NAME",
        "ARMATURE_AUTO",
        "ARMATURE_ENVELOPE",
        "BONE",
        "BONE_RELATIVE",
        "CURVE",
        "FOLLOW",
        "PATH_CONST",
        "LATTICE",
        "VERTEX",
        "VERTEX_TRI",
    ]
    | None = "OBJECT",
    xmirror: bool | None = False,
    keep_transform: bool | None = False,
):
    """Set the object's parenting

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['OBJECT','ARMATURE','ARMATURE_NAME','ARMATURE_AUTO','ARMATURE_ENVELOPE','BONE','BONE_RELATIVE','CURVE','FOLLOW','PATH_CONST','LATTICE','VERTEX','VERTEX_TRI'] | None
    :param xmirror: X Mirror, Apply weights symmetrically along X axis, for Envelope/Automatic vertex groups creation
    :type xmirror: bool | None
    :param keep_transform: Keep Transform, Apply transformation before parenting
    :type keep_transform: bool | None
    """

def particle_system_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a particle system

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def particle_system_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the selected particle system

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def paths_calculate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    start_frame: int | None = 1,
    end_frame: int | None = 250,
):
    """Calculate motion paths for the selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param start_frame: Start, First frame to calculate object paths on
    :type start_frame: int | None
    :param end_frame: End, Last frame to calculate object paths on
    :type end_frame: int | None
    """

def paths_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    only_selected: bool | None = False,
):
    """Clear path caches for all objects, hold Shift key for selected objects only

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param only_selected: Only Selected, Only clear paths from selected objects
    :type only_selected: bool | None
    """

def paths_range_update(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Update frame range for motion paths from the Scene's current frame range

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def paths_update(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Recalculate paths for selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def pointcloud_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a point cloud object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def posemode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Enable or disable posing/selecting bones

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def proxy_make(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    object: str | None = "DEFAULT",
):
    """Add empty object to become local replacement data of a library-linked object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param object: Proxy Object, Name of lib-linked/collection object to make a proxy for
    :type object: str | None
    """

def quadriflow_remesh(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_paint_symmetry: bool | None = True,
    use_preserve_sharp: bool | None = False,
    use_preserve_boundary: bool | None = False,
    preserve_paint_mask: bool | None = False,
    smooth_normals: bool | None = False,
    mode: typing.Literal["RATIO", "EDGE", "FACES"] | None = "FACES",
    target_ratio: float | None = 1.0,
    target_edge_length: float | None = 0.1,
    target_faces: int | None = 4000,
    mesh_area: float | None = -1,
    seed: int | None = 0,
):
    """Create a new quad based mesh using the surface data of the current mesh. All data layers will be lost

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param use_paint_symmetry: Use Paint Symmetry, Generates a symmetrical mesh using the paint symmetry configuration
        :type use_paint_symmetry: bool | None
        :param use_preserve_sharp: Preserve Sharp, Try to preserve sharp features on the mesh
        :type use_preserve_sharp: bool | None
        :param use_preserve_boundary: Preserve Mesh Boundary, Try to preserve mesh boundary on the mesh
        :type use_preserve_boundary: bool | None
        :param preserve_paint_mask: Preserve Paint Mask, Reproject the paint mask onto the new mesh
        :type preserve_paint_mask: bool | None
        :param smooth_normals: Smooth Normals, Set the output mesh normals to smooth
        :type smooth_normals: bool | None
        :param mode: Mode, How to specify the amount of detail for the new mesh

    RATIO
    Ratio, Specify target number of faces relative to the current mesh.

    EDGE
    Edge Length, Input target edge length in the new mesh.

    FACES
    Faces, Input target number of faces in the new mesh.
        :type mode: typing.Literal['RATIO','EDGE','FACES'] | None
        :param target_ratio: Ratio, Relative number of faces compared to the current mesh
        :type target_ratio: float | None
        :param target_edge_length: Edge Length, Target edge length in the new mesh
        :type target_edge_length: float | None
        :param target_faces: Number of Faces, Approximate number of faces (quads) in the new mesh
        :type target_faces: int | None
        :param mesh_area: Old Object Face Area, This property is only used to cache the object area for later calculations
        :type mesh_area: float | None
        :param seed: Seed, Random seed to use with the solver. Different seeds will cause the remesher to come up with different quad layouts on the mesh
        :type seed: int | None
    """

def quick_explode(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    style: typing.Literal["EXPLODE", "BLEND"] | None = "EXPLODE",
    amount: int | None = 100,
    frame_duration: int | None = 50,
    frame_start: int | None = 1,
    frame_end: int | None = 10,
    velocity: float | None = 1.0,
    fade: bool | None = True,
):
    """Make selected objects explode

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param style: Explode Style
    :type style: typing.Literal['EXPLODE','BLEND'] | None
    :param amount: Amount of pieces
    :type amount: int | None
    :param frame_duration: Duration
    :type frame_duration: int | None
    :param frame_start: Start Frame
    :type frame_start: int | None
    :param frame_end: End Frame
    :type frame_end: int | None
    :param velocity: Outwards Velocity
    :type velocity: float | None
    :param fade: Fade, Fade the pieces over time
    :type fade: bool | None
    """

def quick_fur(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    density: typing.Literal["LIGHT", "MEDIUM", "HEAVY"] | None = "MEDIUM",
    view_percentage: int | None = 10,
    length: float | None = 0.1,
):
    """Add fur setup to the selected objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param density: Fur Density
    :type density: typing.Literal['LIGHT','MEDIUM','HEAVY'] | None
    :param view_percentage: View %
    :type view_percentage: int | None
    :param length: Length
    :type length: float | None
    """

def quick_liquid(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    show_flows: bool | None = False,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param show_flows: Render Liquid Objects, Keep the liquid objects visible during rendering
    :type show_flows: bool | None
    """

def quick_smoke(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    style: typing.Literal["SMOKE", "FIRE", "BOTH"] | None = "SMOKE",
    show_flows: bool | None = False,
):
    """Use selected objects as smoke emitters

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param style: Smoke Style
    :type style: typing.Literal['SMOKE','FIRE','BOTH'] | None
    :param show_flows: Render Smoke Objects, Keep the smoke objects visible during rendering
    :type show_flows: bool | None
    """

def randomize_transform(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    random_seed: int | None = 0,
    use_delta: bool | None = False,
    use_loc: bool | None = True,
    loc: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    use_rot: bool | None = True,
    rot: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    use_scale: bool | None = True,
    scale_even: bool | None = False,
    scale: collections.abc.Iterable[float] | None = (1.0, 1.0, 1.0),
):
    """Randomize objects loc/rot/scale

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param random_seed: Random Seed, Seed value for the random generator
    :type random_seed: int | None
    :param use_delta: Transform Delta, Randomize delta transform values instead of regular transform
    :type use_delta: bool | None
    :param use_loc: Randomize Location, Randomize the location values
    :type use_loc: bool | None
    :param loc: Location, Maximum distance the objects can spread over each axis
    :type loc: collections.abc.Iterable[float] | None
    :param use_rot: Randomize Rotation, Randomize the rotation values
    :type use_rot: bool | None
    :param rot: Rotation, Maximum rotation over each axis
    :type rot: collections.abc.Iterable[float] | None
    :param use_scale: Randomize Scale, Randomize the scale values
    :type use_scale: bool | None
    :param scale_even: Scale Even, Use the same scale value for all axis
    :type scale_even: bool | None
    :param scale: Scale, Maximum scale randomization over each axis
    :type scale: collections.abc.Iterable[float] | None
    """

def rotation_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    clear_delta: bool | None = False,
):
    """Clear the object's rotation

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param clear_delta: Clear Delta, Clear delta rotation in addition to clearing the normal rotation transform
    :type clear_delta: bool | None
    """

def scale_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    clear_delta: bool | None = False,
):
    """Clear the object's scale

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param clear_delta: Clear Delta, Clear delta scale in addition to clearing the normal scale transform
    :type clear_delta: bool | None
    """

def select_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
):
    """Change selection of all visible objects in scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle, Toggle selection for all elements.

    SELECT
    Select, Select all elements.

    DESELECT
    Deselect, Deselect all elements.

    INVERT
    Invert, Invert selection of all elements.
        :type action: typing.Literal['TOGGLE','SELECT','DESELECT','INVERT'] | None
    """

def select_by_type(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
    type: typing.Literal[
        "MESH",
        "CURVE",
        "SURFACE",
        "META",
        "FONT",
        "HAIR",
        "POINTCLOUD",
        "VOLUME",
        "ARMATURE",
        "LATTICE",
        "EMPTY",
        "GPENCIL",
        "CAMERA",
        "LIGHT",
        "SPEAKER",
        "LIGHT_PROBE",
    ]
    | None = "MESH",
):
    """Select all visible objects that are of a type

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: bool | None
    :param type: Type
    :type type: typing.Literal['MESH','CURVE','SURFACE','META','FONT','HAIR','POINTCLOUD','VOLUME','ARMATURE','LATTICE','EMPTY','GPENCIL','CAMERA','LIGHT','SPEAKER','LIGHT_PROBE'] | None
    """

def select_camera(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
):
    """Select the active camera

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend the selection
    :type extend: bool | None
    """

def select_grouped(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
    type: typing.Literal[
        "CHILDREN_RECURSIVE",
        "CHILDREN",
        "PARENT",
        "SIBLINGS",
        "TYPE",
        "COLLECTION",
        "HOOK",
        "PASS",
        "COLOR",
        "KEYINGSET",
        "LIGHT_TYPE",
    ]
    | None = "CHILDREN_RECURSIVE",
):
    """Select all visible objects grouped by various properties

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param extend: Extend, Extend selection instead of deselecting everything first
        :type extend: bool | None
        :param type: Type

    CHILDREN_RECURSIVE
    Children.

    CHILDREN
    Immediate Children.

    PARENT
    Parent.

    SIBLINGS
    Siblings, Shared Parent.

    TYPE
    Type, Shared object type.

    COLLECTION
    Collection, Shared collection.

    HOOK
    Hook.

    PASS
    Pass, Render pass Index.

    COLOR
    Color, Object Color.

    KEYINGSET
    Keying Set, Objects included in active Keying Set.

    LIGHT_TYPE
    Light Type, Matching light types.
        :type type: typing.Literal['CHILDREN_RECURSIVE','CHILDREN','PARENT','SIBLINGS','TYPE','COLLECTION','HOOK','PASS','COLOR','KEYINGSET','LIGHT_TYPE'] | None
    """

def select_hierarchy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: typing.Literal["PARENT", "CHILD"] | None = "PARENT",
    extend: bool | None = False,
):
    """Select object relative to the active object's position in the hierarchy

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to select in the hierarchy
    :type direction: typing.Literal['PARENT','CHILD'] | None
    :param extend: Extend, Extend the existing selection
    :type extend: bool | None
    """

def select_less(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Deselect objects at the boundaries of parent/child relationships

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_linked(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
    type: typing.Literal[
        "OBDATA", "MATERIAL", "DUPGROUP", "PARTICLE", "LIBRARY", "LIBRARY_OBDATA"
    ]
    | None = "OBDATA",
):
    """Select all visible objects that are linked

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: bool | None
    :param type: Type
    :type type: typing.Literal['OBDATA','MATERIAL','DUPGROUP','PARTICLE','LIBRARY','LIBRARY_OBDATA'] | None
    """

def select_mirror(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    extend: bool | None = False,
):
    """Select the Mirror objects of the selected object eg. L.sword -> R.sword

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param extend: Extend, Extend selection instead of deselecting everything first
    :type extend: bool | None
    """

def select_more(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select connected parent/child objects

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_pattern(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    pattern: str = "*",
    case_sensitive: bool | None = False,
    extend: bool | None = True,
):
    """Select objects matching a naming pattern

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param pattern: Pattern, Name filter using '*', '?' and '[abc]' unix style wildcards
    :type pattern: str
    :param case_sensitive: Case Sensitive, Do a case sensitive compare
    :type case_sensitive: bool | None
    :param extend: Extend, Extend the existing selection
    :type extend: bool | None
    """

def select_random(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    percent: float | None = 50.0,
    seed: int | None = 0,
    action: typing.Literal["SELECT", "DESELECT"] | None = "SELECT",
):
    """Set select on random visible objects

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param percent: Percent, Percentage of objects to select randomly
        :type percent: float | None
        :param seed: Random Seed, Seed for the random number generator
        :type seed: int | None
        :param action: Action, Selection action to execute

    SELECT
    Select, Select all elements.

    DESELECT
    Deselect, Deselect all elements.
        :type action: typing.Literal['SELECT','DESELECT'] | None
    """

def select_same_collection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    collection: str = "",
):
    """Select object in the same collection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param collection: Collection, Name of the collection to select
    :type collection: str
    """

def shade_flat(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Render and display faces uniform, using Face Normals

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def shade_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Render and display faces smooth, using interpolated Vertex Normals

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def shaderfx_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal[
        "FX_BLUR",
        "FX_COLORIZE",
        "FX_FLIP",
        "FX_GLOW",
        "FX_PIXEL",
        "FX_RIM",
        "FX_SHADOW",
        "FX_SWIRL",
        "FX_WAVE",
    ]
    | None = "FX_BLUR",
):
    """Add a visual effect to the active object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    FX_BLUR
    Blur, Apply Gaussian Blur to object.

    FX_COLORIZE
    Colorize, Apply different tint effects.

    FX_FLIP
    Flip, Flip image.

    FX_GLOW
    Glow, Create a glow effect.

    FX_PIXEL
    Pixelate, Pixelate image.

    FX_RIM
    Rim, Add a rim to the image.

    FX_SHADOW
    Shadow, Create a shadow effect.

    FX_SWIRL
    Swirl, Create a rotation distortion.

    FX_WAVE
    Wave Distortion, Apply sinusoidal deformation.
        :type type: typing.Literal['FX_BLUR','FX_COLORIZE','FX_FLIP','FX_GLOW','FX_PIXEL','FX_RIM','FX_SHADOW','FX_SWIRL','FX_WAVE'] | None
    """

def shaderfx_move_down(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
):
    """Move effect down in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    """

def shaderfx_move_to_index(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
    index: int | None = 0,
):
    """Change the effect's position in the list so it evaluates after the set number of others

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    :param index: Index, The index to move the effect to
    :type index: int | None
    """

def shaderfx_move_up(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
):
    """Move effect up in the stack

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    """

def shaderfx_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shaderfx: str = "",
    report: bool | None = False,
):
    """Remove a effect from the active grease pencil object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shaderfx: Shader, Name of the shaderfx to edit
    :type shaderfx: str
    :param report: Report, Create a notification after the operation
    :type report: bool | None
    """

def shape_key_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    from_mix: bool | None = True,
):
    """Add shape key to the object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param from_mix: From Mix, Create the new shape key from the existing mix of keys
    :type from_mix: bool | None
    """

def shape_key_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear weights for all shape keys

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def shape_key_mirror(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_topology: bool | None = False,
):
    """Mirror the current shape key along the local X axis

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_topology: Topology Mirror, Use topology based mirroring (for when both sides of mesh have matching, unique topology)
    :type use_topology: bool | None
    """

def shape_key_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["TOP", "UP", "DOWN", "BOTTOM"] | None = "TOP",
):
    """Move the active shape key up/down in the list

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    TOP
    Top, Top of the list.

    UP
    Up.

    DOWN
    Down.

    BOTTOM
    Bottom, Bottom of the list.
        :type type: typing.Literal['TOP','UP','DOWN','BOTTOM'] | None
    """

def shape_key_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
):
    """Remove shape key from the object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All, Remove all shape keys
    :type all: bool | None
    """

def shape_key_retime(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Resets the timing for absolute shape keys

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def shape_key_transfer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["OFFSET", "RELATIVE_FACE", "RELATIVE_EDGE"] | None = "OFFSET",
    use_clamp: bool | None = False,
):
    """Copy the active shape key of another selected object to this one

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Transformation Mode, Relative shape positions to the new shape method

    OFFSET
    Offset, Apply the relative positional offset.

    RELATIVE_FACE
    Relative Face, Calculate relative position (using faces).

    RELATIVE_EDGE
    Relative Edge, Calculate relative position (using edges).
        :type mode: typing.Literal['OFFSET','RELATIVE_FACE','RELATIVE_EDGE'] | None
        :param use_clamp: Clamp Offset, Clamp the transformation to the distance each vertex moves in the original shape
        :type use_clamp: bool | None
    """

def skin_armature_create(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Create an armature that parallels the skin layout

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def skin_loose_mark_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: typing.Literal["MARK", "CLEAR"] | None = "MARK",
):
    """Mark/clear selected vertices as loose

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action

    MARK
    Mark, Mark selected vertices as loose.

    CLEAR
    Clear, Set selected vertices as not loose.
        :type action: typing.Literal['MARK','CLEAR'] | None
    """

def skin_radii_equalize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Make skin radii of selected vertices equal on each axis

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def skin_root_mark(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Mark selected vertices as roots

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def speaker_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a speaker object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def subdivision_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    level: int | None = 1,
    relative: bool | None = False,
):
    """Sets a Subdivision Surface Level (1-5)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param level: Level
    :type level: int | None
    :param relative: Relative, Apply the subdivision surface level as an offset relative to the current level
    :type relative: bool | None
    """

def surfacedeform_bind(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    modifier: str = "",
):
    """Bind mesh to target in surface deform modifier

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param modifier: Modifier, Name of the modifier to edit
    :type modifier: str
    """

def text_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a text object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param radius: Radius
        :type radius: float | None
        :param enter_editmode: Enter Editmode, Enter editmode when adding this object
        :type enter_editmode: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def track_clear(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["CLEAR", "CLEAR_KEEP_TRANSFORM"] | None = "CLEAR",
):
    """Clear tracking constraint or flag from object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['CLEAR','CLEAR_KEEP_TRANSFORM'] | None
    """

def track_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["DAMPTRACK", "TRACKTO", "LOCKTRACK"] | None = "DAMPTRACK",
):
    """Make the object track another object, using various methods/constraints

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['DAMPTRACK','TRACKTO','LOCKTRACK'] | None
    """

def transform_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    location: bool | None = True,
    rotation: bool | None = True,
    scale: bool | None = True,
    properties: bool | None = True,
):
    """Apply the object's transformation to its data

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param location: Location
    :type location: bool | None
    :param rotation: Rotation
    :type rotation: bool | None
    :param scale: Scale
    :type scale: bool | None
    :param properties: Apply Properties, Modify properties such as curve vertex radius, font size and bone envelope
    :type properties: bool | None
    """

def transform_axis_target(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Interactively point cameras and lights to a location (Ctrl translates)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def transforms_to_deltas(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["ALL", "LOC", "ROT", "SCALE"] | None = "ALL",
    reset_values: bool | None = True,
):
    """Convert normal object transforms to delta transforms, any existing delta transforms will be included as well

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode, Which transforms to transfer

    ALL
    All Transforms, Transfer location, rotation, and scale transforms.

    LOC
    Location, Transfer location transforms only.

    ROT
    Rotation, Transfer rotation transforms only.

    SCALE
    Scale, Transfer scale transforms only.
        :type mode: typing.Literal['ALL','LOC','ROT','SCALE'] | None
        :param reset_values: Reset Values, Clear transform values after transferring to deltas
        :type reset_values: bool | None
    """

def unlink_data(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new vertex group to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_assign(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Assign the selected vertices to the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_assign_new(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Assign the selected vertices to a new vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_clean(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    limit: float | None = 0.0,
    keep_single: bool | None = False,
):
    """Remove vertex group assignments which are not required

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of Groups shall be used
    :type group_select_mode: str | None
    :param limit: Limit, Remove vertices which weight is below or equal to this limit
    :type limit: float | None
    :param keep_single: Keep Single, Keep verts assigned to at least one group when cleaning
    :type keep_single: bool | None
    """

def vertex_group_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Make a copy of the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_copy_to_linked(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Replace vertex groups of all users of the same geometry data by vertex groups of active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_copy_to_selected(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Replace vertex groups of selected objects by vertex groups of active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_deselect(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Deselect all selected vertices assigned to the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_fix(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    dist: float | None = 0.0,
    strength: float | None = 1.0,
    accuracy: float | None = 1.0,
):
    """Modify the position of selected vertices by changing only their respective groups' weights (this tool may be slow for many vertices)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param dist: Distance, The distance to move to
    :type dist: float | None
    :param strength: Strength, The distance moved can be changed by this multiplier
    :type strength: float | None
    :param accuracy: Change Sensitivity, Change the amount weights are altered with each iteration: lower values are slower
    :type accuracy: float | None
    """

def vertex_group_invert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    auto_assign: bool | None = True,
    auto_remove: bool | None = True,
):
    """Invert active vertex group's weights

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of Groups shall be used
    :type group_select_mode: str | None
    :param auto_assign: Add Weights, Add vertices from groups that have zero weight before inverting
    :type auto_assign: bool | None
    :param auto_remove: Remove Weights, Remove vertices from groups that have zero weight after inverting
    :type auto_remove: bool | None
    """

def vertex_group_levels(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    offset: float | None = 0.0,
    gain: float | None = 1.0,
):
    """Add some offset and multiply with some gain the weights of the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of Groups shall be used
    :type group_select_mode: str | None
    :param offset: Offset, Value to add to weights
    :type offset: float | None
    :param gain: Gain, Value to multiply weights by
    :type gain: float | None
    """

def vertex_group_limit_total(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    limit: int | None = 4,
):
    """Limit deform weights associated with a vertex to a specified number by removing lowest weights

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of Groups shall be used
    :type group_select_mode: str | None
    :param limit: Limit, Maximum number of deform weights
    :type limit: int | None
    """

def vertex_group_lock(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: typing.Literal["TOGGLE", "LOCK", "UNLOCK", "INVERT"] | None = "TOGGLE",
    mask: typing.Literal["ALL", "SELECTED", "UNSELECTED", "INVERT_UNSELECTED"]
    | None = "ALL",
):
    """Change the lock state of all or some vertex groups of active object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Lock action to execute on vertex groups

    TOGGLE
    Toggle, Unlock all vertex groups if there is at least one locked group, lock all in other case.

    LOCK
    Lock, Lock all vertex groups.

    UNLOCK
    Unlock, Unlock all vertex groups.

    INVERT
    Invert, Invert the lock state of all vertex groups.
        :type action: typing.Literal['TOGGLE','LOCK','UNLOCK','INVERT'] | None
        :param mask: Mask, Apply the action based on vertex group selection

    ALL
    All, Apply action to all vertex groups.

    SELECTED
    Selected, Apply to selected vertex groups.

    UNSELECTED
    Unselected, Apply to unselected vertex groups.

    INVERT_UNSELECTED
    Invert Unselected, Apply the opposite of Lock/Unlock to unselected vertex groups.
        :type mask: typing.Literal['ALL','SELECTED','UNSELECTED','INVERT_UNSELECTED'] | None
    """

def vertex_group_mirror(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mirror_weights: bool | None = True,
    flip_group_names: bool | None = True,
    all_groups: bool | None = False,
    use_topology: bool | None = False,
):
    """Mirror vertex group, flip weights and/or names, editing only selected vertices, flipping when both sides are selected otherwise copy from unselected

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mirror_weights: Mirror Weights, Mirror weights
    :type mirror_weights: bool | None
    :param flip_group_names: Flip Group Names, Flip vertex group names
    :type flip_group_names: bool | None
    :param all_groups: All Groups, Mirror all vertex groups weights
    :type all_groups: bool | None
    :param use_topology: Topology Mirror, Use topology based mirroring (for when both sides of mesh have matching, unique topology)
    :type use_topology: bool | None
    """

def vertex_group_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Move the active vertex group up/down in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction, Direction to move the active vertex group towards
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def vertex_group_normalize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Normalize weights of the active vertex group, so that the highest ones are now 1.0

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_normalize_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    lock_active: bool | None = True,
):
    """Normalize all weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of Groups shall be used
    :type group_select_mode: str | None
    :param lock_active: Lock Active, Keep the values of the active group while normalizing others
    :type lock_active: bool | None
    """

def vertex_group_quantize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    steps: int | None = 4,
):
    """Set weights to a fixed number of steps

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of Groups shall be used
    :type group_select_mode: str | None
    :param steps: Steps, Number of steps between 0 and 1
    :type steps: int | None
    """

def vertex_group_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
    all_unlocked: bool | None = False,
):
    """Delete the active or all vertex groups from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: All, Remove all vertex groups
    :type all: bool | None
    :param all_unlocked: All Unlocked, Remove all unlocked vertex groups
    :type all_unlocked: bool | None
    """

def vertex_group_remove_from(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_all_groups: bool | None = False,
    use_all_verts: bool | None = False,
):
    """Remove the selected vertices from active or all vertex group(s)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_all_groups: All Groups, Remove from all groups
    :type use_all_groups: bool | None
    :param use_all_verts: All Vertices, Clear the active group
    :type use_all_verts: bool | None
    """

def vertex_group_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select all the vertices assigned to the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_set_active(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group: str | None = "",
):
    """Set the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group: Group, Vertex group to set as active
    :type group: str | None
    """

def vertex_group_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    group_select_mode: str | None = "",
    factor: float | None = 0.5,
    repeat: int | None = 1,
    expand: float | None = 0.0,
):
    """Smooth weights for selected vertices

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param group_select_mode: Subset, Define which subset of Groups shall be used
    :type group_select_mode: str | None
    :param factor: Factor
    :type factor: float | None
    :param repeat: Iterations
    :type repeat: int | None
    :param expand: Expand/Contract, Expand/contract weights
    :type expand: float | None
    """

def vertex_group_sort(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    sort_type: typing.Literal["NAME", "BONE_HIERARCHY"] | None = "NAME",
):
    """Sort vertex groups

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param sort_type: Sort type, Sort type
    :type sort_type: typing.Literal['NAME','BONE_HIERARCHY'] | None
    """

def vertex_parent_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Parent selected objects to the selected vertices

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_weight_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy weights from active to selected

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_weight_delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    weight_group: int | None = -1,
):
    """Delete this weight from the vertex (disabled if vertex group is locked)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param weight_group: Weight Index, Index of source weight in active vertex group
    :type weight_group: int | None
    """

def vertex_weight_normalize_active_vertex(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Normalize active vertex's weights

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_weight_paste(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    weight_group: int | None = -1,
):
    """Copy this group's weight to other selected vertices (disabled if vertex group is locked)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param weight_group: Weight Index, Index of source weight in active vertex group
    :type weight_group: int | None
    """

def vertex_weight_set_active(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    weight_group: int | None = -1,
):
    """Set as active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param weight_group: Weight Index, Index of source weight in active vertex group
    :type weight_group: int | None
    """

def visual_transform_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Apply the object's visual transformation to its data

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def volume_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Add a volume object to the scene

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def volume_import(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    directory: str = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    hide_props_region: bool | None = True,
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
    filter_usd: bool | None = False,
    filter_volume: bool | None = True,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: typing.Literal[
        "FILE_SORT_ALPHA", "FILE_SORT_EXTENSION", "FILE_SORT_TIME", "FILE_SORT_SIZE"
    ]
    | None = "FILE_SORT_ALPHA",
    use_sequence_detection: bool | None = True,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    rotation: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
    scale: collections.abc.Iterable[float] | None = (0.0, 0.0, 0.0),
):
    """Import OpenVDB volume file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str
        :param directory: Directory, Directory of the file
        :type directory: str
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
        :param use_sequence_detection: Detect Sequences, Automatically detect animated sequences in selected volume files (based on file names)
        :type use_sequence_detection: bool | None
        :param align: Align, The alignment of the new object

    WORLD
    World, Align the new object to the world.

    VIEW
    View, Align the new object to the view.

    CURSOR
    3D Cursor, Use the 3D cursor orientation for the new object.
        :type align: typing.Literal['WORLD','VIEW','CURSOR'] | None
        :param location: Location, Location for the newly added object
        :type location: collections.abc.Iterable[float] | None
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: collections.abc.Iterable[float] | None
        :param scale: Scale, Scale for the newly added object
        :type scale: collections.abc.Iterable[float] | None
    """

def voxel_remesh(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Calculates a new manifold mesh based on the volume of the current mesh. All data layers will be lost

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def voxel_size_edit(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Modify the mesh voxel size interactively used in the voxel remesher

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """
