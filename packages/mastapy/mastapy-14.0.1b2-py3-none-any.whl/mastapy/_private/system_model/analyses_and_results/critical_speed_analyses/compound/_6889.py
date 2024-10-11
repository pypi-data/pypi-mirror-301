"""KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6855,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
        "KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6758,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6848,
        _6881,
        _6892,
        _6895,
        _6902,
        _6904,
    )

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis._Cast_KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis"

    @property
    def conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6855.ConicalGearCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_6855.ConicalGearCompoundCriticalSpeedAnalysis)

    @property
    def gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6881.GearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6881,
        )

        return self.__parent__._cast(_6881.GearCompoundCriticalSpeedAnalysis)

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6902.MountableComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6902,
        )

        return self.__parent__._cast(
            _6902.MountableComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6848.ComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6848,
        )

        return self.__parent__._cast(_6848.ComponentCompoundCriticalSpeedAnalysis)

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6904.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6904,
        )

        return self.__parent__._cast(_6904.PartCompoundCriticalSpeedAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6892.KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6892,
        )

        return self.__parent__._cast(
            _6892.KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6895.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6895,
        )

        return self.__parent__._cast(
            _6895.KlingelnbergCycloPalloidSpiralBevelGearCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis":
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
class KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis(
    _6855.ConicalGearCompoundCriticalSpeedAnalysis
):
    """KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS
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
    ) -> "List[_6758.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis]

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
    ) -> "List[_6758.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis]

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
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis(
            self
        )
