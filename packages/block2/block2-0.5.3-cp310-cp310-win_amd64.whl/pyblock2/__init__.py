"""""" # start delvewheel patch
def _delvewheel_patch_1_7_1():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_7_1()
del _delvewheel_patch_1_7_1
# end delvewheel patch

import os
import sys

sys.path += [os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..", "build")]

if os.name == "nt" and sys.version_info[1] >= 8:
    for path in os.environ["PATH"].split(";"):
        if path != "" and os.path.exists(os.path.abspath(path)):
            os.add_dll_directory(os.path.abspath(path))
