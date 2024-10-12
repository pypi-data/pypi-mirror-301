import os
import re
import click
import json
import shutil
import ctypes
import win32com.client
from packaging.version import Version
from dotenv import dotenv_values

ERROR_COLOR = '\033[91m' # Red
WARNING_COLOR = '\033[93m' # Yellow
SUCCESS_COLOR = '\033[92m' # Green
RESET_COLOR = '\033[0m' # Reset

CONFIG_PATH = r'.exe-index.config' # Default config path

@click.command()
def new_index():
    '''
    Create a new index folder.
    '''
    obj = load_config() 
    INDEX_PATH = obj.get('index-path')
    EXE_INDEX_SETTING_FILE = os.path.join(INDEX_PATH, CONFIG_PATH)

    if not os.path.exists(INDEX_PATH):
        click.echo(f'{ERROR_COLOR}Index path does not exist.{RESET_COLOR}')
        return

    if os.path.exists(EXE_INDEX_SETTING_FILE):
        click.echo(f'{ERROR_COLOR}Index already exists, please run `exe-index publish` to publish the current exe to the index.{RESET_COLOR}')
        return

    # Create the index file and make it hidden windows
    with open(EXE_INDEX_SETTING_FILE, 'w') as f:
        f.write(json.dumps({}, indent=4))
    os.system(f'attrib +h "{EXE_INDEX_SETTING_FILE}"')
    click.echo(f'{SUCCESS_COLOR}Index created at \'{INDEX_PATH}\'.{RESET_COLOR}')

@click.group()
def cli():
    pass

@cli.command()
def init():
    '''
    Create a new config file with default values, if the file already exists, only missing values will be added.
    '''
    obj = load_config()
    with open(CONFIG_PATH, 'w') as f:
        f.write(json.dumps(obj, indent=4))
    click.echo(f'{SUCCESS_COLOR}Config file created at \'{CONFIG_PATH}\'.{RESET_COLOR}')

@cli.command()
def publish():
    '''
    Publish the current exe to the index.
    '''
    # Load the config file
    obj = load_config()
    EXE_NAME = obj.get('exe-name')
    EXE_PATH = obj.get('exe-path')
    EXE_VERSION = obj.get('exe-version')
    INDEX_PATH = obj.get('index-path')
    
    # Check if any values are missing
    ERROR_LIST = []
    if not EXE_NAME: ERROR_LIST.append('exe-name')
    if not EXE_PATH: ERROR_LIST.append('exe-path')
    if not EXE_VERSION: ERROR_LIST.append('exe-version')
    if not INDEX_PATH: ERROR_LIST.append('index-path')
    if ERROR_LIST: 
        click.echo(f'{ERROR_COLOR}Missing values in config file: {", ".join(ERROR_LIST)}{RESET_COLOR}')
        return
    
    EXE_PATH = os.path.abspath(EXE_PATH)
    INDEX_PATH = os.path.abspath(INDEX_PATH)

    # Check if the index exists
    EXE_INDEX_SETTING_FILE = os.path.join(INDEX_PATH, CONFIG_PATH)
    if not os.path.exists(EXE_INDEX_SETTING_FILE):
        click.echo(f'{ERROR_COLOR}Index \'{INDEX_PATH}\' does not exist, please run `exe-new-index` to create a new index.{RESET_COLOR}')
        return

    upload_file(EXE_NAME, EXE_PATH, EXE_VERSION, INDEX_PATH)

@cli.command()
def verify():
    '''
    Verify the current exe is exposed in the index.
    '''    
    # Load the config file
    obj = load_config()
    EXE_NAME = obj.get('exe-name')
    EXE_PATH = obj.get('exe-path')
    EXE_VERSION = obj.get('exe-version')
    INDEX_PATH = obj.get('index-path')
    
    # Check if any values are missing
    ERROR_LIST = []
    if not EXE_NAME: ERROR_LIST.append('exe-name')
    if not EXE_PATH: ERROR_LIST.append('exe-path')
    if not EXE_VERSION: ERROR_LIST.append('exe-version')
    if not INDEX_PATH: ERROR_LIST.append('index-path')
    if ERROR_LIST: 
        click.echo(f'{ERROR_COLOR}Missing values in config file: {", ".join(ERROR_LIST)}{RESET_COLOR}')
        return
    
    EXE_PATH = os.path.abspath(EXE_PATH)
    INDEX_PATH = os.path.abspath(INDEX_PATH)

    # Check if the index exists
    EXE_INDEX_SETTING_FILE = os.path.join(INDEX_PATH, CONFIG_PATH)
    if not os.path.exists(EXE_INDEX_SETTING_FILE):
        click.echo(f'{ERROR_COLOR}Index \'{INDEX_PATH}\' does not exist, please run `exe-new-index` to create a new index.{RESET_COLOR}')
        return
    
    package_path = os.path.join(INDEX_PATH, f'_{EXE_NAME}')
    upload_target = os.path.join(INDEX_PATH, f'{EXE_NAME}.lnk')
    expose_stable_version(upload_target, package_path)


def upload_file(exe_name: str, exe_path: str, exe_version: str, index_path: str):
    '''
    Upload the exe to the index.
    '''
    click.echo(f'Uploading \'{exe_name}\' v{exe_version} to index \'{index_path}\'...')
    package_path = os.path.join(index_path, f'_{exe_name}')
    upload_target = os.path.join(index_path, f'{exe_name}.lnk')
    upload_versioned_target = os.path.join(package_path, f'{exe_name}_v{exe_version}.exe')

    # Check if package path exists and create it if it does not
    if not os.path.exists(package_path):
        os.makedirs(package_path)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(package_path, FILE_ATTRIBUTE_HIDDEN)
    
    # Check if the same version of the exe is already in the index
    exe_uid_files = os.listdir(package_path)
    if f'{exe_name}_v{exe_version}.exe' in exe_uid_files:
        click.echo(f'{ERROR_COLOR}Version {exe_version} of exe \'{exe_name}\' already exists in the index.{RESET_COLOR}')
        return
    
    # Copy the exe to the index
    shutil.copy(exe_path, upload_versioned_target)
    click.echo(f'{SUCCESS_COLOR}Uploaded \'{exe_name}\' v{exe_version} to index \'{index_path}\'.{RESET_COLOR}')
    expose_stable_version(upload_target, package_path)

def expose_stable_version(upload_target: str, package_path: str):
    '''
    Expose the stable version of the exe.
    '''
    click.echo(f'Exposing stable version of exe...')
    exe_list = os.listdir(package_path)
    exe_list = [{
        'name': x,
        'version': x.split('_v')[1].split('.exe')[0],
    } for x in exe_list]
    exe_list = sorted(exe_list, key=lambda x: Version(x['version']), reverse=True)
    exe_list = [x for x in exe_list if Version(x['version']).is_prerelease == False]
    stable_exe = exe_list[0]["name"]
    if os.path.exists(upload_target): os.remove(upload_target)
    
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(upload_target)
    shortcut.Targetpath = os.path.join(package_path, stable_exe)
    shortcut.save()

    # shutil.copy(os.path.join(package_path, stable_exe), upload_target)
    click.echo(f'{SUCCESS_COLOR}Stable version \'{stable_exe}\' exposed.{RESET_COLOR}')

@cli.command()
def config():
    '''
    Print the current config file values. Usefull for debugging.
    '''
    obj = load_config()
    click.echo('Current Config:')
    click.echo(json.dumps(obj, indent=4))

def load_config():
    obj: dict = {
        'exe-name': None,
        'exe-path': None,
        'exe-version': None,
        'index-path': None,
        'thrid-party-configs': {
            'ppm-config-path': '.proj.config',
            },
        }
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            _obj: dict = json.loads(f.read())
            obj = {**obj, **_obj}

    ppm_config = obj.get('thrid-party-configs', {}).get('ppm-config-path')
    if ppm_config and os.path.exists(ppm_config):
        try:
            with open(ppm_config, 'r') as f:
                file_text = f.read()
                _obj: dict = json.loads(ppm_parse(file_text, json.loads(file_text)))
                obj = {**obj, **{
                    "exe-name": _obj.get("exe-index", {}).get("exe-name") or obj.get("exe-name"),
                    "exe-version": _obj.get("exe-index", {}).get("exe-version") or obj.get("exe-version"),
                    "exe-path": _obj.get("exe-index", {}).get("exe-path") or obj.get("exe-path"),
                    "index-path": _obj.get("exe-index", {}).get("index-path") or obj.get("index-path"),
                }}
        except ImportError:
            click.echo(f'{WARNING_COLOR}Python Project Manager not found, skipping config file.{RESET_COLOR}')

    return obj

def ppm_parse(string: str, dict_obj: dict) -> str:
    '''
    Literally the same as the `parse` function in the ppm package 3.0.2, but with a few modifications.
    '''
    # Parse dynamic values
    def parse_match(match: re.Match[str]) -> str:
        return parse_dynamic_value(match.group(0), dict_obj)
    
    # Parse dynamic values recursively
    def parse_dynamic_value(dynamic_value, dict, recursive_check: list = None) -> str:
        if isinstance(dynamic_value, str) and dynamic_value.startswith('%env:') and dynamic_value.endswith('%'):
            try:
                dynamic_value = dynamic_value[1:-1] # Remove the %'s
                env_key = dynamic_value.split(':')[1] # Get the env key
                return dotenv_values('.env')[env_key] # Get the env value
            except KeyError:
                return dynamic_value

        if recursive_check is None: # Initialize the recursive check list
            recursive_check = []

        # Check for circular references
        if dynamic_value in recursive_check:
            raise Exception(
                f'Circular reference detected: {' => '.join(recursive_check)} => {dynamic_value}')
        recursive_check.append(dynamic_value) # Add the current dynamic value to the recursive check list

        # Get the value from the dict
        dot_walk = dynamic_value[1:-1].split('.')
        for key in dot_walk:
            dict = dict[key]

        # If the value is a string, parse it
        if isinstance(dict, str) and dict.startswith('%') and dict.endswith('%'):
            return parse_dynamic_value(dict, dict_obj, recursive_check)
        return dict

    string = re.sub(r'%.*?%', parse_match, string)

    return string