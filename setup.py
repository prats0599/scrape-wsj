import subprocess
import sys

python = sys.executable
# Define the packages to be installed
packages = ['requests', 'bs4', 'selenium']

# Loop through the packages and install them using pip
for package in packages:
    try:
        subprocess.check_call([python, '-m', 'pip', 'install', package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")

