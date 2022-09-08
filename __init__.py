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
import sys
import importlib

modulesFullNames = {}

modulesNames = ['prefs',
                'cto_purge',
                ]

for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

if 'DEBUG_MODE' in sys.argv:
    import os
    import time
    os.system("cls")
    timestr = time.strftime("%Y-%m-%d %H:%M:%S")
    print('---------------------------------------')
    print('-------------- RESTART ----------------')
    print('---------------------------------------')
    print(timestr, __name__ + ": registered")
    print()
    sys.argv.remove('DEBUG_MODE')

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
