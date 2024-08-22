import bpy
from .main import register as main_register, unregister as main_unregister

bl_info = {
    "name": "UE Texture Importer",
    "description": "Imports Unreal Engine JSON materials and automatically sets up corresponding textures in Blender.",
    "author": "KingxJulz",
    "version": (1, 0, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > PSK / PSA",
    "warning": "This requires the PSK / PSA addon in the N-Panel/Sidebar",
    "wiki_url": "https://github.com/Julz876/FModel-Auto-Texture/blob/main/README.md",
    "tracker_url": "https://github.com/Julz876/FModel-Auto-Texture/issues",
    "category": "Import-Export",
}

def register():
    main_register()  # Register the main script components
    # Additional registration logic can go here

def unregister():
    main_unregister()  # Unregister the main script components
    # Additional unregistration logic can go here

if __name__ == "__main__":
    register()
