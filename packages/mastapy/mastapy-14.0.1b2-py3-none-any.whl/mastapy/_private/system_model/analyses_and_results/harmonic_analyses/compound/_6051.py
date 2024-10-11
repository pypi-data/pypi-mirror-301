"""ConnectorCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6094,
)

_CONNECTOR_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ConnectorCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5850,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6023,
        _6040,
        _6095,
        _6096,
        _6113,
    )

    Self = TypeVar("Self", bound="ConnectorCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectorCompoundHarmonicAnalysis._Cast_ConnectorCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorCompoundHarmonicAnalysis:
    """Special nested class for casting ConnectorCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ConnectorCompoundHarmonicAnalysis"

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6094.MountableComponentCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6094.MountableComponentCompoundHarmonicAnalysis)

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6040.ComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6040,
        )

        return self.__parent__._cast(_6040.ComponentCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6096.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6096,
        )

        return self.__parent__._cast(_6096.PartCompoundHarmonicAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7718.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7715.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def bearing_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6023.BearingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6023,
        )

        return self.__parent__._cast(_6023.BearingCompoundHarmonicAnalysis)

    @property
    def oil_seal_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6095.OilSealCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6095,
        )

        return self.__parent__._cast(_6095.OilSealCompoundHarmonicAnalysis)

    @property
    def shaft_hub_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6113.ShaftHubConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6113,
        )

        return self.__parent__._cast(_6113.ShaftHubConnectionCompoundHarmonicAnalysis)

    @property
    def connector_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ConnectorCompoundHarmonicAnalysis":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class ConnectorCompoundHarmonicAnalysis(
    _6094.MountableComponentCompoundHarmonicAnalysis
):
    """ConnectorCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5850.ConnectorHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConnectorHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5850.ConnectorHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConnectorHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectorCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectorCompoundHarmonicAnalysis
        """
        return _Cast_ConnectorCompoundHarmonicAnalysis(self)
