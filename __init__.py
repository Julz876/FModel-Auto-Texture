import bpy
from .main_script import register as main_register, unregister as main_unregister

bl_info = {
    "name": "UE Texture Importer",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "category": "Import-Export",
    "author": "KingJulz",
}

def register():
    main_register()  # Register the main script components
    # Additional registration logic can go here

def unregister():
    main_unregister()  # Unregister the main script components
    # Additional unregistration logic can go here

if __name__ == "__main__":
    register()
