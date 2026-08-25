"""Load every nested step module so Behave can discover its step definitions.

Behave 1.2.6 only imports the .py files that sit directly in `features/steps`,
not the ones in sub-folders. This single bootstrap walks every sub-folder and
imports each `*_steps.py` exactly once, under a unique module name, so the
`@given/@when/@then` decorators register without duplicating any step.

The leading underscore keeps this module first in Behave's alphabetical load
order, so nested steps are registered before any top-level step module runs.
"""

import importlib.util
import os
import sys

_STEPS_ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_step_module(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)


for _dirpath, _dirnames, _filenames in sorted(os.walk(_STEPS_ROOT)):
    if _dirpath == _STEPS_ROOT or "__pycache__" in _dirpath:
        continue
    _package = os.path.relpath(_dirpath, _STEPS_ROOT).replace(os.sep, ".")
    for _filename in sorted(_filenames):
        if not _filename.endswith("_steps.py"):
            continue
        _load_step_module(os.path.join(_dirpath, _filename),
                          f"_nested_steps.{_package}.{_filename[:-3]}")
