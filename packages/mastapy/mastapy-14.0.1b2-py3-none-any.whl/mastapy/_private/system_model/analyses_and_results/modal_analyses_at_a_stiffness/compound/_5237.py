"""ZerolBevelGearCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5125,
)

_ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "ZerolBevelGearCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5107,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5113,
        _5134,
        _5141,
        _5167,
        _5188,
        _5190,
    )
    from mastapy._private.system_model.part_model.gears import _2612

    Self = TypeVar("Self", bound="ZerolBevelGearCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearCompoundModalAnalysisAtAStiffness._Cast_ZerolBevelGearCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting ZerolBevelGearCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "ZerolBevelGearCompoundModalAnalysisAtAStiffness"

    @property
    def bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5125.BevelGearCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5125.BevelGearCompoundModalAnalysisAtAStiffness)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5113.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5113,
        )

        return self.__parent__._cast(
            _5113.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5141.ConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5141,
        )

        return self.__parent__._cast(_5141.ConicalGearCompoundModalAnalysisAtAStiffness)

    @property
    def gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5167.GearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5167,
        )

        return self.__parent__._cast(_5167.GearCompoundModalAnalysisAtAStiffness)

    @property
    def mountable_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5188.MountableComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5188,
        )

        return self.__parent__._cast(
            _5188.MountableComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5134.ComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5134,
        )

        return self.__parent__._cast(_5134.ComponentCompoundModalAnalysisAtAStiffness)

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5190.PartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5190,
        )

        return self.__parent__._cast(_5190.PartCompoundModalAnalysisAtAStiffness)

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
    def zerol_bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "ZerolBevelGearCompoundModalAnalysisAtAStiffness":
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
class ZerolBevelGearCompoundModalAnalysisAtAStiffness(
    _5125.BevelGearCompoundModalAnalysisAtAStiffness
):
    """ZerolBevelGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2612.ZerolBevelGear":
        """mastapy.system_model.part_model.gears.ZerolBevelGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5107.ZerolBevelGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ZerolBevelGearModalAnalysisAtAStiffness]

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
    ) -> "List[_5107.ZerolBevelGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ZerolBevelGearModalAnalysisAtAStiffness]

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
    ) -> "_Cast_ZerolBevelGearCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearCompoundModalAnalysisAtAStiffness
        """
        return _Cast_ZerolBevelGearCompoundModalAnalysisAtAStiffness(self)
