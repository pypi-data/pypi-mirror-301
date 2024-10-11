"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7707 import (
        AnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7708 import (
        AbstractAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7709 import (
        CompoundAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7710 import (
        ConnectionAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7711 import (
        ConnectionCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7712 import (
        ConnectionFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7713 import (
        ConnectionStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7714 import (
        ConnectionTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7715 import (
        DesignEntityCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7716 import (
        FEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7717 import (
        PartAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7718 import (
        PartCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7719 import (
        PartFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7720 import (
        PartStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7721 import (
        PartTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7722 import (
        StaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7723 import (
        TimeSeriesLoadAnalysisCase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.analysis_cases._7707": [
            "AnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7708": [
            "AbstractAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7709": [
            "CompoundAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7710": [
            "ConnectionAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7711": [
            "ConnectionCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7712": [
            "ConnectionFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7713": [
            "ConnectionStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7714": [
            "ConnectionTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7715": [
            "DesignEntityCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7716": [
            "FEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7717": [
            "PartAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7718": [
            "PartCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7719": [
            "PartFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7720": [
            "PartStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7721": [
            "PartTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7722": [
            "StaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7723": [
            "TimeSeriesLoadAnalysisCase"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AnalysisCase",
    "AbstractAnalysisOptions",
    "CompoundAnalysisCase",
    "ConnectionAnalysisCase",
    "ConnectionCompoundAnalysis",
    "ConnectionFEAnalysis",
    "ConnectionStaticLoadAnalysisCase",
    "ConnectionTimeSeriesLoadAnalysisCase",
    "DesignEntityCompoundAnalysis",
    "FEAnalysis",
    "PartAnalysisCase",
    "PartCompoundAnalysis",
    "PartFEAnalysis",
    "PartStaticLoadAnalysisCase",
    "PartTimeSeriesLoadAnalysisCase",
    "StaticLoadAnalysisCase",
    "TimeSeriesLoadAnalysisCase",
)
