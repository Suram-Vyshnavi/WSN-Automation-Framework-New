"""
Bootstrap loader: imports all step definitions from the studentpersona/
subdirectory so behave can discover them (behave 1.x does not recurse).
"""
import importlib.util
import os
import sys

_studentpersona_dir = os.path.join(os.path.dirname(__file__), "studentpersona")

for _filename in sorted(os.listdir(_studentpersona_dir)):
    if _filename.endswith("_steps.py"):
        _module_name = f"_studentpersona.{_filename[:-3]}"
        _filepath = os.path.join(_studentpersona_dir, _filename)
        _spec = importlib.util.spec_from_file_location(_module_name, _filepath)
        _module = importlib.util.module_from_spec(_spec)
        sys.modules[_module_name] = _module
        _spec.loader.exec_module(_module)
