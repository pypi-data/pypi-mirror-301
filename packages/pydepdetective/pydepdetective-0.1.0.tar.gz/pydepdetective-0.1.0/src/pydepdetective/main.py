import ast
import subprocess
import sys
import importlib.util
import pkg_resources
import re

def extract_imports(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == 'importlib':
                # Handle dynamic imports
                if len(node.args) > 0 and isinstance(node.args[0], ast.Str):
                    imports.add(node.args[0].s.split('.')[0])
    
    return imports

def filter_standard_library(imports):
    standard_libs = set(sys.stdlib_module_names)
    return {imp for imp in imports if imp not in standard_libs}

def get_installed_packages():
    return {pkg.key for pkg in pkg_resources.working_set}

def map_import_to_package(import_name):
    # Common mappings that don't follow the standard naming convention (WE NEED MORE)
    mappings = {
        'PIL': 'pillow',
        'cv2': 'opencv-python',
        'sklearn': 'scikit-learn',
        'bs4': 'beautifulsoup4',
        'yaml': 'pyyaml',
    }
    return mappings.get(import_name, import_name)

def install_dependencies(dependencies):
    installed = get_installed_packages()
    to_install = [map_import_to_package(dep) for dep in dependencies if dep.lower() not in installed]
    
    if not to_install:
        print("All dependencies are already installed.")
        return

    for dep in to_install:
        print(f"Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        except subprocess.CalledProcessError:
            print(f"Failed to install {dep}. It might not be available on PyPI or there could be a naming mismatch.")

def analyze_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Look for pip install comments
    pip_installs = re.findall(r'#\s*pip install\s+(\S+)', content)
    
    # Look for requirements.txt references
    req_file_mention = re.search(r'#.*requirements\.txt', content)
    
    return pip_installs, bool(req_file_mention)

def main():
    if len(sys.argv) != 2:
        print("Usage: python auto_install_deps.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    imports = extract_imports(file_path)
    third_party_imports = filter_standard_library(imports)

    pip_installs, req_file_mentioned = analyze_file_content(file_path)

    if not third_party_imports and not pip_installs and not req_file_mentioned:
        print("No third-party dependencies found.")
        return

    print("Found the following potential dependencies:")
    for imp in third_party_imports:
        print(f"- {imp} (from import statements)")
    for pkg in pip_installs:
        print(f"- {pkg} (from '# pip install' comments)")
    
    if req_file_mentioned:
        print("Note: A reference to 'requirements.txt' was found in the file.")
        user_input = input("Do you want to install dependencies from 'requirements.txt'? (y/n): ")
        if user_input.lower() == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print("Dependencies from requirements.txt installed successfully!")
            except subprocess.CalledProcessError:
                print("Failed to install from requirements.txt. The file might not exist or there could be an error.")
            except FileNotFoundError:
                print("requirements.txt file not found.")

    user_input = input("Do you want to install the detected dependencies? (y/n): ")
    if user_input.lower() == 'y':
        all_deps = set(third_party_imports) | set(pip_installs)
        install_dependencies(all_deps)
        print("All dependencies installed successfully!")
    else:
        print("Installation cancelled.")

if __name__ == "__main__":
    main()