import os
from google.genai import types
from config import MAX_CHARACTERS

def get_file_content(working_directory, file_path):
    
    # Combine the working directory with the specified file path
    full_path = os.path.join(working_directory, file_path)

    # Get absolute paths for comparison
    absolute_path_working_dir = os.path.abspath(working_directory)
    absolute_full_path = os.path.abspath(full_path)

    # Ensure the specified file is within the working directory
    if not absolute_full_path.startswith(absolute_path_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
    # Check if the file exists
    if not os.path.isfile(absolute_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Read and return the file content
        with open(absolute_full_path, 'r') as file:
            content = file.read(MAX_CHARACTERS)
            if len(content) == MAX_CHARACTERS:
                content += "\n\n" + f"[...File {absolute_full_path} truncated to at {MAX_CHARACTERS} characters]."
        
        return content
    
    except Exception as e:
        return f'Error: {str(e)}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARACTERS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)