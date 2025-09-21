import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    # Combine the working directory with the specified file path
    full_path = os.path.join(working_directory, file_path)

    # Get absolute paths for comparison
    absolute_path_working_dir = os.path.abspath(working_directory)
    absolute_full_path = os.path.abspath(full_path)

    # Ensure the specified file is within the working directory
    if not absolute_full_path.startswith(absolute_path_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
    # Check if the file exists
    if not os.path.isfile(absolute_full_path):
        return f'Error: File "{file_path}" not found.'
    
    # Check if the file is a Python file
    if not absolute_full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Run the Python file and capture output
        completed_process = subprocess.run(
            ["python", absolute_full_path] + args,
            capture_output=True,
            cwd=working_directory,
            text=True,
            check=True,
            timeout=30
        )

        if completed_process.returncode != 0:
            return f"Process exited with {completed_process.returncode}"

        if completed_process.stdout:
            return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        
    except subprocess.TimeoutExpired:
        return f"Error: Execution of {file_path} timed out after 30 seconds."
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)