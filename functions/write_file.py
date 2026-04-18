import os

def write_file(working_directory, file_path, content):
    try:
        # if file_path outside working_directory, return error
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

        if not os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # if file_path points to existing directory, return error 
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: Standard Library encountered {e}'
