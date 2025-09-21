import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # Combine the working directory with the specified directory
    full_path = os.path.join(working_directory, directory)

    # Get absolute paths for comparison
    absolute_path_working_dir = os.path.abspath(working_directory)
    absolute_full_path = os.path.abspath(full_path)

    # Ensure the specified directory is within the working directory
    if not absolute_full_path.startswith(absolute_path_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check if the directory exists
    if not os.path.isdir(absolute_full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:    
        # Output information about files in the directory
        dir_info_list = []
        for dirofile in os.listdir(absolute_full_path):
            dirofile_path = os.path.join(absolute_full_path, dirofile)
            is_dir = os.path.isdir(dirofile_path)

            if os.path.isdir(dirofile_path):
                dir_info_list.append(f"Directory: {dirofile}")
            else:
                size = os.path.getsize(dirofile_path)
                dir_info_list.append(f"File: {dirofile}, Size: {size} bytes")

        return "\n".join(dir_info_list)
    
    except Exception as e:
        return f'Error: {str(e)}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)