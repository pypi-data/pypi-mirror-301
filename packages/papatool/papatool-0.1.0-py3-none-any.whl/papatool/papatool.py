import os
import subprocess
import sys

def install_dependencies():
    """Install minimal dependencies for packaging and uploading."""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'setuptools', 'wheel', 'twine'])

def create_project(project_name):
    """Create a basic Python package project structure."""
    print(f"Creating project: {project_name}")

    # Create the project structure
    os.makedirs(f"{project_name}/{project_name}", exist_ok=True)
    open(f"{project_name}/{project_name}/__init__.py", 'w').close()  # Create empty __init__.py

    # Write basic setup.py
    with open(f"{project_name}/setup.py", 'w') as f:
        f.write(f"""
from setuptools import setup, find_packages

setup(
    name='{project_name}',
    version='0.1.0',
    packages=find_packages(),
    description='A sample {project_name} package',
    author='Your Name',
    author_email='you@example.com',
    url='https://github.com/yourusername/{project_name}',
    install_requires=[],
)
""")

    # Create README.md
    with open(f"{project_name}/README.md", 'w') as f:
        f.write(f"# {project_name}\n\nA sample Python package.")

    print(f"Project {project_name} created successfully.")

def build_package():
    """Build the package."""
    print("Building the package...")
    
    # Clean previous builds
    os.system('rm -rf dist/* build/* *.egg-info')
    
    # Build the source distribution
    subprocess.check_call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])

def upload_package():
    """Upload the package to PyPI using twine."""
    print("Uploading the package to PyPI...")
    
    # Upload using twine
    subprocess.check_call([sys.executable, '-m', 'twine', 'upload', 'dist/*'])

def main():
    if len(sys.argv) < 2:
        print("Usage: package_tool.py [create|build|upload] <project_name>")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == 'create':
        if len(sys.argv) < 3:
            print("Please specify the project name.")
            sys.exit(1)
        project_name = sys.argv[2]
        install_dependencies()
        create_project(project_name)
    elif command == 'build':
        install_dependencies()
        build_package()
    elif command == 'upload':
        install_dependencies()
        upload_package()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
