import bpy
import json
import os
import sys
import random

from .normal_converter import create_normal_converter

def setup_material(material_name, json_file_path, texture_directories, common_prefix):
    create_normal_converter()  # Create node group when setting up the material

# Ensuring the normal converter is created and available
create_normal_converter()

def remove_nodes(node_tree):
    # Remove all nodes from the node tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

def find_textures(base_path, textures):
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            for texture_type, texture_name in textures.items():
                expected_texture_name = f"{texture_name}.png"
                if filename.startswith(expected_texture_name):
                    abs_texture_path = os.path.join(root, filename)
                    print(f"Found: {filename}")
                    print(f"Expected: {expected_texture_name}")
                    print(f"Path: {abs_texture_path}")
                    return abs_texture_path, texture_type
    return None, None

# Replace 'your_material_file.json' with the actual path to your JSON file
json_file_path = your_material_file.json

# Common prefix for relative texture paths
# Dumped game directory
common_prefix = "H:/Dumped Games/CallistoProtocol"

# Possible texture directories
texture_directories = [
    "H:/Dumped Games/CallistoProtocol/Game/Characters/Player/Textures",
    "H:/Dumped Games/CallistoProtocol/Game/Characters/Elias/Textures",
    "H:/Dumped Games/CallistoProtocol/Game/Characters/Shared",
]

#Change for the type or normal conversion, 0.0 for opengl and 1.0 for directx
opengl_directx_flip = 1.0

# Load JSON data
with open(json_file_path, 'r') as json_file:
    try:
        mat_data = json.load(json_file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{json_file_path}': {e}")
        mat_data = {}

# Extract textures dictionary
textures = mat_data.get("Textures", {})

# Filter out unnecessary information in texture names
textures = {key: value.split('/')[-1].split('.')[0] for key, value in textures.items()}

# Get the base name of the JSON file (excluding the extension)
material_name = os.path.splitext(os.path.basename(json_file_path))[0]

print(f"Material Name: {material_name}")

# Find the material in Blender based on its name
material = bpy.data.materials.get(material_name)

if material:
    # Ensure we're using nodes in the material
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # Clear existing nodes in the material
    remove_nodes(material.node_tree)
    
    # Create Shader nodes
    principled_node = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    separate_rgb_node = material.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
    separate_rgb_node.location = (-576, -487)
    #separate_rgb_node2 = material.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
    #separate_rgb_node2.location = (-769, -878)
    separate_rgb_node3 = material.node_tree.nodes.new(type='ShaderNodeSeparateRGB')
    separate_rgb_node3.location = (-805, 112)
    #combine_rgb_node = material.node_tree.nodes.new(type='ShaderNodeCombineRGB')
    #combine_rgb_node.location = (-400, -858)
    mix_rgb_node = material.node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_node.location = (-524, 124)
    mix_rgb_node2 = material.node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_node2.location = (-224, 124)
    invert_node = material.node_tree.nodes.new(type='ShaderNodeInvert')
    invert_node.location = (-577, -346)
    #invert_node2 = material.node_tree.nodes.new(type='ShaderNodeInvert')
    #invert_node2.location = (-593, -810)
    normal_map_node = material.node_tree.nodes.new(type='ShaderNodeNormalMap')
    normal_map_node.location = (-233, -824)
    rgb_node = material.node_tree.nodes.new(type='ShaderNodeRGB')
    rgb_node.location = (-533, -124)

    # Getting the Normal Converter node group
    normal_converter = nodes.get('Normal_Convert')
    
    if not normal_converter:
        create_normal_converter()
        normal_converter = nodes.new('ShaderNodeGroup')
        normal_converter.node_tree = bpy.data.node_groups['Normal_Convert']
        normal_converter.location = (-593, -810)


    # Principled BSDF Shader Default
    principled_node.inputs["Subsurface"].default_value = 0.008  # Set Subsurface to 0.008
    principled_node.inputs["Subsurface Radius"].default_value = (1.0, 0.2, 0.1)  # Set Subsurface Radius to 1.0, 0.2, 0.1
    principled_node.inputs["Subsurface Anisotropy"].default_value = 0.8  # Set Subsurface Anisotropy to 0.8
    mix_rgb_node.blend_type = 'MULTIPLY'
    mix_rgb_node2.blend_type = 'MULTIPLY'
    mix_rgb_node.use_clamp = True
    mix_rgb_node2.use_clamp = True
    rgb_node.outputs[0].default_value = (1.0, 0.230, 0.120, 1.0)
    material.node_tree.links.new(rgb_node.outputs[0], principled_node.inputs[2])

    # Y-coordinate for aligning nodes
    y_coordinate = 550
    
    # Create a Material Output node
    material_output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    
    # Connect the Principled BSDF shader node to the Material Output node
    material.node_tree.links.new(principled_node.outputs[0], material_output_node.inputs[0])
    material_output_node.location.x = 300

    # Print the textures dictionary
    print("Textures Dictionary:", textures)

# Iterate through possible texture directories and search for textures
found_textures = []
for texture_type, texture_name in textures.items():
    expected_texture_name = f"{texture_name}.png"

    found = False
    for texture_directory in texture_directories:
        base_directory = os.path.join(common_prefix, texture_directory)

        print(f"Searching in directory: {base_directory}")

        abs_texture_path, found_texture_type = find_textures(base_directory, {texture_type: texture_name})

        if abs_texture_path:
            print(f"Texture found: {abs_texture_path}")
            found = True

            # Add the corresponding node to the material node tree
            node_type = "ShaderNodeTexImage"
            texture_node = material.node_tree.nodes.new(type=node_type)

            # Set the label for the texture node
            texture_node.label = f"{material_name}_{found_texture_type}"

            # Set the location for each texture node on the Y-axis
            texture_node.location.x = -1200
            texture_node.location.y = y_coordinate

            # Increment the Y-coordinate for the next node
            y_coordinate -= 290  # Adjust this value based on your desired spacing

            # Load the image
            try:
                texture_node.image = bpy.data.images.load(abs_texture_path)

                # Set color space to 'None' for Normal Map and ORM textures
                if found_texture_type == "Normal Map" or found_texture_type == "ORM Map":
                    texture_node.image.colorspace_settings.name = 'Non-Color'
                
                if found_texture_type == "Alpha Mask Texture" or found_texture_type == "PM_SpecularMasks":
                    texture_node.image.colorspace_settings.name = 'Non-Color'

                print(f"Loaded texture: {abs_texture_path}")

                # Connect the nodes based on your intended material appearance
                if found_texture_type == "Diffuse Map":
                    #material.node_tree.links.new(texture_node.outputs[0], principled_node.inputs[0])
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
                    #material.node_tree.links.new(separate_rgb_node2.outputs[0], combine_rgb_node.inputs[0])
                    #material.node_tree.links.new(separate_rgb_node2.outputs[1], invert_node2.inputs[1])
                    #material.node_tree.links.new(invert_node2.outputs[0], combine_rgb_node.inputs[1])
                    #material.node_tree.links.new(separate_rgb_node2.outputs[2], combine_rgb_node.inputs[2])
                    #material.node_tree.links.new(combine_rgb_node.outputs[0], normal_map_node.inputs[1])
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

            break  # Stop searching if the texture is found

    # If no texture is found, print a message
    if not found:
        print(f"No matching texture found for material '{material_name}' and type '{texture_type}'.")
else:
    print(f"Material '{material_name}' not found in Blender.")


# UI panel Testing
class Combine_PT_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PSK / PSA"
    bl_label = "Import textures from Json"

    #--- draw ---#
    def draw(self, context):
        layout = self.layout
        layout.label(text='How to Use')
        layout.label(text='1. Select material json file')
        layout.label(text='2. Select textures directory')
        layout.label(text='3. Select 2 armatures')
        layout.label(text='4. Click the button below')        
        layout.operator(Importjson_OT_Run_Button.bl_idname, icon='MESH_DATA')
