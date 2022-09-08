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

'''
Custom Transform Orientations Purge add-on
'''
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

# v1.0.0 (09.05.2022) - by Marcelo M. Marques
# Added: initial creation

# --- ### Imports
import bpy

from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty, BoolProperty


def update_filter(self, context):
    # removes invalid characters entered by the user: comma and spaces
    strFilter = ""
    strValue = self.CTO_FILTER[:]
    for char in strValue:
        if char != " " and char != ",":
            strFilter += char
    if self.CTO_FILTER != strFilter:
        self.CTO_FILTER = strFilter


class CtoPurgePreferences(AddonPreferences):
    bl_idname = __package__

    CTO_FILTER: StringProperty(
        name="",
        description="Character(s) that if found in the Custom Transform Orientation name it will\n" +
                    "prevent that row to be purged by this addon. Each character is individually\n" +
                    "evaluated, so if *ANY* one is found in the name the row will not be purged.\n" +
                    "** Be aware that the comma character (,) does not work with this addon **",
        default="_",
        maxlen=32,
        update=update_filter
    )

    CTO_SPACE: BoolProperty(
        name="Filter if SPACES",
        description="Indicates that if a SPACE character is found in the Custom Transform Orientation name\n" +
                    "it will prevent that row to be purged by this addon.",
        default=False
    )

    void_spacer: BoolProperty()

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, 'void_spacer', icon='BLANK1', text="", emboss=False)
        col = row.column(align=True)
        col.scale_y = 0.8
        col.label(text="- Below you can configure a list of characters that if any is present in a Custom Transform Orientation (CTO) name")
        col.label(text="it will prevent this addon to delete that CTO row from the Blender's Transform Orientation dropdown list.  This way")
        col.label(text="you can create a personal filter to keep some but not all CTOs in your project file.  The additional checkbox allows")
        col.label(text='you to indicate that a "SPACE" character must also be considered as a filter character.')
        col.label(text=" ")
        col.label(text='- So for example, if you add to the list below the character "@" and you have that character added to the name of')
        col.label(text="one or more CTOs that you want to keep around, this addon will not delete those CTOs from the Blender's Transform")
        col.label(text="Orientation dropdown list when the Purge Custom Orientation pushbutton gets pressed by you.")
        col.label(text=" ")
        col.label(text="Note: Any of these configured filter characters can be used in any position within the CTO's name to work as a filter.")
        col.label(text="It does not have to be used as a prefix or suffix;  if found any place in the CTO's name it will work alright.")

        layout.separator()
        split = layout.split(factor=0.25)
        splat = split.row()
        splat.alignment = "RIGHT"
        splat.label(text="Filter character(s)")
        splat = split.row()
        splat.alignment = "LEFT"
        splat.prop(self, 'CTO_FILTER', text="")

        split = layout.split(factor=0.25)
        splat = split.row()
        splat.alignment = "RIGHT"
        splat.label(text="Filter if SPACES ")
        splat = split.row()
        splat.alignment = "LEFT"
        splat.prop(self, 'CTO_SPACE', text="")

        layout.separator()
        box = layout.box()
        row = box.row(align=True)
        box.scale_y = 0.5
        box.label(text=" Additional information and Acknowledge:")
        box.label(text="")
        box.label(text=" - This addon prepared and packaged by Marcelo M Marques (mmmrqs@gmail.com)")
        box.label(text="   (updates at https://github.com/mmmrqs/cto_purge)")
        box.label(text="")
        box.label(text=" Special thanks to: 'iyadahmed' Iyad Ahmed for his posts on the community forums,")
        box.label(text=" which have been crucial for making this addon.")
        box.label(text="")


# Registration
def register():
    bpy.utils.register_class(CtoPurgePreferences)


def unregister():
    bpy.utils.unregister_class(CtoPurgePreferences)


if __name__ == '__main__':
    register()
