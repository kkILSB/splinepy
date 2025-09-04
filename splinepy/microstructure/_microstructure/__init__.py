"""splinepy/microstructure/_microstructure/__init__.py.

Interface single- and multi-patch microstructures.
"""

from splinepy.microstructure._microstructure import (
    microstructure_multi_patch,
    microstructure_single_patch
)
from splinepy.microstructure._microstructure.microstructure_multi_patch import \
        _MicrostructureMultiPatch
from splinepy.microstructure._microstructure.microstructure_single_patch \
        import _MicrostructureSinglePatch


__all__ = [
    "microstructure_multi_patch",
    "microstructure_single_patch",
    "_MicrostructureMultiPatch",
    "_MicrostructureSinglePatch"
]
