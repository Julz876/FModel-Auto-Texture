import bpy
import json
import os
from .normal_converter import create_normal_converter
import logging

logging.basicConfig(level=logging.INFO)

def remove_nodes(node_tree):
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)
        logging.info("scene material cleared!")

def find_textures(base_path, textures):
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            for texture_type, texture_name in textures.items():
                expected_texture_name = f"{texture_name}.png"
                if filename.startswith(expected_texture_name):
                    abs_texture_path = os.path.join(root, filename)
                    return abs_texture_path, texture_type
    return None, None

def setup_material(context, json_file_path, texture_directories):
    if not json_file_path or not os.path.isfile(json_file_path):
        print("Error: JSON file path is not valid or not provided.")
        return {'CANCELLED'}
    
    if not texture_directories:
        print("Error: Texture directories path is not provided.")
        return {'CANCELLED'}

    create_normal_converter()

    opengl_directx_flip = 1.0

    with open(json_file_path, 'r') as json_file:
        try:
            mat_data = json.load(json_file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file '{json_file_path}': {e}")
            mat_data = {}

    textures = mat_data.get("Textures", {})
    textures = {key: value.split('/')[-1].split('.')[0] for key, value in textures.items()}

    material_name = os.path.splitext(os.path.basename(json_file_path))[0]

    print(f"Material Name: {material_name}")

    material = bpy.data.materials.get(material_name)

    if material:
        material.use_nodes = True
        nodes = material.node_tree.nodes
        remove_nodes(material.node_tree)
    
        principled_node = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        separate_rgb_node = material.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
        separate_rgb_node.location = (-576, -487)
        separate_rgb_node3 = material.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
        separate_rgb_node3.location = (-805, 112)
        mix_rgb_node = material.node_tree.nodes.new(type='ShaderNodeMixRGB')
        mix_rgb_node.location = (-524, 124)
        mix_rgb_node2 = material.node_tree.nodes.new(type='ShaderNodeMixRGB')
        mix_rgb_node2.location = (-224, 124)
        invert_node = material.node_tree.nodes.new(type='ShaderNodeInvert')
        invert_node.location = (-577, -346)
        normal_map_node = material.node_tree.nodes.new(type='ShaderNodeNormalMap')
        normal_map_node.location = (-233, -824)
        rgb_node = material.node_tree.nodes.new(type='ShaderNodeRGB')
        rgb_node.location = (-533, -124)

        normal_converter = nodes.get('Normal_Convert')
        
        if not normal_converter:
            create_normal_converter()
            normal_converter = nodes.new('ShaderNodeGroup')
            normal_converter.node_tree = bpy.data.node_groups['Normal_Convert']
            normal_converter.location = (-593, -810)

        principled_node.inputs[7].default_value = 0.008
        principled_node.inputs[8].default_value = (1.0, 0.2, 0.1)
        principled_node.inputs[11].default_value = 0.8
        mix_rgb_node.blend_type = 'MULTIPLY'
        mix_rgb_node2.blend_type = 'MULTIPLY'
        mix_rgb_node.use_clamp = True
        mix_rgb_node2.use_clamp = True
        rgb_node.outputs[0].default_value = (1.0, 0.230, 0.120, 1.0)
        material.node_tree.links.new(rgb_node.outputs[0], principled_node.inputs[2])

        y_coordinate = 550
        
        material_output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        material.node_tree.links.new(principled_node.outputs[0], material_output_node.inputs[0])
        material_output_node.location.x = 300

        print("Textures Dictionary:", textures)

        for texture_type, texture_name in textures.items():
            expected_texture_name = f"{texture_name}.png"

            found = False
            for texture_directory in texture_directories.split(";"):
                abs_texture_path, found_texture_type = find_textures(texture_directory, {texture_type: texture_name})

                if abs_texture_path:
                    print(f"Texture found: {abs_texture_path}")
                    found = True

                    texture_node = material.node_tree.nodes.new(type="ShaderNodeTexImage")
                    texture_node.label = f"{material_name}_{found_texture_type}"
                    texture_node.location.x = -1200
                    texture_node.location.y = y_coordinate

                    y_coordinate -= 290

                    try:
                        texture_node.image = bpy.data.images.load(abs_texture_path)

                        if found_texture_type in ["Normal Map", "ORM Map", "Alpha Mask Texture", "PM_SpecularMasks"]:
                            texture_node.image.colorspace_settings.name = 'Non-Color'

                        print(f"Loaded texture: {abs_texture_path}")

                        if found_texture_type == "Diffuse Map":
                            material.node_tree.links.new(texture_node.outputs[0], mix_rgb_node.inputs[1])
                            material.node_tree.links.new(mix_rgb_node.outputs[0], mix_rgb_node2.inputs[1])
                            material.node_tree.links.new(separate_rgb_node.outputs[0], mix_rgb_node2.inputs[2])
                            material.node_tree.links.new(mix_rgb_node2.outputs[0], principled_node.inputs[0])
                        elif found_texture_type == "SSS Map":
                            material.node_tree.links.new(texture_node.outputs[0], principled_node.inputs[3])
                        elif found_texture_type == "ORM Map":
                            material.node_tree.links.new(texture_node.outputs[0], separate_rgb_node.inputs[0])
                            material.node_tree.links.new(texture_node.outputs[1], invert_node.inputs[1])
                            material.node_tree.links.new(invert_node.outputs[0], principled_node.inputs[7])
                            material.node_tree.links.new(separate_rgb_node.outputs[1], principled_node.inputs[9])
                            material.node_tree.links.new(separate_rgb_node.outputs[2], principled_node.inputs[6])
                        elif found_texture_type == "Normal Map":
                            material.node_tree.links.new(texture_node.outputs[0], normal_converter.inputs[0])
                            material.node_tree.links.new(normal_converter.outputs[0], normal_map_node.inputs[1])
                            normal_converter.inputs[1].default_value = opengl_directx_flip
                            material.node_tree.links.new(normal_map_node.outputs[0], principled_node.inputs[22])
                        elif found_texture_type == "Alpha Mask Texture":
                            material.node_tree.links.new(texture_node.outputs[0], separate_rgb_node3.inputs[0])
                            material.node_tree.links.new(texture_node.outputs[0], mix_rgb_node.inputs[2])
                            material.node_tree.links.new(separate_rgb_node3.outputs[0], mix_rgb_node.inputs[0])
                        else:
                            print(f"Unhandled texture type: {found_texture_type}")

                        print("Number of links in material:", len(material.node_tree.links))
                        print("Nodes in material:", len(material.node_tree.nodes))
                    except RuntimeError as e:
                        print(f"Error loading image '{abs_texture_path}': {e}")

                    break

            if not found:
                print(f"No matching texture found for material '{material_name}' and type '{texture_type}'.")

    else:
        print(f"Material '{material_name}' not found in Blender.")

class MATERIAL_OT_setup(bpy.types.Operator):
    bl_idname = "material.setup_ue_texture"
    bl_label = "Setup UE Texture"

    def execute(self, context):
        json_file_path = context.scene.json_file_path
        texture_directories = context.scene.texture_directories

        if not json_file_path or not os.path.isfile(json_file_path):
            self.report({'ERROR'}, "JSON file path is not valid or not provided.")
            return {'CANCELLED'}
        
        if not texture_directories:
            self.report({'ERROR'}, "Texture directories path is not provided.")
            return {'CANCELLED'}

        setup_material(context, json_file_path, texture_directories)
        return {'FINISHED'}

class Combine_PT_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PSK / PSA"
    bl_label = "Import textures from JSON"

    def draw(self, context):
        layout = self.layout
        layout.label(text='How to Use')
        layout.prop(context.scene, "json_file_path")
        layout.prop(context.scene, "texture_directories")
        layout.operator(MATERIAL_OT_setup.bl_idname, icon='MESH_DATA')

def register():
    bpy.utils.register_class(MATERIAL_OT_setup)
    bpy.utils.register_class(Combine_PT_Panel)
    bpy.types.Scene.json_file_path = bpy.props.StringProperty(name="JSON File Path", subtype='FILE_PATH')
    bpy.types.Scene.texture_directories = bpy.props.StringProperty(name="Texture Directories", subtype='DIR_PATH')

def unregister():
    bpy.utils.unregister_class(MATERIAL_OT_setup)
    bpy.utils.unregister_class(Combine_PT_Panel)
    del bpy.types.Scene.json_file_path
    del bpy.types.Scene.texture_directories

if __name__ == "__main__":
    register()
