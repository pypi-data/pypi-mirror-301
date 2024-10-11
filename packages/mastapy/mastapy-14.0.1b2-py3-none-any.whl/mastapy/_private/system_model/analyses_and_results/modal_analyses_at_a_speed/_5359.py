"""SynchroniserSleeveModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5358,
)

_SYNCHRONISER_SLEEVE_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "SynchroniserSleeveModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5265,
        _5278,
        _5320,
        _5322,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7123
    from mastapy._private.system_model.part_model.couplings import _2671

    Self = TypeVar("Self", bound="SynchroniserSleeveModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SynchroniserSleeveModalAnalysisAtASpeed._Cast_SynchroniserSleeveModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserSleeveModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserSleeveModalAnalysisAtASpeed:
    """Special nested class for casting SynchroniserSleeveModalAnalysisAtASpeed to subclasses."""

    __parent__: "SynchroniserSleeveModalAnalysisAtASpeed"

    @property
    def synchroniser_part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5358.SynchroniserPartModalAnalysisAtASpeed":
        return self.__parent__._cast(_5358.SynchroniserPartModalAnalysisAtASpeed)

    @property
    def coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5278.CouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5278,
        )

        return self.__parent__._cast(_5278.CouplingHalfModalAnalysisAtASpeed)

    @property
    def mountable_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5320.MountableComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5320,
        )

        return self.__parent__._cast(_5320.MountableComponentModalAnalysisAtASpeed)

    @property
    def component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5265.ComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5265,
        )

        return self.__parent__._cast(_5265.ComponentModalAnalysisAtASpeed)

    @property
    def part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5322.PartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5322,
        )

        return self.__parent__._cast(_5322.PartModalAnalysisAtASpeed)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2740.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "SynchroniserSleeveModalAnalysisAtASpeed":
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
class SynchroniserSleeveModalAnalysisAtASpeed(
    _5358.SynchroniserPartModalAnalysisAtASpeed
):
    """SynchroniserSleeveModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_SLEEVE_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2671.SynchroniserSleeve":
        """mastapy.system_model.part_model.couplings.SynchroniserSleeve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7123.SynchroniserSleeveLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserSleeveModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserSleeveModalAnalysisAtASpeed
        """
        return _Cast_SynchroniserSleeveModalAnalysisAtASpeed(self)
