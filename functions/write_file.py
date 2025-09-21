import os
from google.genai import types

def write_file(working_directory, file_path, content):
        
    # Combine the working directory with the specified directory
    full_path = os.path.join(working_directory, file_path)

    # Get absolute paths for comparison
    absolute_path_working_dir = os.path.abspath(working_directory)
    absolute_path_directory = os.path.abspath(full_path)

    # Ensure the specified directory is within the working directory
    if not absolute_path_directory.startswith(absolute_path_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Check if the directory exists, create if not
    dir_name = os.path.dirname(absolute_path_directory)
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except Exception as e:
            return f"Error creating directory '{dir_name}': {str(e)}"
    
    try:
        with open(full_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file '{file_path}': {str(e)}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)