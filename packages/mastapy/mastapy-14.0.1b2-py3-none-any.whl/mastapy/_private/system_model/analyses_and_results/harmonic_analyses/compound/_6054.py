"""CouplingHalfCompoundHarmonicAnalysis"""

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

_COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "CouplingHalfCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5852,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6038,
        _6040,
        _6043,
        _6057,
        _6096,
        _6099,
        _6105,
        _6109,
        _6121,
        _6131,
        _6132,
        _6133,
        _6136,
        _6137,
    )

    Self = TypeVar("Self", bound="CouplingHalfCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfCompoundHarmonicAnalysis._Cast_CouplingHalfCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfCompoundHarmonicAnalysis:
    """Special nested class for casting CouplingHalfCompoundHarmonicAnalysis to subclasses."""

    __parent__: "CouplingHalfCompoundHarmonicAnalysis"

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
    def clutch_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6038.ClutchHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6038,
        )

        return self.__parent__._cast(_6038.ClutchHalfCompoundHarmonicAnalysis)

    @property
    def concept_coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6043.ConceptCouplingHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6043,
        )

        return self.__parent__._cast(_6043.ConceptCouplingHalfCompoundHarmonicAnalysis)

    @property
    def cvt_pulley_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6057.CVTPulleyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6057,
        )

        return self.__parent__._cast(_6057.CVTPulleyCompoundHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6099.PartToPartShearCouplingHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6099,
        )

        return self.__parent__._cast(
            _6099.PartToPartShearCouplingHalfCompoundHarmonicAnalysis
        )

    @property
    def pulley_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6105.PulleyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6105,
        )

        return self.__parent__._cast(_6105.PulleyCompoundHarmonicAnalysis)

    @property
    def rolling_ring_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6109.RollingRingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6109,
        )

        return self.__parent__._cast(_6109.RollingRingCompoundHarmonicAnalysis)

    @property
    def spring_damper_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6121.SpringDamperHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6121,
        )

        return self.__parent__._cast(_6121.SpringDamperHalfCompoundHarmonicAnalysis)

    @property
    def synchroniser_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6131.SynchroniserHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6131,
        )

        return self.__parent__._cast(_6131.SynchroniserHalfCompoundHarmonicAnalysis)

    @property
    def synchroniser_part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6132.SynchroniserPartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6132,
        )

        return self.__parent__._cast(_6132.SynchroniserPartCompoundHarmonicAnalysis)

    @property
    def synchroniser_sleeve_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6133.SynchroniserSleeveCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6133,
        )

        return self.__parent__._cast(_6133.SynchroniserSleeveCompoundHarmonicAnalysis)

    @property
    def torque_converter_pump_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6136.TorqueConverterPumpCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6136,
        )

        return self.__parent__._cast(_6136.TorqueConverterPumpCompoundHarmonicAnalysis)

    @property
    def torque_converter_turbine_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6137.TorqueConverterTurbineCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6137,
        )

        return self.__parent__._cast(
            _6137.TorqueConverterTurbineCompoundHarmonicAnalysis
        )

    @property
    def coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "CouplingHalfCompoundHarmonicAnalysis":
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
class CouplingHalfCompoundHarmonicAnalysis(
    _6094.MountableComponentCompoundHarmonicAnalysis
):
    """CouplingHalfCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5852.CouplingHalfHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.CouplingHalfHarmonicAnalysis]

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
    ) -> "List[_5852.CouplingHalfHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.CouplingHalfHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingHalfCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfCompoundHarmonicAnalysis
        """
        return _Cast_CouplingHalfCompoundHarmonicAnalysis(self)
