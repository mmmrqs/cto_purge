# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# --- ### Header
bl_info = {"name": "CTO Purge",
           "description": "Purge all custom transform orientations",
           "author": "Marcelo M. Marques (based on script by 'iyadahmed' Iyad Ahmed)",
           "version": (1, 0, 2),
           "blender": (2, 80, 75),
           "location": "View3D > Transform Orientations panel",
           "support": "COMMUNITY",
           "category": "3D View",
           "doc_url": "https://github.com/mmmrqs/cto_purge",
           "tracker_url": "https://github.com/mmmrqs/cto_purge/issues"
           }

# --- ### Change log

# v1.0.2 (09.05.2022) - by Marcelo M. Marques
# Added: configuration options to filter out custom transform orientations
# Fixed: issue caused by special characters in the names

# v1.0.1 (11.11.2021) - by Marcelo M. Marques
# Chang: just minor clean up

# v1.0.0 (11.10.2021) - by Marcelo M. Marques
# Added: initial creation

# --- ### Imports
import bpy
import os
from bpy_extras.io_utils import ImportHelper


class CTO_OT_Purge(bpy.types.Operator):
    """ This is a workaround for this issue:
        https://blender.stackexchange.com/questions/136019/blender-2-8-api-how-to-get-a-list-of-custom-transform-orientations/196080#196080
    """
    bl_idname = "object.cto_purge"
    bl_label = "Purge Custom Orientations  "
    bl_description = "Purge all custom transform orientations.\nCheck addon preferences for filter out options"
    bl_options = {"REGISTER"}

    def CTO_FILTER(self):
        """ Indicates which character(s) must be considered as a filter out option. """
        try:
            if __package__.find(".") != -1:
                package = __package__[0:__package__.find(".")]
            else:
                package = __package__
            strFilter = bpy.context.preferences.addons[package].preferences.CTO_FILTER
        except Exception as e:
            strFilter = ""
        return (strFilter)

    def CTO_SPACE(self):
        """ Indicates if SPACE character must also be considered as a filter out option. """
        try:
            if __package__.find(".") != -1:
                package = __package__[0:__package__.find(".")]
            else:
                package = __package__
            bolSpace = bpy.context.preferences.addons[package].preferences.CTO_SPACE
        except Exception as e:
            bolSpace = False
        return (bolSpace)

    def execute(self, context):
        # Try to set transform orientation and catch error message
        try:
            bpy.context.scene.transform_orientation_slots[0].type = ""
        except Exception as inst:
            # Extract a list of transform orientations from error message
            # if we tried to set transform_orientation_slots[0].type to a non existent value, we get error message similar to the one below:
            # > TypeError: bpy_struct: item.attr = val: enum "" not found in ('GLOBAL', 'LOCAL', 'NORMAL', 'GIMBAL', 'VIEW', 'CURSOR', 'Cube', 'Cube.001', 'Cube.002')
            # where each element from the 7th position forward corresponds to one of the custom transform orientations (in the above example: 'Cube', 'Cube.001' and 'Cube.002')
            transforms = str(inst).split("not found in")[1][3:-2].replace("', '", ",").split(",")
            strFilters = self.CTO_FILTER().strip().upper()
            if self.CTO_SPACE():
                strFilters += " "
            # Exclude first 6 "default" transform orientations
            for type in transforms[6:]:
                purge = True
                for char in strFilters:
                    # Will filter out (skip) any row that has any of the filter characters in its name
                    if type.upper().find(char) >= 0:
                        purge = False
                        break
                if purge:
                    # Try to delete this custom transform orientation
                    try:
                        bpy.context.scene.transform_orientation_slots[0].type = type
                        bpy.ops.transform.delete_orientation()
                    except Exception as e:
                        pass
        return {'FINISHED'}


class CTO_OT_Dummy(bpy.types.Operator):
    bl_idname = "object.cto_dummy"
    bl_label = ""
    bl_description = "There is nothing here"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        return {'FINISHED'}


def extend_transfo_pop_up(self, context):
    layout = self.layout
    row = layout.row(align=False)
    row.operator(CTO_OT_Purge.bl_idname, icon='TRASH')
    row.operator(CTO_OT_Dummy.bl_idname, icon='BLANK1', emboss=False)


def register():
    bpy.utils.register_class(CTO_OT_Dummy)
    bpy.utils.register_class(CTO_OT_Purge)
    bpy.types.VIEW3D_PT_transform_orientations.append(extend_transfo_pop_up)


def unregister():
    bpy.types.VIEW3D_PT_transform_orientations.remove(extend_transfo_pop_up)
    bpy.utils.unregister_class(CTO_OT_Purge)
    bpy.utils.unregister_class(CTO_OT_Dummy)


if __name__ == '__main__':
    register()
