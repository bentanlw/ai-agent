import os
import subprocess


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

        run_py_file = subprocess.run(
            command, capture_output=True, text=True, timeout=30
        )
        output_string = []

        if run_py_file.returncode:
            output_string.append(f"Process exited with code {run_py_file.returncode}")
        if (not run_py_file.stdout) and (not run_py_file.stderr):
            output_string.append("No output produced")

        output_string.append(f"STDOUT: {run_py_file.stdout}")
        output_string.append(f"STDERR: {run_py_file.stderr}")
        return "\n".join(output_string)
    except Exception as e:
        return f"Error: executing Python file: {e}"
