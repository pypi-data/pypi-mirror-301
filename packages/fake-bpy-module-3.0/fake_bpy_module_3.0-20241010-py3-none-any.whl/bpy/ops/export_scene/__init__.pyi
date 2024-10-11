import typing
import collections.abc
import typing_extensions
import bpy.types

def fbx(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    filter_glob: str = "*.fbx",
    use_selection: bool | None = False,
    use_active_collection: bool | None = False,
    global_scale: float | None = 1.0,
    apply_unit_scale: bool | None = True,
    apply_scale_options: typing.Literal[
        "FBX_SCALE_NONE", "FBX_SCALE_UNITS", "FBX_SCALE_CUSTOM", "FBX_SCALE_ALL"
    ]
    | None = "FBX_SCALE_NONE",
    use_space_transform: bool | None = True,
    bake_space_transform: bool | None = False,
    object_types: set[
        typing.Literal["EMPTY", "CAMERA", "LIGHT", "ARMATURE", "MESH", "OTHER"]
    ]
    | None = {"ARMATURE", "CAMERA", "EMPTY", "LIGHT", "MESH", "OTHER"},
    use_mesh_modifiers: bool | None = True,
    use_mesh_modifiers_render: bool | None = True,
    mesh_smooth_type: typing.Literal["OFF", "FACE", "EDGE"] | None = "OFF",
    use_subsurf: bool | None = False,
    use_mesh_edges: bool | None = False,
    use_tspace: bool | None = False,
    use_custom_props: bool | None = False,
    add_leaf_bones: bool | None = True,
    primary_bone_axis: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "Y",
    secondary_bone_axis: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "X",
    use_armature_deform_only: bool | None = False,
    armature_nodetype: typing.Literal["NULL", "ROOT", "LIMBNODE"] | None = "NULL",
    bake_anim: bool | None = True,
    bake_anim_use_all_bones: bool | None = True,
    bake_anim_use_nla_strips: bool | None = True,
    bake_anim_use_all_actions: bool | None = True,
    bake_anim_force_startend_keying: bool | None = True,
    bake_anim_step: float | None = 1.0,
    bake_anim_simplify_factor: float | None = 1.0,
    path_mode: typing.Literal["AUTO", "ABSOLUTE", "RELATIVE", "MATCH", "STRIP", "COPY"]
    | None = "AUTO",
    embed_textures: bool | None = False,
    batch_mode: typing.Literal[
        "OFF", "SCENE", "COLLECTION", "SCENE_COLLECTION", "ACTIVE_SCENE_COLLECTION"
    ]
    | None = "OFF",
    use_batch_own_dir: bool | None = True,
    use_metadata: bool | None = True,
    axis_forward: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "-Z",
    axis_up: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "Y",
):
    """Write a FBX file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_glob: filter_glob
        :type filter_glob: str
        :param use_selection: Selected Objects, Export selected and visible objects only
        :type use_selection: bool | None
        :param use_active_collection: Active Collection, Export only objects from the active collection (and its children)
        :type use_active_collection: bool | None
        :param global_scale: Scale, Scale all data (Some importers do not support scaled armatures!)
        :type global_scale: float | None
        :param apply_unit_scale: Apply Unit, Take into account current Blender units settings (if unset, raw Blender Units values are used as-is)
        :type apply_unit_scale: bool | None
        :param apply_scale_options: Apply Scalings, How to apply custom and units scalings in generated FBX file (Blender uses FBX scale to detect units on import, but many other applications do not handle the same way)

    FBX_SCALE_NONE
    All Local -- Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0.

    FBX_SCALE_UNITS
    FBX Units Scale -- Apply custom scaling to each object transformation, and units scaling to FBX scale.

    FBX_SCALE_CUSTOM
    FBX Custom Scale -- Apply custom scaling to FBX scale, and units scaling to each object transformation.

    FBX_SCALE_ALL
    FBX All -- Apply custom scaling and units scaling to FBX scale.
        :type apply_scale_options: typing.Literal['FBX_SCALE_NONE','FBX_SCALE_UNITS','FBX_SCALE_CUSTOM','FBX_SCALE_ALL'] | None
        :param use_space_transform: Use Space Transform, Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is
        :type use_space_transform: bool | None
        :param bake_space_transform: Apply Transform, Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender's space (WARNING! experimental option, use at own risks, known broken with armatures/animations)
        :type bake_space_transform: bool | None
        :param object_types: Object Types, Which kind of object to export

    EMPTY
    Empty.

    CAMERA
    Camera.

    LIGHT
    Lamp.

    ARMATURE
    Armature -- WARNING: not supported in dupli/group instances.

    MESH
    Mesh.

    OTHER
    Other -- Other geometry types, like curve, metaball, etc. (converted to meshes).
        :type object_types: set[typing.Literal['EMPTY','CAMERA','LIGHT','ARMATURE','MESH','OTHER']] | None
        :param use_mesh_modifiers: Apply Modifiers, Apply modifiers to mesh objects (except Armature ones) - WARNING: prevents exporting shape keys
        :type use_mesh_modifiers: bool | None
        :param use_mesh_modifiers_render: Use Modifiers Render Setting, Use render settings when applying modifiers to mesh objects (DISABLED in Blender 2.8)
        :type use_mesh_modifiers_render: bool | None
        :param mesh_smooth_type: Smoothing, Export smoothing information (prefer 'Normals Only' option if your target importer understand split normals)

    OFF
    Normals Only -- Export only normals instead of writing edge or face smoothing data.

    FACE
    Face -- Write face smoothing.

    EDGE
    Edge -- Write edge smoothing.
        :type mesh_smooth_type: typing.Literal['OFF','FACE','EDGE'] | None
        :param use_subsurf: Export Subdivision Surface, Export the last Catmull-Rom subdivision modifier as FBX subdivision (does not apply the modifier even if 'Apply Modifiers' is enabled)
        :type use_subsurf: bool | None
        :param use_mesh_edges: Loose Edges, Export loose edges (as two-vertices polygons)
        :type use_mesh_edges: bool | None
        :param use_tspace: Tangent Space, Add binormal and tangent vectors, together with normal they form the tangent space (will only work correctly with tris/quads only meshes!)
        :type use_tspace: bool | None
        :param use_custom_props: Custom Properties, Export custom properties
        :type use_custom_props: bool | None
        :param add_leaf_bones: Add Leaf Bones, Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)
        :type add_leaf_bones: bool | None
        :param primary_bone_axis: Primary Bone Axis
        :type primary_bone_axis: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
        :param secondary_bone_axis: Secondary Bone Axis
        :type secondary_bone_axis: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
        :param use_armature_deform_only: Only Deform Bones, Only write deforming bones (and non-deforming ones when they have deforming children)
        :type use_armature_deform_only: bool | None
        :param armature_nodetype: Armature FBXNode Type, FBX type of node (object) used to represent Blender's armatures (use Null one unless you experience issues with other app, other choices may no import back perfectly in Blender...)

    NULL
    Null -- 'Null' FBX node, similar to Blender's Empty (default).

    ROOT
    Root -- 'Root' FBX node, supposed to be the root of chains of bones....

    LIMBNODE
    LimbNode -- 'LimbNode' FBX node, a regular joint between two bones....
        :type armature_nodetype: typing.Literal['NULL','ROOT','LIMBNODE'] | None
        :param bake_anim: Baked Animation, Export baked keyframe animation
        :type bake_anim: bool | None
        :param bake_anim_use_all_bones: Key All Bones, Force exporting at least one key of animation for all bones (needed with some target applications, like UE4)
        :type bake_anim_use_all_bones: bool | None
        :param bake_anim_use_nla_strips: NLA Strips, Export each non-muted NLA strip as a separated FBX's AnimStack, if any, instead of global scene animation
        :type bake_anim_use_nla_strips: bool | None
        :param bake_anim_use_all_actions: All Actions, Export each action as a separated FBX's AnimStack, instead of global scene animation (note that animated objects will get all actions compatible with them, others will get no animation at all)
        :type bake_anim_use_all_actions: bool | None
        :param bake_anim_force_startend_keying: Force Start/End Keying, Always add a keyframe at start and end of actions for animated channels
        :type bake_anim_force_startend_keying: bool | None
        :param bake_anim_step: Sampling Rate, How often to evaluate animated values (in frames)
        :type bake_anim_step: float | None
        :param bake_anim_simplify_factor: Simplify, How much to simplify baked values (0.0 to disable, the higher the more simplified)
        :type bake_anim_simplify_factor: float | None
        :param path_mode: Path Mode, Method used to reference paths

    AUTO
    Auto -- Use Relative paths with subdirectories only.

    ABSOLUTE
    Absolute -- Always write absolute paths.

    RELATIVE
    Relative -- Always write relative paths (where possible).

    MATCH
    Match -- Match Absolute/Relative setting with input path.

    STRIP
    Strip Path -- Filename only.

    COPY
    Copy -- Copy the file to the destination path (or subdirectory).
        :type path_mode: typing.Literal['AUTO','ABSOLUTE','RELATIVE','MATCH','STRIP','COPY'] | None
        :param embed_textures: Embed Textures, Embed textures in FBX binary file (only for "Copy" path mode!)
        :type embed_textures: bool | None
        :param batch_mode: Batch Mode

    OFF
    Off -- Active scene to file.

    SCENE
    Scene -- Each scene as a file.

    COLLECTION
    Collection -- Each collection (data-block ones) as a file, does not include content of children collections.

    SCENE_COLLECTION
    Scene Collections -- Each collection (including master, non-data-block ones) of each scene as a file, including content from children collections.

    ACTIVE_SCENE_COLLECTION
    Active Scene Collections -- Each collection (including master, non-data-block one) of the active scene as a file, including content from children collections.
        :type batch_mode: typing.Literal['OFF','SCENE','COLLECTION','SCENE_COLLECTION','ACTIVE_SCENE_COLLECTION'] | None
        :param use_batch_own_dir: Batch Own Dir, Create a dir for each exported file
        :type use_batch_own_dir: bool | None
        :param use_metadata: Use Metadata
        :type use_metadata: bool | None
        :param axis_forward: Forward
        :type axis_forward: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
        :param axis_up: Up
        :type axis_up: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
    """

def gltf(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    export_format: typing.Literal["GLB", "GLTF_SEPARATE", "GLTF_EMBEDDED"]
    | None = "GLB",
    ui_tab: typing.Literal["GENERAL", "MESHES", "OBJECTS", "ANIMATION"]
    | None = "GENERAL",
    export_copyright: str = "",
    export_image_format: typing.Literal["AUTO", "JPEG"] | None = "AUTO",
    export_texture_dir: str = "",
    export_keep_originals: bool | None = False,
    export_texcoords: bool | None = True,
    export_normals: bool | None = True,
    export_draco_mesh_compression_enable: bool | None = False,
    export_draco_mesh_compression_level: int | None = 6,
    export_draco_position_quantization: int | None = 14,
    export_draco_normal_quantization: int | None = 10,
    export_draco_texcoord_quantization: int | None = 12,
    export_draco_color_quantization: int | None = 10,
    export_draco_generic_quantization: int | None = 12,
    export_tangents: bool | None = False,
    export_materials: typing.Literal["EXPORT", "PLACEHOLDER", "NONE"] | None = "EXPORT",
    export_colors: bool | None = True,
    use_mesh_edges: bool | None = False,
    use_mesh_vertices: bool | None = False,
    export_cameras: bool | None = False,
    export_selected: bool | None = False,
    use_selection: bool | None = False,
    use_visible: bool | None = False,
    use_renderable: bool | None = False,
    use_active_collection: bool | None = False,
    export_extras: bool | None = False,
    export_yup: bool | None = True,
    export_apply: bool | None = False,
    export_animations: bool | None = True,
    export_frame_range: bool | None = True,
    export_frame_step: int | None = 1,
    export_force_sampling: bool | None = True,
    export_nla_strips: bool | None = True,
    export_def_bones: bool | None = False,
    export_current_frame: bool | None = False,
    export_skins: bool | None = True,
    export_all_influences: bool | None = False,
    export_morph: bool | None = True,
    export_morph_normal: bool | None = True,
    export_morph_tangent: bool | None = False,
    export_lights: bool | None = False,
    export_displacement: bool | None = False,
    will_save_settings: bool | None = False,
    filter_glob: str = "*.glb;*.gltf",
):
    """Export scene as glTF 2.0 file

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param export_format: Format, Output format and embedding options. Binary is most efficient, but JSON (embedded or separate) may be easier to edit later

    GLB
    glTF Binary (.glb) -- Exports a single file, with all data packed in binary form. Most efficient and portable, but more difficult to edit later.

    GLTF_SEPARATE
    glTF Separate (.gltf + .bin + textures) -- Exports multiple files, with separate JSON, binary and texture data. Easiest to edit later.

    GLTF_EMBEDDED
    glTF Embedded (.gltf) -- Exports a single file, with all data packed in JSON. Less efficient than binary, but easier to edit later.
        :type export_format: typing.Literal['GLB','GLTF_SEPARATE','GLTF_EMBEDDED'] | None
        :param ui_tab: ui_tab, Export setting categories

    GENERAL
    General -- General settings.

    MESHES
    Meshes -- Mesh settings.

    OBJECTS
    Objects -- Object settings.

    ANIMATION
    Animation -- Animation settings.
        :type ui_tab: typing.Literal['GENERAL','MESHES','OBJECTS','ANIMATION'] | None
        :param export_copyright: Copyright, Legal rights and conditions for the model
        :type export_copyright: str
        :param export_image_format: Images, Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web applications due to the smaller file size

    AUTO
    Automatic -- Save PNGs as PNGs and JPEGs as JPEGs. If neither one, use PNG.

    JPEG
    JPEG Format (.jpg) -- Save images as JPEGs. (Images that need alpha are saved as PNGs though.) Be aware of a possible loss in quality.
        :type export_image_format: typing.Literal['AUTO','JPEG'] | None
        :param export_texture_dir: Textures, Folder to place texture files in. Relative to the .gltf file
        :type export_texture_dir: str
        :param export_keep_originals: Keep original, Keep original textures files if possible. WARNING: if you use more than one texture, where pbr standard requires only one, only one texture will be used. This can lead to unexpected results
        :type export_keep_originals: bool | None
        :param export_texcoords: UVs, Export UVs (texture coordinates) with meshes
        :type export_texcoords: bool | None
        :param export_normals: Normals, Export vertex normals with meshes
        :type export_normals: bool | None
        :param export_draco_mesh_compression_enable: Draco mesh compression, Compress mesh using Draco
        :type export_draco_mesh_compression_enable: bool | None
        :param export_draco_mesh_compression_level: Compression level, Compression level (0 = most speed, 6 = most compression, higher values currently not supported)
        :type export_draco_mesh_compression_level: int | None
        :param export_draco_position_quantization: Position quantization bits, Quantization bits for position values (0 = no quantization)
        :type export_draco_position_quantization: int | None
        :param export_draco_normal_quantization: Normal quantization bits, Quantization bits for normal values (0 = no quantization)
        :type export_draco_normal_quantization: int | None
        :param export_draco_texcoord_quantization: Texcoord quantization bits, Quantization bits for texture coordinate values (0 = no quantization)
        :type export_draco_texcoord_quantization: int | None
        :param export_draco_color_quantization: Color quantization bits, Quantization bits for color values (0 = no quantization)
        :type export_draco_color_quantization: int | None
        :param export_draco_generic_quantization: Generic quantization bits, Quantization bits for generic coordinate values like weights or joints (0 = no quantization)
        :type export_draco_generic_quantization: int | None
        :param export_tangents: Tangents, Export vertex tangents with meshes
        :type export_tangents: bool | None
        :param export_materials: Materials, Export materials

    EXPORT
    Export -- Export all materials used by included objects.

    PLACEHOLDER
    Placeholder -- Do not export materials, but write multiple primitive groups per mesh, keeping material slot information.

    NONE
    No export -- Do not export materials, and combine mesh primitive groups, losing material slot information.
        :type export_materials: typing.Literal['EXPORT','PLACEHOLDER','NONE'] | None
        :param export_colors: Vertex Colors, Export vertex colors with meshes
        :type export_colors: bool | None
        :param use_mesh_edges: Loose Edges, Export loose edges as lines, using the material from the first material slot
        :type use_mesh_edges: bool | None
        :param use_mesh_vertices: Loose Points, Export loose points as glTF points, using the material from the first material slot
        :type use_mesh_vertices: bool | None
        :param export_cameras: Cameras, Export cameras
        :type export_cameras: bool | None
        :param export_selected: Selected Objects, Export selected objects only
        :type export_selected: bool | None
        :param use_selection: Selected Objects, Export selected objects only
        :type use_selection: bool | None
        :param use_visible: Visible Objects, Export visible objects only
        :type use_visible: bool | None
        :param use_renderable: Renderable Objects, Export renderable objects only
        :type use_renderable: bool | None
        :param use_active_collection: Active Collection, Export objects in the active collection only
        :type use_active_collection: bool | None
        :param export_extras: Custom Properties, Export custom properties as glTF extras
        :type export_extras: bool | None
        :param export_yup: +Y Up, Export using glTF convention, +Y up
        :type export_yup: bool | None
        :param export_apply: Apply Modifiers, Apply modifiers (excluding Armatures) to mesh objects -WARNING: prevents exporting shape keys
        :type export_apply: bool | None
        :param export_animations: Animations, Exports active actions and NLA tracks as glTF animations
        :type export_animations: bool | None
        :param export_frame_range: Limit to Playback Range, Clips animations to selected playback range
        :type export_frame_range: bool | None
        :param export_frame_step: Sampling Rate, How often to evaluate animated values (in frames)
        :type export_frame_step: int | None
        :param export_force_sampling: Always Sample Animations, Apply sampling to all animations
        :type export_force_sampling: bool | None
        :param export_nla_strips: Group by NLA Track, When on, multiple actions become part of the same glTF animation if they're pushed onto NLA tracks with the same name. When off, all the currently assigned actions become one glTF animation
        :type export_nla_strips: bool | None
        :param export_def_bones: Export Deformation Bones Only, Export Deformation bones only (and needed bones for hierarchy)
        :type export_def_bones: bool | None
        :param export_current_frame: Use Current Frame, Export the scene in the current animation frame
        :type export_current_frame: bool | None
        :param export_skins: Skinning, Export skinning (armature) data
        :type export_skins: bool | None
        :param export_all_influences: Include All Bone Influences, Allow >4 joint vertex influences. Models may appear incorrectly in many viewers
        :type export_all_influences: bool | None
        :param export_morph: Shape Keys, Export shape keys (morph targets)
        :type export_morph: bool | None
        :param export_morph_normal: Shape Key Normals, Export vertex normals with shape keys (morph targets)
        :type export_morph_normal: bool | None
        :param export_morph_tangent: Shape Key Tangents, Export vertex tangents with shape keys (morph targets)
        :type export_morph_tangent: bool | None
        :param export_lights: Punctual Lights, Export directional, point, and spot lights. Uses "KHR_lights_punctual" glTF extension
        :type export_lights: bool | None
        :param export_displacement: Displacement Textures (EXPERIMENTAL), EXPERIMENTAL: Export displacement textures. Uses incomplete "KHR_materials_displacement" glTF extension
        :type export_displacement: bool | None
        :param will_save_settings: Remember Export Settings, Store glTF export settings in the Blender project
        :type will_save_settings: bool | None
        :param filter_glob: filter_glob
        :type filter_glob: str
    """

def obj(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    filter_glob: str = "*.obj;*.mtl",
    use_selection: bool | None = False,
    use_animation: bool | None = False,
    use_mesh_modifiers: bool | None = True,
    use_edges: bool | None = True,
    use_smooth_groups: bool | None = False,
    use_smooth_groups_bitflags: bool | None = False,
    use_normals: bool | None = True,
    use_uvs: bool | None = True,
    use_materials: bool | None = True,
    use_triangles: bool | None = False,
    use_nurbs: bool | None = False,
    use_vertex_groups: bool | None = False,
    use_blen_objects: bool | None = True,
    group_by_object: bool | None = False,
    group_by_material: bool | None = False,
    keep_vertex_order: bool | None = False,
    global_scale: float | None = 1.0,
    path_mode: typing.Literal["AUTO", "ABSOLUTE", "RELATIVE", "MATCH", "STRIP", "COPY"]
    | None = "AUTO",
    axis_forward: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "-Z",
    axis_up: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "Y",
):
    """Save a Wavefront OBJ File

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_glob: filter_glob
        :type filter_glob: str
        :param use_selection: Selection Only, Export selected objects only
        :type use_selection: bool | None
        :param use_animation: Animation, Write out an OBJ for each frame
        :type use_animation: bool | None
        :param use_mesh_modifiers: Apply Modifiers, Apply modifiers
        :type use_mesh_modifiers: bool | None
        :param use_edges: Include Edges
        :type use_edges: bool | None
        :param use_smooth_groups: Smooth Groups, Write sharp edges as smooth groups
        :type use_smooth_groups: bool | None
        :param use_smooth_groups_bitflags: Bitflag Smooth Groups, Same as 'Smooth Groups', but generate smooth groups IDs as bitflags (produces at most 32 different smooth groups, usually much less)
        :type use_smooth_groups_bitflags: bool | None
        :param use_normals: Write Normals, Export one normal per vertex and per face, to represent flat faces and sharp edges
        :type use_normals: bool | None
        :param use_uvs: Include UVs, Write out the active UV coordinates
        :type use_uvs: bool | None
        :param use_materials: Write Materials, Write out the MTL file
        :type use_materials: bool | None
        :param use_triangles: Triangulate Faces, Convert all faces to triangles
        :type use_triangles: bool | None
        :param use_nurbs: Write Nurbs, Write nurbs curves as OBJ nurbs rather than converting to geometry
        :type use_nurbs: bool | None
        :param use_vertex_groups: Polygroups
        :type use_vertex_groups: bool | None
        :param use_blen_objects: OBJ Objects, Export Blender objects as OBJ objects
        :type use_blen_objects: bool | None
        :param group_by_object: OBJ Groups, Export Blender objects as OBJ groups
        :type group_by_object: bool | None
        :param group_by_material: Material Groups, Generate an OBJ group for each part of a geometry using a different material
        :type group_by_material: bool | None
        :param keep_vertex_order: Keep Vertex Order
        :type keep_vertex_order: bool | None
        :param global_scale: Scale
        :type global_scale: float | None
        :param path_mode: Path Mode, Method used to reference paths

    AUTO
    Auto -- Use Relative paths with subdirectories only.

    ABSOLUTE
    Absolute -- Always write absolute paths.

    RELATIVE
    Relative -- Always write relative paths (where possible).

    MATCH
    Match -- Match Absolute/Relative setting with input path.

    STRIP
    Strip Path -- Filename only.

    COPY
    Copy -- Copy the file to the destination path (or subdirectory).
        :type path_mode: typing.Literal['AUTO','ABSOLUTE','RELATIVE','MATCH','STRIP','COPY'] | None
        :param axis_forward: Forward
        :type axis_forward: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
        :param axis_up: Up
        :type axis_up: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
    """

def x3d(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str = "",
    check_existing: bool | None = True,
    filter_glob: str = "*.x3d",
    use_selection: bool | None = False,
    use_mesh_modifiers: bool | None = True,
    use_triangulate: bool | None = False,
    use_normals: bool | None = False,
    use_compress: bool | None = False,
    use_hierarchy: bool | None = True,
    name_decorations: bool | None = True,
    use_h3d: bool | None = False,
    global_scale: float | None = 1.0,
    path_mode: typing.Literal["AUTO", "ABSOLUTE", "RELATIVE", "MATCH", "STRIP", "COPY"]
    | None = "AUTO",
    axis_forward: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "Z",
    axis_up: typing.Literal["X", "Y", "Z", "-X", "-Y", "-Z"] | None = "Y",
):
    """Export selection to Extensible 3D file (.x3d)

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: str
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | None
        :param filter_glob: filter_glob
        :type filter_glob: str
        :param use_selection: Selection Only, Export selected objects only
        :type use_selection: bool | None
        :param use_mesh_modifiers: Apply Modifiers, Use transformed mesh data from each object
        :type use_mesh_modifiers: bool | None
        :param use_triangulate: Triangulate, Write quads into 'IndexedTriangleSet'
        :type use_triangulate: bool | None
        :param use_normals: Normals, Write normals with geometry
        :type use_normals: bool | None
        :param use_compress: Compress, Compress the exported file
        :type use_compress: bool | None
        :param use_hierarchy: Hierarchy, Export parent child relationships
        :type use_hierarchy: bool | None
        :param name_decorations: Name decorations, Add prefixes to the names of exported nodes to indicate their type
        :type name_decorations: bool | None
        :param use_h3d: H3D Extensions, Export shaders for H3D
        :type use_h3d: bool | None
        :param global_scale: Scale
        :type global_scale: float | None
        :param path_mode: Path Mode, Method used to reference paths

    AUTO
    Auto -- Use Relative paths with subdirectories only.

    ABSOLUTE
    Absolute -- Always write absolute paths.

    RELATIVE
    Relative -- Always write relative paths (where possible).

    MATCH
    Match -- Match Absolute/Relative setting with input path.

    STRIP
    Strip Path -- Filename only.

    COPY
    Copy -- Copy the file to the destination path (or subdirectory).
        :type path_mode: typing.Literal['AUTO','ABSOLUTE','RELATIVE','MATCH','STRIP','COPY'] | None
        :param axis_forward: Forward
        :type axis_forward: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
        :param axis_up: Up
        :type axis_up: typing.Literal['X','Y','Z','-X','-Y','-Z'] | None
    """
