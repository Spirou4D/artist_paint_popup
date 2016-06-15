# -*- coding: utf8 -*-
# python
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
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {"name": "Artist Paint Popup",
            "author": "CDMJ, Spirou4D",
            "version": (1, 0),
            "blender": (2, 77, 0),
            "location": "",
            "description": "shortcut menu for Artist Panel addon",
            "warning": "",
            "wiki_url": "",
            "category": "Paint"}

import bpy
from bpy.types import   AddonPreferences,\
                        Menu,\
                        Panel,\
                        UIList,\
                        Operator
import math
import os
SEP = os.sep

#-------------------------------------------New: get the addon preferences
def get_addon_prefs_corr():
    Addons = bpy.context.user_preferences.addons
    for i in Addons:
        if Addons.find('artist_paint_panel') != -1:
            key = Addons.find('artist_paint_panel')
            break
        elif Addons.find('artist_paint_panel-master') != -1:
            key = Addons.find('artist_paint_panel-master')
            break
        else:
            return -1
    return Addons[key].preferences

def pollAPT(self, context):
    scene = context.scene
    obj =  context.active_object
    empty = scene.maincanvas_is_empty
    main_canvas_name = ""

    if not(empty):
        if scene.artist_paint is not None:
            if len(scene.artist_paint) !=0:
                for main_canvas in scene.artist_paint:
                    main_canvas_name = (main_canvas.filename)[:-4]
    else:
        return False

    if obj is not None:
        return obj.name == main_canvas_name

class canvasPopup(Operator):
    bl_idname = "artist_paint.popup"
    bl_label = "Artist Paint Popup"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        A = obj is not None
        B = context.mode == 'PAINT_TEXTURE'
        C = context.mode == 'EDIT_CURVE'
        return A and (B or C)

    def check(self, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=240)

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        #"ARTIST_PAINT_OT_popup"
        addon_prefs = get_addon_prefs_corr()
        if addon_prefs == -1:
            print("You must install the 'Artist Paint Panel' Add-On, please")
            return {'FINISHED'}

        CustomAngle  = str(addon_prefs['customAngle'])
        toolsettings = context.tool_settings
        ipaint = toolsettings.image_paint

        buttName_1 = CustomAngle +"°"
        buttName_2 = CustomAngle +"°"

        layout = self.layout
        layout.active = context.scene.UI_is_activated

        row = layout.row(align = True)
        row1 = row.split(align=True)
        row1.label("Shading")
        row2 = row.split(align=True)
        row2.operator("artist_paint.multitexture",
                    text='', icon="RENDERLAYERS")
        row2.operator("artist_paint.glsl",
                    text='', icon="RADIO")
        row2.scale_x = 1.00

        box = layout.box()
        col = box.column()
        col.label("Objects Masking Tools")
        col.operator("artist_paint.trace_selection",
                    text = "Mask from Gpencil",
                    icon = 'OUTLINER_OB_MESH')

        col.separator()                             #empty line

        col.operator("artist_paint.curve_2dpoly",
                    text = "Make Vector Contour",
                    icon = 'PARTICLE_POINT')

        row = col.row(align = True)
        row.operator("artist_paint.curve_unwrap",
                    text = "To Mesh Mask",
                    icon = 'OUTLINER_OB_MESH')
        row.operator("artist_paint.inverted_mask",
                    text = "To Inverted Mesh Mask",
                    icon = 'MOD_TRIANGULATE')

        col.separator()                             #empty line

        col.prop(ipaint, "use_stencil_layer",
                                text="Use stencil mask")
        if ipaint.use_stencil_layer == True:
            cel = col.column(align = True)
            cel.template_ID(ipaint, "stencil_image")
            cel.operator("image.new", text="New").\
                                        gen_context = 'PAINT_STENCIL'
            row = cel.row(align = True)
            row.prop(ipaint, "stencil_color", text="")
            row.prop(ipaint, "invert_stencil",
                        text="Invert the mask",
                        icon='IMAGE_ALPHA')

        col.separator()                             #empty line

        box = layout.box()                        #CANVAS FRAME CONSTRAINT
        col = box.column(align = True)
        row = col.row(align = True)
        row1 = row.split(align=True)
        row1.label(text="Mirror")
        row1.scale_x = 0.60
        row.separator()
        row2 = row.split(align=True)
        row2.prop(ipaint, "use_symmetry_x", text="Hor.", toggle=True)
        row2.prop(ipaint, "use_symmetry_y", text="Ver.", toggle=True)
        row2.scale_x = 0.70
        row.separator()
        row3 = row.split(align=True)
        row3.operator("artist_paint.set_symmetry_origin",
                    text="New", icon='VIEW3D_VEC')
        row4 = row.split(align=True)
        row4.operator("artist_paint.reset_origin",
                    text="", icon='RECOVER_AUTO')

        col.separator()

        row = col.row(align = True)
        row.operator("artist_paint.canvas_horizontal",
                    text="Canvas Flip Horizontal",
                    icon='ARROW_LEFTRIGHT')
        row.operator("artist_paint.canvas_vertical",
                    text = "Canvas Flip Vertical",
                    icon = 'FILE_PARENT')


        row = col.row(align = True)                    #ROTATION
        row.label(text="Rotation")
        row.prop(context.scene, "canvas_in_frame" ,
                                    text="Frame Constraint")
        row.enabled = pollAPT(self, context)

        row = col.row(align = True)
        row.operator("artist_paint.rotate_ccw_15",
                    text = "Rotate -" + buttName_1, icon = 'TRIA_LEFT')
        row.operator("artist_paint.rotate_cw_15",
                    text = "Rotate +" + buttName_2, icon = 'TRIA_RIGHT')

        row = col.row(align = True)
        row.operator("artist_paint.rotate_ccw_90",
                    text = "Rotate 90° CCW", icon = 'PREV_KEYFRAME')
        row.operator("artist_paint.rotate_cw_90",
                    text = "Rotate 90° CW", icon = 'NEXT_KEYFRAME')

        col.operator("artist_paint.canvas_resetrot",
                    text = "Reset Rotation", icon = 'CANCEL')



def register():
    bpy.utils.register_module(__name__)

    km_list = ['3D View']
    for i in km_list:
        sm = bpy.context.window_manager
        km = sm.keyconfigs.default.keymaps[i]
        kmi = km.keymap_items.new('artist_paint.popup', 'W', 'PRESS', alt=True)

def unregister():
    bpy.utils.unregister_module(__name__)

    km_list = ['3D View']
    for i in km_list:
        sm = bpy.context.window_manager
        km = sm.keyconfigs.default.keymaps[i]
        for kmi in (kmi for kmi in km.keymap_items \
                            if (kmi.idname == "artist_paint.popup")):
            km.keymap_items.remove(kmi)


if __name__ == "__main__":
    register()
