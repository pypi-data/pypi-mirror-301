"""StraightBevelGearSetSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2794

_STRAIGHT_BEVEL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "StraightBevelGearSetSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.straight_bevel import _410
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4256
    from mastapy._private.system_model.analyses_and_results.static_loads import _7117
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2772,
        _2777,
        _2812,
        _2847,
        _2874,
        _2895,
        _2905,
        _2907,
    )
    from mastapy._private.system_model.part_model.gears import _2607

    Self = TypeVar("Self", bound="StraightBevelGearSetSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearSetSystemDeflection._Cast_StraightBevelGearSetSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearSetSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearSetSystemDeflection:
    """Special nested class for casting StraightBevelGearSetSystemDeflection to subclasses."""

    __parent__: "StraightBevelGearSetSystemDeflection"

    @property
    def bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2794.BevelGearSetSystemDeflection":
        return self.__parent__._cast(_2794.BevelGearSetSystemDeflection)

    @property
    def agma_gleason_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2777.AGMAGleasonConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2777,
        )

        return self.__parent__._cast(_2777.AGMAGleasonConicalGearSetSystemDeflection)

    @property
    def conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2812.ConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2812,
        )

        return self.__parent__._cast(_2812.ConicalGearSetSystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "_2847.GearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2847,
        )

        return self.__parent__._cast(_2847.GearSetSystemDeflection)

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2895.SpecialisedAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2895,
        )

        return self.__parent__._cast(_2895.SpecialisedAssemblySystemDeflection)

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2772.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2772,
        )

        return self.__parent__._cast(_2772.AbstractAssemblySystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2874.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2874,
        )

        return self.__parent__._cast(_2874.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7719.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartFEAnalysis)

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
    def straight_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "StraightBevelGearSetSystemDeflection":
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
class StraightBevelGearSetSystemDeflection(_2794.BevelGearSetSystemDeflection):
    """StraightBevelGearSetSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_SET_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2607.StraightBevelGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7117.StraightBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating(self: "Self") -> "_410.StraightBevelGearSetRating":
        """mastapy.gears.rating.straight_bevel.StraightBevelGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_410.StraightBevelGearSetRating":
        """mastapy.gears.rating.straight_bevel.StraightBevelGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4256.StraightBevelGearSetPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearSetPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gears_system_deflection(
        self: "Self",
    ) -> "List[_2907.StraightBevelGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearsSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_gears_system_deflection(
        self: "Self",
    ) -> "List[_2907.StraightBevelGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelGearsSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_system_deflection(
        self: "Self",
    ) -> "List[_2905.StraightBevelGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelMeshesSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_meshes_system_deflection(
        self: "Self",
    ) -> "List[_2905.StraightBevelGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelMeshesSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearSetSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearSetSystemDeflection
        """
        return _Cast_StraightBevelGearSetSystemDeflection(self)
