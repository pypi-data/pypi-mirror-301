"""CylindricalGearSetPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4202

_CYLINDRICAL_GEAR_SET_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "CylindricalGearSetPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical import _477
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4139,
        _4187,
        _4188,
        _4223,
        _4228,
        _4244,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7016
    from mastapy._private.system_model.part_model.gears import _2585

    Self = TypeVar("Self", bound="CylindricalGearSetPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetPowerFlow._Cast_CylindricalGearSetPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetPowerFlow:
    """Special nested class for casting CylindricalGearSetPowerFlow to subclasses."""

    __parent__: "CylindricalGearSetPowerFlow"

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4202.GearSetPowerFlow":
        return self.__parent__._cast(_4202.GearSetPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4244.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4244

        return self.__parent__._cast(_4244.SpecialisedAssemblyPowerFlow)

    @property
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4139.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4139

        return self.__parent__._cast(_4139.AbstractAssemblyPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4223.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4223

        return self.__parent__._cast(_4223.PartPowerFlow)

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
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4228.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4228

        return self.__parent__._cast(_4228.PlanetaryGearSetPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "CylindricalGearSetPowerFlow":
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
class CylindricalGearSetPowerFlow(_4202.GearSetPowerFlow):
    """CylindricalGearSetPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2585.CylindricalGearSet":
        """mastapy.system_model.part_model.gears.CylindricalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7016.CylindricalGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating(self: "Self") -> "_477.CylindricalGearSetRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_477.CylindricalGearSetRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_power_flow(self: "Self") -> "List[_4188.CylindricalGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_gears_power_flow(
        self: "Self",
    ) -> "List[_4188.CylindricalGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearsPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_power_flow(self: "Self") -> "List[_4187.CylindricalGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_meshes_power_flow(
        self: "Self",
    ) -> "List[_4187.CylindricalGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalMeshesPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def ratings_for_all_designs(self: "Self") -> "List[_477.CylindricalGearSetRating]":
        """List[mastapy.gears.rating.cylindrical.CylindricalGearSetRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingsForAllDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetPowerFlow
        """
        return _Cast_CylindricalGearSetPowerFlow(self)
