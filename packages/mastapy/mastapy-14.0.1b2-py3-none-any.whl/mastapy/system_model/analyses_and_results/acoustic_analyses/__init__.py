"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7695 import (
        AcousticAnalysisRunType,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7696 import (
        AcousticPreconditionerType,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7697 import (
        AcousticSurfaceSelectionList,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7698 import (
        AcousticSurfaceWithSelection,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7699 import (
        HarmonicAcousticAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7700 import (
        InitialGuessOption,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7701 import (
        M2LHfCacheType,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7702 import (
        NearFieldIntegralsCacheType,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7703 import (
        OctreeCreationMethod,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7704 import (
        SingleExcitationDetails,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7705 import (
        SingleHarmonicExcitationAnalysisDetail,
    )
    from mastapy._private.system_model.analyses_and_results.acoustic_analyses._7706 import (
        UnitForceExcitationAnalysisDetail,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.acoustic_analyses._7695": [
            "AcousticAnalysisRunType"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7696": [
            "AcousticPreconditionerType"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7697": [
            "AcousticSurfaceSelectionList"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7698": [
            "AcousticSurfaceWithSelection"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7699": [
            "HarmonicAcousticAnalysis"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7700": [
            "InitialGuessOption"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7701": [
            "M2LHfCacheType"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7702": [
            "NearFieldIntegralsCacheType"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7703": [
            "OctreeCreationMethod"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7704": [
            "SingleExcitationDetails"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7705": [
            "SingleHarmonicExcitationAnalysisDetail"
        ],
        "_private.system_model.analyses_and_results.acoustic_analyses._7706": [
            "UnitForceExcitationAnalysisDetail"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AcousticAnalysisRunType",
    "AcousticPreconditionerType",
    "AcousticSurfaceSelectionList",
    "AcousticSurfaceWithSelection",
    "HarmonicAcousticAnalysis",
    "InitialGuessOption",
    "M2LHfCacheType",
    "NearFieldIntegralsCacheType",
    "OctreeCreationMethod",
    "SingleExcitationDetails",
    "SingleHarmonicExcitationAnalysisDetail",
    "UnitForceExcitationAnalysisDetail",
)
