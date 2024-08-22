# UE Texture Importer for Blender

### Version: 1.0.0
### Author: KingJulz

## Overview

The **UE Texture Importer** is a Blender addon designed to simplify the process of importing and setting up textures from Unreal Engine JSON material files. This tool automates the creation of materials in Blender, ensuring they are properly configured based on the texture maps specified in the JSON file. The add-on includes a custom normal map converter, enabling you to switch between OpenGL and DirectX normal map formats with ease.

Note: This addon requires the PSK / PSA toolbar addon to be installed and enabled in Blender.

## Features

- **JSON Material Import:** Automatically loads material settings from a JSON file and creates a Blender material with the specified textures.
- **Texture Handling:** Supports various texture types, including Diffuse, ORM (Occlusion, Roughness, Metalness), Normal, and Alpha Mask textures.
- **Normal Map Conversion:** A custom node group for converting normal maps between OpenGL and DirectX formats.
- **Customizable Settings:** Easily toggle between OpenGL and DirectX normal maps using a simple slider.
- **User Interface Panel:** A convenient UI panel in the 3D View for quick access to the texture import functionality.

## Installation

1. Download the repository.
2. Open Blender and click `Edit > Preferences > Add-ons`.
3. Click `Install` and select the downloaded ZIP file or extracted folder containing the addon files.
4. Enable the addon by checking the box next to "UE Texture Importer".
5. Ensure that the PSK / PSA addon is installed and enabled, showing in the sidebar/N-Panel

## Usage

1. **Select Material JSON File:**
   - The addon expects a JSON file containing material definitions, including texture paths.
   - Place the JSON file in the appropriate directory.
   
2. **Select Textures Directory:**
   - Make sure the texture images are in one of the specified directories.
   - The addon searches the provided paths to locate and link the correct textures.

3. **Adjust Normal Map Settings (Optional):**
   - The add-on includes an option to flip the Y-axis for normal maps based on whether you’re using OpenGL or DirectX.
   - This can be controlled by adjusting the `opengl_directx_flip` value in the script.

4. **Run the Importer:**
   - Use the UI panel in the 3D Viewport to start the import process. The addon will create a material with the specified textures and apply it to the selected object.

## Code Structure

- `__init__.py`: Handles the registration and unregistration of the addon.
- `normal_converter.py`: Contains the function for creating the Normal Map conversion node group.
- `main.py`: Main script for loading textures, creating materials, and managing the Blender UI panel.

## Requirements

- Blender 3.0 or later.
- A JSON file with material definitions and corresponding texture paths.

## Troubleshooting

- **Textures Not Found:** Ensure that the textures are in the correct directories as defined in the script.
- **Material Not Created:** Double-check the JSON file format and the material name in Blender.

## Contributing

Feel free to submit issues or pull requests to contribute to this project. Contributions are always welcome!

## Contact

For any questions or support, please contact me.
