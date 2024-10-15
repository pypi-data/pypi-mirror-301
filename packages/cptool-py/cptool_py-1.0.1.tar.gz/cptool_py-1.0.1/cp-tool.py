import os
import re
import sys

TEMPLATE_PATH = os.path.join(os.path.expanduser('~'), '.local/share/cp-tool/template')
DEFAULT_EXTENSION = '.cpp'

def main(args):
    cur_directory = os.getcwd()

    # Check if args contains an extension
    extension = DEFAULT_EXTENSION
    if len(args) > 1 and (args[-1].startswith('-e=') or args[-1].startswith('--extension=')):
        extension = '.' + args[-1].split('=')[1].lstrip('.')
        args = args[:-1]
    
    # Check if template file exists before doing anything
    full_template_path = TEMPLATE_PATH + extension
    ensure_exists(full_template_path)

    # Command for creating contest files
    if len(args) > 3 and args[1] == 'contest' and args[2].isdigit():
        num_problems = int(args[2])
        contest_name = ' '.join(args[3:])
        new_dir = create_contest(cur_directory, contest_name, num_problems, extension)
        print('Contest files created.')
        print_dir(new_dir)
    # Command for creating problem files
    elif len(args) > 2 and args[1] == 'problem':
        problem_name = ' '.join(args[2:])
        new_dir = create_problem(cur_directory, problem_name, extension)
        print('Problem files created.')
        print_dir(new_dir)
    # Command for creating template
    elif len(args) == 3 and args[1] == 'template':
        add_template(cur_directory, ' '.join(args[2:]), extension, True)
        print('Template file created')
    # Help command
    elif len(args) == 2 and args[1] == 'help':
        print_help()
    # Unknown command
    else:
        print('Invalid usage:')
        print_help()

def create_contest(directory, num_problems, name, extension):
    # Create directory with problems: "problem1.cpp", "problem2.cpp", ...
    new_path = create_directory(directory, name)
    for i in range(1, num_problems+1):
        problem_name = 'problem' + str(i)
        add_template(new_path, problem_name, extension)
    return new_path

def create_problem(directory, name, extension):
    new_path = create_directory(directory, name, extension)
    add_template(new_path, name, extension)
    return new_path

def add_template(directory, file_name, extension, override=False):
    # Read template file
    full_template_path = TEMPLATE_PATH + extension
    template_data = ""
    with open(full_template_path, 'r') as f:
        template_data = f.read()

    formatted_file_name = format_name(file_name, extension)
    new_path = os.path.join(directory, formatted_file_name) + extension

    # Write template file
    if not override:
        ensure_not_exists(new_path)
    with open(new_path, 'w') as f:
        f.write(template_data)

def print_help():
    print('Usage: cpt <commands> [args]')
    print('cpt help')
    print('cpt problem <name>')
    print('cpt contest <num_problems> <name>')
    print('cpt template <name>')
    print('--extension=<ext> or -e=<ext> to specify file extension')

def create_directory(directory, directory_name, extension):
    formatted_directory_name = format_name(directory_name, extension)
    joined_path = os.path.join(directory, formatted_directory_name)
    ensure_not_exists(joined_path)
    os.mkdir(joined_path)
    return joined_path

def format_name(name, extension):
    # Replace spaces and remove special characters
    formatted = name.replace(' ', '_')
    formatted = re.sub(r'[^\w]', '', formatted)
    formatted = formatted.rstrip(extension)
    return formatted

def print_dir(dir):
    print('dir=' + dir)

def ensure_exists(path):
    if not os.path.exists(path):
        crash_with_error(f'Error: {path} does not exist')

def ensure_not_exists(path):
    if os.path.exists(path):
        crash_with_error(f'Error: {path} exists')

def crash_with_error(message):
    print(message)
    sys.exit(1) # Exit with error

if __name__ == '__main__':
    main(sys.argv)
