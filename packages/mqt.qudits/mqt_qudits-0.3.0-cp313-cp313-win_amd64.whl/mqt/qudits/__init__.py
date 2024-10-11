"""MQT Qudits - A framework for mixed-dimensional qudit quantum computing."""

from __future__ import annotations


# start delvewheel patch
def _delvewheel_patch_1_8_2():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'mqt_qudits.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_8_2()
del _delvewheel_patch_1_8_2
# end delvewheel patch

from ._version import version as __version__
from ._version import version_tuple as version_info

__all__ = [
    "__version__",
    "version_info",
]
