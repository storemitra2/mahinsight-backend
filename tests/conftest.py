import sys
import os

# Ensure the project root (backend folder) is on sys.path for pytest imports
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
