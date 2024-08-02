import subprocess

# Execute pip freeze
pip_freeze_output = subprocess.check_output(['pip', 'freeze'], text=True)

# Open requirements.txt (read mode) and write the output of pip freeze
with open('requirements.txt', 'w') as req_file:

    for line in pip_freeze_output.splitlines():
        if '@ file' in line:
            package_version = line.split('@')[0]
            req_file.write(package_version + '\n')
        else:
            req_file.write(line + '\n')