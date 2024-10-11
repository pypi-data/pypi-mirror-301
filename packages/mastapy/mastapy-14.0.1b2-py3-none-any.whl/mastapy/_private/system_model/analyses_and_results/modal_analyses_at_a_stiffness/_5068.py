"""PulleyModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5014,
)

_PULLEY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "PulleyModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5001,
        _5018,
        _5057,
        _5059,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7093
    from mastapy._private.system_model.part_model.couplings import _2652

    Self = TypeVar("Self", bound="PulleyModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PulleyModalAnalysisAtAStiffness._Cast_PulleyModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PulleyModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PulleyModalAnalysisAtAStiffness:
    """Special nested class for casting PulleyModalAnalysisAtAStiffness to subclasses."""

    __parent__: "PulleyModalAnalysisAtAStiffness"

    @property
    def coupling_half_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5014.CouplingHalfModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5014.CouplingHalfModalAnalysisAtAStiffness)

    @property
    def mountable_component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5057.MountableComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5057,
        )

        return self.__parent__._cast(_5057.MountableComponentModalAnalysisAtAStiffness)

    @property
    def component_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5001.ComponentModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5001,
        )

        return self.__parent__._cast(_5001.ComponentModalAnalysisAtAStiffness)

    @property
    def part_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5059.PartModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5059,
        )

        return self.__parent__._cast(_5059.PartModalAnalysisAtAStiffness)

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
    def cvt_pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5018.CVTPulleyModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5018,
        )

        return self.__parent__._cast(_5018.CVTPulleyModalAnalysisAtAStiffness)

    @property
    def pulley_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "PulleyModalAnalysisAtAStiffness":
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
class PulleyModalAnalysisAtAStiffness(_5014.CouplingHalfModalAnalysisAtAStiffness):
    """PulleyModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PULLEY_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2652.Pulley":
        """mastapy.system_model.part_model.couplings.Pulley

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7093.PulleyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PulleyModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_PulleyModalAnalysisAtAStiffness
        """
        return _Cast_PulleyModalAnalysisAtAStiffness(self)
