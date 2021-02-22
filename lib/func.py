# -*- coding: utf-8 -*-

"""
Description: project static functions

"""

# => IMPORTS
import os
import configparser
import shutil
import re


# => PREPARE CONFIG PARSERs
config = configparser.ConfigParser()

CONFIG_FILENAME = './config/config.ini'
PREFIXES_FILENAME = 'prefixes.txt'

SORT_SECTION = ' SORT '
PATHS_SECTION = ' PATHS '
LENGTH = 0

paths_variables = []
sorting_variables = []


# => READ A CONFIG FILE
def get_config():
    config.read(CONFIG_FILENAME)
    return config


# => SETUP FUNCTION
def setup():
    def get_desktop_path():

        # => RETURNS FULL DESKTOP PATH
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        return desktop_path

    desktop = get_desktop_path()

    # => GET CONFIG
    data = get_config()

    try:
        DIR_NAME = data[' NAMES ']['sorting_dir']

    except KeyError:
        DIR_NAME = 'ProjectSorting'

    PATH = rf"{desktop}\{DIR_NAME}"

    # => ADD VARIABLE TO GLOBAL LIST OF CONFIG
    # => VARIABLES TO SET WHEN THERE'S SECTION ERROR
    paths_variables.append(['sorting_dir_path', PATH])

    # => CHECK IF DIRECTORY IS NOT SET
    if not os.path.isdir(PATH):
        # => CREATE DIR
        os.mkdir(desktop + '/' + DIR_NAME)

        print(f"[+] Created directory {DIR_NAME} at {PATH}")


# => CREATE SORTING SECTIONS IN CONFIG.INI FILE
def set_sorting_sections(sections: list):
    data = get_config()

    # => IF SORT SECTION EXISTS IN CONFIG.INI FILE - CREATE NEW
    if SORT_SECTION not in data.sections():
        data.add_section(SORT_SECTION)

    sorting_variables.append(['length', str(len(sections))])

    # => SET ALL VARS FROM LIST
    for var in sorting_variables:
        data.set(SORT_SECTION, var[0], var[1])

    # => FOR EVERY SECTION USER PASSED - SET IT IN CONFIG FILE
    set_values(SORT_SECTION, sections, var_name='sort')

    # => SAVE TO FILE
    with open(CONFIG_FILENAME, 'w') as config_file:
        config.write(config_file)


# => SET PATHS TO THE DIRECTORIES WHERE PROJECTS WILL BE STORED
def set_sorting_paths(paths: list):
    # => PATHS SECTION DOES NOT EXISTS IN FILE
    data = get_config()

    paths_variables.append(['length', str(len(paths))])

    if PATHS_SECTION not in data.sections():
        data.add_section(PATHS_SECTION)

    # => SET ALL VARS FROM LIST
    for var in paths_variables:
        data.set(PATHS_SECTION, var[0], var[1])

    # => FOR EVERY PATH USER PASSED - SET IT IN ARRAY IN CONFIG FILE

    set_values(PATHS_SECTION, paths, var_name='path')

    data[' GLOBAL ']['set'] = str(1)

    # => SAVE TO FILE
    with open(CONFIG_FILENAME, 'w') as config_file:
        config.write(config_file)


# => SET NEW VALUES OR CHANGE IN GIVEN SECTION FOR GIVEN VAR_NAME
def set_values(section: str, array: list, var_name: str):
    variables = config.items(section)

    for var in variables:
        if var[0].startswith(var_name):
            config[section][var[0]] = ''

    for index, value in enumerate(array):
        try:
            # => IF EXISTS
            config[section][f'{var_name}[{index}]'] = value
            print(f'[+] Set new value {value} for {var_name}[{index}] in {section} section')

        except KeyError:
            # => IF NOT EXISTS
            config.set(section, f'{var_name}[{index}]', value)
            print(f"[+] Created var {var_name}[{index}] with value {value} in {section} section")


# => RETURNS ALL PROJECTS EXISTING IN CREATED BY PROGRAM PROJECT-SORTING DIRECTORY
def get_dir_names():
    data = get_config()
    PATH = data[PATHS_SECTION]['sorting_dir_path']

    return [d for d in os.listdir(PATH) if os.path.isdir(os.path.join(PATH, d))]


# => READ ARRAYS
def get_array(section: str, length: int, name: str, data):
    return [data[section][f'{name}[{i}]'] for i in range(length)]


# => SORT ALL PROJECTS SAVED IN SORTING DIRECTORY
def sort_projects_name(projects: list):
    data = get_config()

    # => GET LENGTH
    SORT_LENGTH = data[SORT_SECTION]['length']
    PATHS_LENGTH = data[PATHS_SECTION]['length']

    # => GET ARRAYS
    prefixes = get_array(SORT_SECTION, int(SORT_LENGTH), 'sort', data)
    paths = get_array(PATHS_SECTION, int(PATHS_LENGTH), 'path', data)

    result = []

    # FIND OUT WHICH PROJECT GOES TO THE GIVEN DIR SET IN CONFIG FILE
    for project in projects:
        for prefix in prefixes:
            if project.startswith(prefix):
                index = prefixes.index(prefix)

                # => INSERT HERE A FUNCTION THAT CUTS A PROJECT NAME AND RENAMES IT OR WHERE'S LATER

                # => APPEND A PATH WHERE TO MOVE A PROJECT AND PROJECT NAME
                result.append(
                    [
                        paths[index],
                        project
                    ]
                )

                break

            else:
                print(f"[-] Project {project} doesn't have his prefix set ")

    return result


# => MOVE GIVEN PROJECT TO A GIVEN DIRECTORY SET IN PATH
def move_project(project, path):
    data = get_config()
    PATH = data[PATHS_SECTION]['sorting_dir_path']
    PATH = rf'{PATH}\{project}'
    COUNT = 0

    # => IF GIVEN DIRECTORY AT PATH path EXISTS
    if os.path.isdir(path):

        # => MOVE FILE
        print(f'[+] Trying to move {project} to {path}')
        shutil.move(PATH, path)
        COUNT += 1
        print(f'[+] Moved {project} to {path}')

    else:
        print(f'[-] Directory at path {path} is not a directory or not exists - creating ')

        # => CREATE AND MOVE AGAIN
        os.mkdir(path)

        print(f'[+] Trying to move again {project} to {path}')
        shutil.move(PATH, path)
        print(f'[+] Moved {project} to {path}')

    return COUNT


# => CREATE HELPFUL PREFIXES.TXT FILE WITH ALL THE PREFIXES AND PATH USER SET BEFORE
def create_prefixes_txt():
    data = get_config()
    DIRECTORY_PATH = data[PATHS_SECTION]['sorting_dir_path']
    PATH = fr'{DIRECTORY_PATH}\{PREFIXES_FILENAME}'

    # => GET LENGTH
    SORT_LENGTH = data[SORT_SECTION]['length']
    PATHS_LENGTH = data[PATHS_SECTION]['length']

    prefixes = get_array(SORT_SECTION, int(SORT_LENGTH), 'sort', data)
    paths = get_array(PATHS_SECTION, int(PATHS_LENGTH), 'path', data)

    with open(PATH, 'w') as file:
        file.write('[+] Project Sorting Prefixes and Paths [+]')
        file.write('\n\n')

        for prefix, path in zip(prefixes, paths):
            file.write(f'[+]\tPrefix: {prefix}\tPath: {path}\n')


def start():
    print("[+] Project Sorter 1.0.0 \n\n")
    print("[+] Set your prefixes and paths...\n")


# => CHECK IF A GIVEN STRING CONTAINS ILLEGAL CHARS
def check_character(string: str):
    EXPRESSION = r"#%&{}<>*? " + '"' + "$!'@:+`|="
    regular_e = re.compile(EXPRESSION)

    if regular_e.search(string): return True
    else: return False


# => SET ALL PREFIXES AND PATHS
def set_all():
    prefixes = []
    paths = []

    yes = ['y', 'Y', 'yes', 'Yes', 'YES']
    no = ['n', 'N', 'no', 'No', 'NO']
    e = ['e', 'E']

    while True:
        print("\n[+] TYPE e TO END")
        prefix = input("[+] Type your starting project name prefix (Example: prefix_ProjectName): ")
        path = input(f"[+] Paste your path to the directory where project with {prefix} prefix will be moving later: ")

        if prefix in e:
            return prefixes, paths

        # => CHECK PREFIX AND PATH LOOKING FOR INVALID CHARS
        if check_character(prefix):
            print("[-] Invalid char (prefix must be typed like with file-naming rules)")
            continue

        if check_character(path):
            print("[-] Invalid path ")
            continue

        agreed = input(f"[?] Project names that "
                       f"starts with {prefix} will be moving to the {path} dir. Are you sure? (y/n)")

        if agreed in yes:
            prefixes.append(prefix)
            paths.append(path)

        elif agreed in no:
            print("[+] Deleting... ")
            continue

        else:
            print("[-] This is not a option! ")

    return prefixes, paths


# => HELP MSG
def help_msg():
    print("\n[+] You can now leave a script and let it run in background, when clicking in a right bottom corner")
    print("[+] there will be shown some options. You can kill this process in the Task Manager\n")
