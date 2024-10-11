"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5980 import (
        ConnectedComponentType,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5981 import (
        ExcitationSourceSelection,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5982 import (
        ExcitationSourceSelectionBase,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5983 import (
        ExcitationSourceSelectionGroup,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5984 import (
        HarmonicSelection,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5985 import (
        ModalContributionDisplayMethod,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5986 import (
        ModalContributionFilteringMethod,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5987 import (
        ResultLocationSelectionGroup,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5988 import (
        ResultLocationSelectionGroups,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5989 import (
        ResultNodeSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5980": [
            "ConnectedComponentType"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5981": [
            "ExcitationSourceSelection"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5982": [
            "ExcitationSourceSelectionBase"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5983": [
            "ExcitationSourceSelectionGroup"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5984": [
            "HarmonicSelection"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5985": [
            "ModalContributionDisplayMethod"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5986": [
            "ModalContributionFilteringMethod"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5987": [
            "ResultLocationSelectionGroup"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5988": [
            "ResultLocationSelectionGroups"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5989": [
            "ResultNodeSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConnectedComponentType",
    "ExcitationSourceSelection",
    "ExcitationSourceSelectionBase",
    "ExcitationSourceSelectionGroup",
    "HarmonicSelection",
    "ModalContributionDisplayMethod",
    "ModalContributionFilteringMethod",
    "ResultLocationSelectionGroup",
    "ResultLocationSelectionGroups",
    "ResultNodeSelection",
)
