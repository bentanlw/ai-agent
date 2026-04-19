import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_work_dir, directory))
        valid_target_dir = (
            os.path.commonpath([abs_work_dir, target_dir]) == abs_work_dir
        )
        if not valid_target_dir:
            #            print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            #            print(f'Error: "{directory}" is not a directory')
            return f'Error: "{directory}" is not a directory'
        files_info = []
        with os.scandir(target_dir) as d:
            #            print(f"Result for '{directory}':")
            for f in d:
                files_info.append(
                    f"- {f.name}: file_size={f.stat().st_size}, is_dir={f.is_dir()}"
                )
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: Standard Library encountered {e}"
