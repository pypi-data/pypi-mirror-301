"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.acoustics._2684 import (
        AcousticAnalysisOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2685 import (
        AcousticAnalysisSetup,
    )
    from mastapy._private.system_model.part_model.acoustics._2686 import (
        AcousticAnalysisSetupCacheReporting,
    )
    from mastapy._private.system_model.part_model.acoustics._2687 import (
        AcousticAnalysisSetupCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2688 import (
        AcousticEnvelopeType,
    )
    from mastapy._private.system_model.part_model.acoustics._2689 import (
        AcousticInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2690 import (
        CacheMemoryEstimates,
    )
    from mastapy._private.system_model.part_model.acoustics._2691 import (
        FEPartInputSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2692 import (
        FESurfaceSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2693 import HoleInFaceGroup
    from mastapy._private.system_model.part_model.acoustics._2694 import (
        MeshedResultPlane,
    )
    from mastapy._private.system_model.part_model.acoustics._2695 import (
        MeshedResultSphere,
    )
    from mastapy._private.system_model.part_model.acoustics._2696 import (
        MeshedResultSurface,
    )
    from mastapy._private.system_model.part_model.acoustics._2697 import (
        MeshedResultSurfaceBase,
    )
    from mastapy._private.system_model.part_model.acoustics._2698 import (
        MicrophoneArrayDesign,
    )
    from mastapy._private.system_model.part_model.acoustics._2699 import (
        PartSelectionForAcousticEnvelope,
    )
    from mastapy._private.system_model.part_model.acoustics._2700 import (
        ResultPlaneOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2701 import (
        ResultSphereOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2702 import (
        ResultSurfaceCollection,
    )
    from mastapy._private.system_model.part_model.acoustics._2703 import (
        ResultSurfaceOptions,
    )
    from mastapy._private.system_model.part_model.acoustics._2704 import (
        SphericalEnvelopeCentreDefinition,
    )
    from mastapy._private.system_model.part_model.acoustics._2705 import (
        SphericalEnvelopeType,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.acoustics._2684": ["AcousticAnalysisOptions"],
        "_private.system_model.part_model.acoustics._2685": ["AcousticAnalysisSetup"],
        "_private.system_model.part_model.acoustics._2686": [
            "AcousticAnalysisSetupCacheReporting"
        ],
        "_private.system_model.part_model.acoustics._2687": [
            "AcousticAnalysisSetupCollection"
        ],
        "_private.system_model.part_model.acoustics._2688": ["AcousticEnvelopeType"],
        "_private.system_model.part_model.acoustics._2689": [
            "AcousticInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2690": ["CacheMemoryEstimates"],
        "_private.system_model.part_model.acoustics._2691": [
            "FEPartInputSurfaceOptions"
        ],
        "_private.system_model.part_model.acoustics._2692": [
            "FESurfaceSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2693": ["HoleInFaceGroup"],
        "_private.system_model.part_model.acoustics._2694": ["MeshedResultPlane"],
        "_private.system_model.part_model.acoustics._2695": ["MeshedResultSphere"],
        "_private.system_model.part_model.acoustics._2696": ["MeshedResultSurface"],
        "_private.system_model.part_model.acoustics._2697": ["MeshedResultSurfaceBase"],
        "_private.system_model.part_model.acoustics._2698": ["MicrophoneArrayDesign"],
        "_private.system_model.part_model.acoustics._2699": [
            "PartSelectionForAcousticEnvelope"
        ],
        "_private.system_model.part_model.acoustics._2700": ["ResultPlaneOptions"],
        "_private.system_model.part_model.acoustics._2701": ["ResultSphereOptions"],
        "_private.system_model.part_model.acoustics._2702": ["ResultSurfaceCollection"],
        "_private.system_model.part_model.acoustics._2703": ["ResultSurfaceOptions"],
        "_private.system_model.part_model.acoustics._2704": [
            "SphericalEnvelopeCentreDefinition"
        ],
        "_private.system_model.part_model.acoustics._2705": ["SphericalEnvelopeType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisOptions",
    "AcousticAnalysisSetup",
    "AcousticAnalysisSetupCacheReporting",
    "AcousticAnalysisSetupCollection",
    "AcousticEnvelopeType",
    "AcousticInputSurfaceOptions",
    "CacheMemoryEstimates",
    "FEPartInputSurfaceOptions",
    "FESurfaceSelectionForAcousticEnvelope",
    "HoleInFaceGroup",
    "MeshedResultPlane",
    "MeshedResultSphere",
    "MeshedResultSurface",
    "MeshedResultSurfaceBase",
    "MicrophoneArrayDesign",
    "PartSelectionForAcousticEnvelope",
    "ResultPlaneOptions",
    "ResultSphereOptions",
    "ResultSurfaceCollection",
    "ResultSurfaceOptions",
    "SphericalEnvelopeCentreDefinition",
    "SphericalEnvelopeType",
)
