"""StraightBevelPlanetGearCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5479,
)

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "StraightBevelPlanetGearCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5354,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5376,
        _5388,
        _5397,
        _5404,
        _5430,
        _5451,
        _5453,
    )

    Self = TypeVar("Self", bound="StraightBevelPlanetGearCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelPlanetGearCompoundModalAnalysisAtASpeed._Cast_StraightBevelPlanetGearCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelPlanetGearCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelPlanetGearCompoundModalAnalysisAtASpeed:
    """Special nested class for casting StraightBevelPlanetGearCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "StraightBevelPlanetGearCompoundModalAnalysisAtASpeed"

    @property
    def straight_bevel_diff_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5479.StraightBevelDiffGearCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5479.StraightBevelDiffGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5388.BevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5388,
        )

        return self.__parent__._cast(_5388.BevelGearCompoundModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5376.AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5376,
        )

        return self.__parent__._cast(
            _5376.AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed
        )

    @property
    def conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5404.ConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5404,
        )

        return self.__parent__._cast(_5404.ConicalGearCompoundModalAnalysisAtASpeed)

    @property
    def gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5430.GearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5430,
        )

        return self.__parent__._cast(_5430.GearCompoundModalAnalysisAtASpeed)

    @property
    def mountable_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5451.MountableComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5451,
        )

        return self.__parent__._cast(
            _5451.MountableComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5397.ComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5397,
        )

        return self.__parent__._cast(_5397.ComponentCompoundModalAnalysisAtASpeed)

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5453.PartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5453,
        )

        return self.__parent__._cast(_5453.PartCompoundModalAnalysisAtASpeed)

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
    def straight_bevel_planet_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "StraightBevelPlanetGearCompoundModalAnalysisAtASpeed":
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
class StraightBevelPlanetGearCompoundModalAnalysisAtASpeed(
    _5479.StraightBevelDiffGearCompoundModalAnalysisAtASpeed
):
    """StraightBevelPlanetGearCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5354.StraightBevelPlanetGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.StraightBevelPlanetGearModalAnalysisAtASpeed]

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
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5354.StraightBevelPlanetGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.StraightBevelPlanetGearModalAnalysisAtASpeed]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelPlanetGearCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelPlanetGearCompoundModalAnalysisAtASpeed
        """
        return _Cast_StraightBevelPlanetGearCompoundModalAnalysisAtASpeed(self)
