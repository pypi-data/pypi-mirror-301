
import re
import python_project_manager

version = python_project_manager.Config.get('version')
if version is None:
    raise ValueError('Version not found in \'.proj.config\'')

toml_path = 'pyproject.toml'
with open(toml_path, 'r') as file:
    toml = file.read()
version_regex = r'version = ".*?"'
toml = re.sub(version_regex, f'version = "{version}"', toml)
with open(toml_path, 'w') as file:
    file.write(toml)
