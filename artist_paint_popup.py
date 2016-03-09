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
            "blender": (2, 76, 0),
            "location": "",
            "description": "shortcut menu for Artist Panel addon",
            "warning": "",
            "wiki_url": "",
            "category": "Paint"}

import bpy
from bpy.types import Menu, Panel, UIList, Operator
from rna_prop_ui import PropertyPanel

class canvasPopup(Operator):
    bl_idname = "artist_paint.popup"
    bl_label = "Artist Paint Popup"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        brush = context.tool_settings.image_paint.brush
        ob = context.active_object
        return (brush is not None and ob is not None)

    def check(self, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=160)

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        #"ARTIST_PAINT_OT_popup"
        tool_settings = context.tool_settings
        ipaint = context.tool_settings.image_paint

        layout = self.layout
        col = layout.column()
        col.separator()
        col.prop(ipaint, "use_stencil_layer",
                                text="Use stencil mask")

        if ipaint.use_stencil_layer == True:
            col.template_ID(ipaint, "stencil_image")
            col.operator("image.new", text="New").\
                                gen_context = 'PAINT_STENCIL'
            col.prop(ipaint, "invert_stencil",
                                text="Invert the mask")
        row = col.row(align=True)
        row.label("Mirror")
        row = col.row(align=True)
        row.operator("artist_paint.canvas_horizontal",
                text="Canvas Flip Horizontal",icon='ARROW_LEFTRIGHT')
        row.operator("artist_paint.canvas_vertical",
                text = "Canvas Flip Vertical", icon = 'FILE_PARENT')
        row = col.row(align=True)
        row.label("Rotation")
        row = col.row(align=True)
        row.operator("artist_paint.rotate_ccw_15",
                text = "Rotate 15° CCW", icon = 'TRIA_LEFT')
        row.operator("artist_paint.rotate_cw_15",
                text = "Rotate 15° CW", icon = 'TRIA_RIGHT')
        row = col.row(align=True)
        row.operator("artist_paint.rotate_ccw_90",
                text = "Rotate 90° CCW", icon = 'PREV_KEYFRAME')
        row.operator("artist_paint.rotate_cw_90",
                text = "Rotate 90° CW", icon = 'NEXT_KEYFRAME')
        col.separator()
        col.operator("artist_paint.canvas_resetrot",
                text = "Reset Rotation", icon = 'CANCEL')



def register():
    bpy.utils.register_class(canvasPopup)

    km_list = ['Image Paint']
    for i in km_list:
        sm = bpy.context.window_manager
        km = sm.keyconfigs.default.keymaps[i]
        kmi = km.keymap_items.new('artist_paint.popup', 'C', 'PRESS')

def unregister():
    bpy.utils.unregister_class(canvasPopup)

    km_list = ['Image Paint']
    for i in km_list:
        sm = bpy.context.window_manager
        km = sm.keyconfigs.default.keymaps[i]
        for kmi in (kmi for kmi in km.keymap_items if (kmi.idname == "artist_paint.popup")):
            km.keymap_items.remove(kmi)



if __name__ == "__main__":
    register()
