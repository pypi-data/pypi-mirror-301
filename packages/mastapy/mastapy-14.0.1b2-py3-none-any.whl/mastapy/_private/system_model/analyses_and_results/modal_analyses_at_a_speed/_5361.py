"""TorqueConverterModalAnalysisAtASpeed"""

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
    _5279,
)

_TORQUE_CONVERTER_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "TorqueConverterModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5240,
        _5322,
        _5341,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7126
    from mastapy._private.system_model.part_model.couplings import _2672

    Self = TypeVar("Self", bound="TorqueConverterModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterModalAnalysisAtASpeed._Cast_TorqueConverterModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterModalAnalysisAtASpeed:
    """Special nested class for casting TorqueConverterModalAnalysisAtASpeed to subclasses."""

    __parent__: "TorqueConverterModalAnalysisAtASpeed"

    @property
    def coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5279.CouplingModalAnalysisAtASpeed":
        return self.__parent__._cast(_5279.CouplingModalAnalysisAtASpeed)

    @property
    def specialised_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5341.SpecialisedAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5341,
        )

        return self.__parent__._cast(_5341.SpecialisedAssemblyModalAnalysisAtASpeed)

    @property
    def abstract_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5240.AbstractAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5240,
        )

        return self.__parent__._cast(_5240.AbstractAssemblyModalAnalysisAtASpeed)

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
    def torque_converter_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "TorqueConverterModalAnalysisAtASpeed":
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
class TorqueConverterModalAnalysisAtASpeed(_5279.CouplingModalAnalysisAtASpeed):
    """TorqueConverterModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2672.TorqueConverter":
        """mastapy.system_model.part_model.couplings.TorqueConverter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7126.TorqueConverterLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverterModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterModalAnalysisAtASpeed
        """
        return _Cast_TorqueConverterModalAnalysisAtASpeed(self)
