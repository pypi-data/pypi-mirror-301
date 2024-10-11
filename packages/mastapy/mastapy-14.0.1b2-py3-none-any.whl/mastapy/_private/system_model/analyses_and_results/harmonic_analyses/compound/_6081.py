"""KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis"""

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
    _6047,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5909,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6040,
        _6073,
        _6084,
        _6087,
        _6094,
        _6096,
    )

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis._Cast_KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis"

    @property
    def conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6047.ConicalGearCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6047.ConicalGearCompoundHarmonicAnalysis)

    @property
    def gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6073.GearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6073,
        )

        return self.__parent__._cast(_6073.GearCompoundHarmonicAnalysis)

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6094.MountableComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6094,
        )

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
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6084.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6084,
        )

        return self.__parent__._cast(
            _6084.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6087.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6087,
        )

        return self.__parent__._cast(
            _6087.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis":
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
class KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis(
    _6047.ConicalGearCompoundHarmonicAnalysis
):
    """KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_HARMONIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5909.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]

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
    ) -> "List[_5909.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis(self)
