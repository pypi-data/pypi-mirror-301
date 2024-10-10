import typing
import collections.abc
import typing_extensions
from . import add_mesh_torus
from . import anim
from . import assets
from . import bmesh
from . import bone_selection_sets
from . import clip
from . import connect_to_output
from . import console
from . import constraint
from . import file
from . import freestyle
from . import geometry_nodes
from . import image
from . import image_as_planes
from . import mesh
from . import node
from . import node_editor
from . import object
from . import object_align
from . import object_quick_effects
from . import object_randomize_transform
from . import presets
from . import rigidbody
from . import screen_play_rendered_anim
from . import sequencer
from . import spreadsheet
from . import userpref
from . import uvcalc_follow_active
from . import uvcalc_lightmap
from . import uvcalc_transform
from . import vertexpaint_dirt
from . import view3d
from . import wm
from . import world

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def register(): ...
def unregister(): ...
