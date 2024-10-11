"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.creation_options._2630 import (
        BeltCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2631 import (
        CycloidalAssemblyCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2632 import (
        CylindricalGearLinearTrainCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2633 import (
        MicrophoneArrayCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2634 import (
        PlanetCarrierCreationOptions,
    )
    from mastapy._private.system_model.part_model.creation_options._2635 import (
        ShaftCreationOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.creation_options._2630": [
            "BeltCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2631": [
            "CycloidalAssemblyCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2632": [
            "CylindricalGearLinearTrainCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2633": [
            "MicrophoneArrayCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2634": [
            "PlanetCarrierCreationOptions"
        ],
        "_private.system_model.part_model.creation_options._2635": [
            "ShaftCreationOptions"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltCreationOptions",
    "CycloidalAssemblyCreationOptions",
    "CylindricalGearLinearTrainCreationOptions",
    "MicrophoneArrayCreationOptions",
    "PlanetCarrierCreationOptions",
    "ShaftCreationOptions",
)
