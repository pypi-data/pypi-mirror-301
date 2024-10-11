"""KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4877,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4759
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4870,
        _4903,
        _4914,
        _4917,
        _4924,
        _4926,
    )

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis._Cast_KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis"

    @property
    def conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4877.ConicalGearCompoundModalAnalysis":
        return self.__parent__._cast(_4877.ConicalGearCompoundModalAnalysis)

    @property
    def gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4903.GearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4903,
        )

        return self.__parent__._cast(_4903.GearCompoundModalAnalysis)

    @property
    def mountable_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4924.MountableComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4924,
        )

        return self.__parent__._cast(_4924.MountableComponentCompoundModalAnalysis)

    @property
    def component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4870.ComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4870,
        )

        return self.__parent__._cast(_4870.ComponentCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4926.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4926,
        )

        return self.__parent__._cast(_4926.PartCompoundModalAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4914.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4914,
        )

        return self.__parent__._cast(
            _4914.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4917.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4917,
        )

        return self.__parent__._cast(
            _4917.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis":
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
class KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis(
    _4877.ConicalGearCompoundModalAnalysis
):
    """KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS
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
    ) -> "List[_4759.KlingelnbergCycloPalloidConicalGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearModalAnalysis]

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
    ) -> "List[_4759.KlingelnbergCycloPalloidConicalGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.KlingelnbergCycloPalloidConicalGearModalAnalysis]

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
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis(self)
