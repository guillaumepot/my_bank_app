import subprocess

# Exécuter pip freeze et capturer la sortie
pip_freeze_output = subprocess.check_output(['pip', 'freeze'], text=True)

# Ouvrir le fichier requirements.txt en mode écriture
with open('requirements.txt', 'w') as req_file:
    # Itérer sur chaque ligne de la sortie de pip freeze
    for line in pip_freeze_output.splitlines():
        # Vérifier si la ligne contient '@ file' et extraire la partie pertinente
        if '@ file' in line:
            package_version = line.split('@')[0]
            req_file.write(package_version + '\n')
        else:
            req_file.write(line + '\n')