import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file relative to the working directory, returns the result of the run",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File name of the python file to be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        # if file_path outside working_directory, return error
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

        if not os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # if file_path is not a file, return error
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # if file name doesn't end with .py, return error
        if os.path.splitext(target_file)[1] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=abs_work_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output_string = []

        if result.returncode != 0:
            output_string.append(f"Process exited with code {result.returncode}")
        if (not result.stdout) and (not result.stderr):
            output_string.append("No output produced")
        if result.stdout:
            output_string.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_string.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output_string)
    except Exception as e:
        return f"Error: executing Python file: {e}"
