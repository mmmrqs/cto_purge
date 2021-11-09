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
           "description": "Purge all custom transformation orientations",
           "author": "Marcelo M. Marques (script by iyadahmed)",
           "version": (1, 0, 0),
           "blender": (2, 80, 75),
           "location": "View3D > Transformation orientation panel",
           "support": "COMMUNITY",
           "category": "3D View",
           "doc_url": "https://github.com/mmmrqs/cto_purge",
           "tracker_url": "https://github.com/mmmrqs/cto_purge/issues"
           }

# --- ### Change log

# v1.0.0 (11.10.2021) - by Marcelo M. Marques
# Added: initial creation

# --- ### Imports
import bpy

class CTO_OT_Purge(bpy.types.Operator):
    bl_idname = "object.cto_purge"
    bl_label = "Purge Custom Orientations  "
    bl_description = "Purge all custom transformation orientations"
    bl_options = {"REGISTER"}

    def execute(self, context):
        try:
            bpy.context.scene.transform_orientation_slots[0].type = ""
        except Exception as inst:
            transforms = str(inst)[str(inst).find("in (")+4:-1]
            transform_list = transforms.split(", ")
            for type in transform_list[6:]:
                try:
                    bpy.context.scene.transform_orientation_slots[0].type = type[1:-1]
                    bpy.ops.transform.delete_orientation()
                except Exception as e:
                    pass
        return {'FINISHED'}


def extend_transfo_pop_up(self, context):
    layout = self.layout
    row = layout.row()
    row.operator(CTO_OT_Purge.bl_idname, text="Purge Custom Orientations  ", icon='TRASH')
    row.separator()
    row.separator()


def register():
    bpy.utils.register_class(CTO_OT_Purge)
    bpy.types.VIEW3D_PT_transform_orientations.append(extend_transfo_pop_up)


def unregister():
    bpy.types.VIEW3D_PT_transform_orientations.remove(extend_transfo_pop_up)
    bpy.utils.unregister_class(CTO_OT_Purge)


if __name__ == '__main__':
    register()
