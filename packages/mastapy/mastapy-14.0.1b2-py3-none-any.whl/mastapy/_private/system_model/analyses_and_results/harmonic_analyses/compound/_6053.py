"""CouplingConnectionCompoundHarmonicAnalysis"""

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
    _6080,
)

_COUPLING_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "CouplingConnectionCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5851,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6037,
        _6042,
        _6050,
        _6098,
        _6120,
        _6135,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundHarmonicAnalysis._Cast_CouplingConnectionCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundHarmonicAnalysis:
    """Special nested class for casting CouplingConnectionCompoundHarmonicAnalysis to subclasses."""

    __parent__: "CouplingConnectionCompoundHarmonicAnalysis"

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6080.InterMountableComponentConnectionCompoundHarmonicAnalysis":
        return self.__parent__._cast(
            _6080.InterMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6050.ConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6050,
        )

        return self.__parent__._cast(_6050.ConnectionCompoundHarmonicAnalysis)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionCompoundAnalysis)

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
    def clutch_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6037.ClutchConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6037,
        )

        return self.__parent__._cast(_6037.ClutchConnectionCompoundHarmonicAnalysis)

    @property
    def concept_coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6042.ConceptCouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6042,
        )

        return self.__parent__._cast(
            _6042.ConceptCouplingConnectionCompoundHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6098.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6098,
        )

        return self.__parent__._cast(
            _6098.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis
        )

    @property
    def spring_damper_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6120.SpringDamperConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6120,
        )

        return self.__parent__._cast(
            _6120.SpringDamperConnectionCompoundHarmonicAnalysis
        )

    @property
    def torque_converter_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6135.TorqueConverterConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6135,
        )

        return self.__parent__._cast(
            _6135.TorqueConverterConnectionCompoundHarmonicAnalysis
        )

    @property
    def coupling_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundHarmonicAnalysis":
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
class CouplingConnectionCompoundHarmonicAnalysis(
    _6080.InterMountableComponentConnectionCompoundHarmonicAnalysis
):
    """CouplingConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5851.CouplingConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.CouplingConnectionHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5851.CouplingConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.CouplingConnectionHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundHarmonicAnalysis
        """
        return _Cast_CouplingConnectionCompoundHarmonicAnalysis(self)
