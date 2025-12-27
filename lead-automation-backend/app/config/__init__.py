# Config package initialization
# Import settings from the parent config.py module
import sys
import os

# Add parent directory to path to import from app.config module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import settings from app/config.py (the module, not this package)
try:
    # Try importing from the config.py file in the parent app directory
    import importlib.util
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")
    spec = importlib.util.spec_from_file_location("app_config", config_file)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    settings = config_module.settings
except Exception as e:
    # Fallback: create a dummy settings object
    print(f"Warning: Could not import settings from config.py: {e}")
    settings = None

__all__ = ['settings']

