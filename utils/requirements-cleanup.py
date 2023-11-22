import argparse

requirements = {}
requirements_file = ''

parser = argparse.ArgumentParser(description='Clean up requirements.txt file')
parser.add_argument('requirements_file', metavar='requirements_file', type=str, nargs='+',
                    help='the requirements file to clean up')



# take a command line argument to determine which requirements file to use
requirements_file = parser.parse_args().requirements_file[0] 


with open(requirements_file, 'r') as file:
    for line in file:
        if line.strip() == '' or line.startswith('#'):
            continue
        package, version = line.strip().split('==')
        if package not in requirements or version > requirements[package]:
            requirements[package] = version

with open(requirements_file, 'w') as file:
    for package, version in sorted(requirements.items()):
        file.write(f'{package}=={version}\n')



