import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # if file_path outside working_directory, return error
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))

        if not os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # if file_path is not a file, return error
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # read fiel and return contents as string, read only up to 10000 characters from file using .read(), check if file larger than limit - try to read one more char than limit, if empty then EOF. if larger than show error

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string

    # except block to catch all standard library error
    except Exception as e:
        return f'Error: Standard Library encountered {e}'
