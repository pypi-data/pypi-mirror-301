"""WormGearSetModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5300,
)

_WORM_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "WormGearSetModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5240,
        _5322,
        _5341,
        _5366,
        _5367,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7137
    from mastapy._private.system_model.part_model.gears import _2611

    Self = TypeVar("Self", bound="WormGearSetModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGearSetModalAnalysisAtASpeed._Cast_WormGearSetModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSetModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSetModalAnalysisAtASpeed:
    """Special nested class for casting WormGearSetModalAnalysisAtASpeed to subclasses."""

    __parent__: "WormGearSetModalAnalysisAtASpeed"

    @property
    def gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5300.GearSetModalAnalysisAtASpeed":
        return self.__parent__._cast(_5300.GearSetModalAnalysisAtASpeed)

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
    def worm_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "WormGearSetModalAnalysisAtASpeed":
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
class WormGearSetModalAnalysisAtASpeed(_5300.GearSetModalAnalysisAtASpeed):
    """WormGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2611.WormGearSet":
        """mastapy.system_model.part_model.gears.WormGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7137.WormGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5367.WormGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.WormGearModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def worm_gears_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5367.WormGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.WormGearModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearsModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5366.WormGearMeshModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.WormGearMeshModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def worm_meshes_modal_analysis_at_a_speed(
        self: "Self",
    ) -> "List[_5366.WormGearMeshModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.WormGearMeshModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshesModalAnalysisAtASpeed")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearSetModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_WormGearSetModalAnalysisAtASpeed
        """
        return _Cast_WormGearSetModalAnalysisAtASpeed(self)
