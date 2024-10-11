"""CylindricalGearModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5036,
)

_CYLINDRICAL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "CylindricalGearModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5001,
        _5026,
        _5057,
        _5059,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7012
    from mastapy._private.system_model.part_model.gears import _2584

    Self = TypeVar("Self", bound="CylindricalGearModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearModalAnalysisAtAStiffness._Cast_CylindricalGearModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearModalAnalysisAtAStiffness:
    """Special nested class for casting CylindricalGearModalAnalysisAtAStiffness to subclasses."""

    __parent__: "CylindricalGearModalAnalysisAtAStiffness"

    @property
    def gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5036.GearModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5036.GearModalAnalysisAtAStiffness)

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
    def cylindrical_planet_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5026.CylindricalPlanetGearModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5026,
        )

        return self.__parent__._cast(
            _5026.CylindricalPlanetGearModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "CylindricalGearModalAnalysisAtAStiffness":
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
class CylindricalGearModalAnalysisAtAStiffness(_5036.GearModalAnalysisAtAStiffness):
    """CylindricalGearModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2584.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7012.CylindricalGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(self: "Self") -> "List[CylindricalGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.CylindricalGearModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearModalAnalysisAtAStiffness
        """
        return _Cast_CylindricalGearModalAnalysisAtAStiffness(self)
