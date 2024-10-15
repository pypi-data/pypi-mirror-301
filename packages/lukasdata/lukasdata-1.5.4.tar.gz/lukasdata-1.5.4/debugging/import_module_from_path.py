import importlib.util
import sys
import os

def import_module_from_path(module_name, file_path):
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    if spec is None:
        raise ImportError(f"Cannot create a module spec for {module_name} from {file_path}")

    # Create a module object from the spec
    module = importlib.util.module_from_spec(spec)

    # Add the module to sys.modules
    sys.modules[module_name] = module

    # Execute the module
    spec.loader.exec_module(module)

    return module
